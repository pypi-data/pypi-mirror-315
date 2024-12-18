import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterable, Literal

import anomed_utils as utils
import falcon
import numpy as np
import requests
from filelock import FileLock, Timeout

from . import anonymizer


class FitResource:
    def __init__(
        self,
        anon_obj: anonymizer.SupervisedLearningAnonymizer,
        model_filepath: str | Path,
        training_data_url: str,
    ) -> None:
        self._anon = anon_obj
        self._expected_array_labels = ["X", "y"]
        self._training_data_url = training_data_url
        self._timeout = 10.0
        self._model_filepath = Path(model_filepath)
        self._model_lock = FileLock(
            self._model_filepath.with_suffix(".lock"), blocking=False
        )

    def on_post(self, _: falcon.Request, resp: falcon.Response) -> None:
        array_payload = _get_data_from_platform(
            self._training_data_url, self._timeout, "Failed to obtain training data."
        )
        _validate_array_payload(
            array_payload, self._expected_array_labels, origin="server"
        )

        training_data = utils.bytes_to_named_ndarrays(array_payload)
        (X, y) = (
            training_data[self._expected_array_labels[0]],
            training_data[self._expected_array_labels[1]],
        )

        _validate_array_input(
            X,
            self._anon,
            "The anonymizer is not compatible with the training data.",
            origin="server",
        )

        try:
            with self._model_lock:
                self._anon.fit(X, y)
                self._anon.save(self._model_filepath)
        except Timeout:
            error_msg = "A training for this anonymizer is already in progress."
            logging.exception(error_msg)
            raise falcon.HTTPError(
                status=falcon.HTTP_SERVICE_UNAVAILABLE,
                description=json.dumps(dict(message=error_msg)),
            )

        resp.text = json.dumps(
            dict(message="Training has been completed successfully.")
        )


def _get_data_from_platform(data_url: str, timeout, error_msg: str) -> bytes:
    try:
        training_data_resp = requests.get(url=data_url, timeout=timeout)
        if training_data_resp.status_code != 200:
            raise ValueError()
        return training_data_resp.content
    except (requests.ConnectionError, ValueError):
        logging.exception(error_msg)
        raise falcon.HTTPError(
            status=falcon.HTTP_SERVICE_UNAVAILABLE, description=error_msg
        )


def _validate_array_payload(
    payload: bytes,
    expected_array_labels: Iterable[str],
    origin: Literal["client", "server"],
) -> None:
    try:
        array_payload = utils.bytes_to_named_ndarrays(payload)
        if not all(
            [
                expected_label in array_payload
                for expected_label in expected_array_labels
            ]
        ):
            raise ValueError("Array payload does not contain all expected labels.")
    except (OSError, ValueError, EOFError):
        error_msg = "Array payload validation failed."
        logging.exception(error_msg)
        if origin == "client":
            raise falcon.HTTPBadRequest(description=error_msg)
        else:
            assert origin == "server"
            raise falcon.HTTPInternalServerError(description=error_msg)


def _validate_array_input(
    input_array: np.ndarray,
    anon: anonymizer.SupervisedLearningAnonymizer,
    error_msg: str,
    origin: Literal["client", "server"],
) -> None:
    try:
        anon.validate_input(input_array)
    except ValueError:
        logging.exception(error_msg)
        if origin == "client":
            raise falcon.HTTPBadRequest(description=error_msg)
        else:
            assert origin == "server"
            raise falcon.HTTPInternalServerError(
                description=error_msg,
            )


class InferenceResource:
    def __init__(
        self,
        anonymizer_identifier: str,
        model_filepath: str | Path,
        model_loader: Callable[[str | Path], anonymizer.SupervisedLearningAnonymizer],
        default_batch_size: int,
        tuning_data_url: str,
        validation_data_url: str,
        utility_evaluation_url: str,
    ) -> None:
        self._anon_id = anonymizer_identifier
        self._model_filepath = Path(model_filepath)
        self._load_model = model_loader
        self._default_batch_size = default_batch_size
        self._url_mapper = dict(
            tuning=tuning_data_url,
            validation=validation_data_url,
            utility=utility_evaluation_url,
        )
        self._timeout = 10.0
        self._loaded_model: anonymizer.SupervisedLearningAnonymizer = None  # type: ignore
        self._loaded_model_modification_time: datetime = None  # type: ignore
        self._expected_array_label = "X"

    def on_post_predict(self, req: falcon.Request, resp: falcon.Response) -> None:
        self._load_most_recent_model()

        array_bytes = req.bounded_stream.read()
        _validate_array_payload(
            array_bytes, [self._expected_array_label], origin="client"
        )
        array_payload = utils.bytes_to_named_ndarrays(array_bytes)
        _validate_array_input(
            array_payload[self._expected_array_label],
            self._loaded_model,
            "Supplied array is not compatible with the anonymizer.",
            origin="client",
        )

        batch_size = req.get_param_as_int("batch_size", default=None)
        prediction = self._loaded_model.predict(
            X=array_payload[self._expected_array_label], batch_size=batch_size
        )
        resp.data = utils.named_ndarrays_to_bytes(dict(prediction=prediction))
        resp.status = falcon.HTTP_CREATED

    def on_post_evaluate(self, req: falcon.Request, resp: falcon.Response) -> None:
        self._load_most_recent_model()

        try:
            data_split = req.get_param("data_split", required=True)
        except falcon.HTTPBadRequest:
            error_msg = "Query parameter 'data_split' is missing!"
            logging.exception(error_msg)
            raise falcon.HTTPBadRequest(description=error_msg)

        try:
            array_payload = _get_data_from_platform(
                self._url_mapper[data_split],
                self._timeout,
                f"Failed to obtain {data_split} data.",
            )
        except KeyError:
            raise falcon.HTTPBadRequest(
                description="Query parameter 'data_split' needs to be either 'tuning' or 'validation'."
            )
        _validate_array_payload(
            array_payload,
            expected_array_labels=[self._expected_array_label],
            origin="server",
        )

        array = utils.bytes_to_named_ndarrays(array_payload)
        X = array[self._expected_array_label]
        prediction = self._loaded_model.predict(X, self._default_batch_size)

        evaluation_response = requests.post(
            url=self._url_mapper["utility"],
            data=utils.named_ndarrays_to_bytes(dict(prediction=prediction)),
            params=dict(anonymizer=self._anon_id, data_split=data_split),
        )
        if evaluation_response.status_code == 201:
            resp.text = json.dumps(
                dict(
                    message=(
                        f"The anonymizer has been evaluated based on {data_split} data."
                    ),
                    evaluation=evaluation_response.json(),
                )
            )
            resp.status = falcon.HTTP_CREATED
        else:
            error_msg = "Utility evaluation failed."
            logging.exception(error_msg)
            raise falcon.HTTPInternalServerError(description=error_msg)

    def _load_most_recent_model(self) -> None:
        if not self._model_filepath.exists():
            error_msg = "This anonymizer is not fitted/trained yet."
            logging.exception(error_msg)
            raise falcon.HTTPBadRequest(
                description=error_msg,
            )
        mod_time_from_disk = datetime.fromtimestamp(
            self._model_filepath.stat().st_mtime
        )
        if _is_older(self._loaded_model_modification_time, mod_time_from_disk):
            self._loaded_model = self._load_model(self._model_filepath)
            self._loaded_model_modification_time = mod_time_from_disk
        else:
            # keep the current model as it is already recent enough
            pass


def _is_older(dt1: datetime | None, dt2: datetime) -> bool:
    """Tell whether `dt1` is older (i.e. more in the past) than `dt2`. If `dt1`
    is the same as `dt2`, or even if `dt1` is `None`, output `True`."""
    if dt1 is None:
        return True
    else:
        return dt1 <= dt2


def supervised_learning_anonymizer_server_factory(
    anonymizer_identifier: str,
    anonymizer_obj: anonymizer.SupervisedLearningAnonymizer,
    default_batch_size: int,
    training_data_url: str,
    tuning_data_url: str,
    validation_data_url: str,
    utility_evaluation_url: str,
    model_loader: Callable[[str | Path], anonymizer.SupervisedLearningAnonymizer],
) -> falcon.App:
    """A factory to create a web application object which hosts an
    `anonymizer.SupervisedLearningAnonymizer`, currently the most basic use
    case of anonymizers (privacy preserving ML models) for the AnoMed
    competition platform.

    By using this factory, you don't have to worry any web-programming issues,
    as they are hidden from you. The generated web app will feature the
    following routes (more details may be found in this project's openapi
    specification):

    * [GET] `/`
    * [POST] `/fit`
    * [POST] `/evaluate`
    * [POST] `/predict`

    Parameters
    ----------
    anonymizer_obj : anonymizer.SupervisedLearningAnonymizer
        An anonymizer that is based on the supervised learning paradigm

    Returns
    -------
    falcon.App
        A web application object based on the falcon web framework.
    """
    app = falcon.App()

    app.add_route(
        "/", utils.StaticJSONResource(dict(message="Anonymizer server is alive!"))
    )
    app.add_route(
        "/fit",
        FitResource(
            anon_obj=anonymizer_obj,
            model_filepath="model",
            training_data_url=training_data_url,
        ),
    )
    ir = InferenceResource(
        anonymizer_identifier=anonymizer_identifier,
        model_filepath="model",
        model_loader=model_loader,
        default_batch_size=default_batch_size,
        tuning_data_url=tuning_data_url,
        validation_data_url=validation_data_url,
        utility_evaluation_url=utility_evaluation_url,
    )
    app.add_route("/evaluate", ir, suffix="evaluate")
    app.add_route("/predict", ir, suffix="predict")
    return app
