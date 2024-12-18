import time
from pathlib import Path
from unittest.mock import MagicMock

import anomed_utils as utils
import falcon
import numpy as np
import pytest
import requests
from falcon import testing

import anomed_anonymizer as anonymizer


@pytest.fixture()
def example_features() -> np.ndarray:
    return np.arange(10)


@pytest.fixture()
def example_targets() -> np.ndarray:
    return np.zeros(shape=(10,))


@pytest.fixture()
def example_dataset(example_features, example_targets) -> dict[str, np.ndarray]:
    return dict(X=example_features, y=example_targets)


class Dummy:
    def __init__(self) -> None:
        pass

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        pass

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.ones(shape=(len(X),))

    def save(self, filepath: str | Path) -> None:
        with open(filepath, "w") as file:
            file.write("test")

    def validate_input(self, X: np.ndarray) -> None:
        pass


class LongFitDummy(Dummy):
    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        time.sleep(1)


@pytest.fixture()
def dummy_anonymizer() -> anonymizer.SupervisedLearningAnonymizer:
    return anonymizer.WrappedAnonymizer(Dummy())


@pytest.fixture()
def dummy_long_fit_anonymizer() -> anonymizer.SupervisedLearningAnonymizer:
    return anonymizer.WrappedAnonymizer(LongFitDummy())


@pytest.fixture()
def dummy_server_args():
    return dict(
        anonymizer_identifier="example_anonymizer",
        default_batch_size=64,
        training_data_url="http://example.com/train",
        tuning_data_url="http://example.com/tuning",
        validation_data_url="http://example.com/validation",
        utility_evaluation_url="http://example.com/utility",
    )


@pytest.fixture()
def client(dummy_anonymizer, dummy_server_args):
    return testing.TestClient(
        app=anonymizer.supervised_learning_anonymizer_server_factory(
            anonymizer_obj=dummy_anonymizer,
            model_loader=lambda _: dummy_anonymizer,
            **dummy_server_args,
        )
    )


@pytest.fixture()
def long_fit_client(dummy_long_fit_anonymizer, dummy_server_args):
    return testing.TestClient(
        app=anonymizer.supervised_learning_anonymizer_server_factory(
            anonymizer_obj=dummy_long_fit_anonymizer,
            model_loader=lambda _: dummy_long_fit_anonymizer,
            **dummy_server_args,
        )
    )


def test_availability(client):
    message = {"message": "Anonymizer server is alive!"}
    response = client.simulate_get("/")
    assert response.json == message


def test_successful_fit_invocation(client, mocker, example_dataset, dummy_server_args):
    mock = _mock_get_numpy_arrays(mocker, example_dataset)

    response = client.simulate_post("/fit")
    assert mock.call_args.kwargs["url"] == dummy_server_args["training_data_url"]
    assert response.status == falcon.HTTP_OK
    assert response.json == dict(message="Training has been completed successfully.")


def _mock_get_numpy_arrays(
    _mocker, named_arrays: dict[str, np.ndarray], status_code: int = 200
) -> MagicMock:
    mock_response = _mocker.MagicMock()
    mock_response.status_code = status_code
    mock_response.content = utils.named_ndarrays_to_bytes(named_arrays)
    return _mocker.patch("requests.get", return_value=mock_response)


def test_failing_fit_invocation_data(client, mocker):
    mock_response = mocker.MagicMock()
    mock_response.side_effect = requests.ConnectionError()

    response = client.simulate_post("/fit", params=dict(batch_size=8))
    assert response.status == falcon.HTTP_SERVICE_UNAVAILABLE


# def test_failing_fit_invocation_parallel_fit(long_fit_client, mocker, example_dataset):
#     mock_response = mocker.MagicMock()
#     mock_response.status_code = 200
#     mock_response.content = utils.named_ndarrays_to_bytes(example_dataset)
#     mocker.patch("requests.get", return_value=mock_response)

#     _ = long_fit_client.simulate_post("/fit", params=dict(batch_size=8))
#     response = long_fit_client.simulate_post("/fit", params=dict(batch_size=8))
#     assert response.status == falcon.HTTP_SERVICE_UNAVAILABLE


def test_successful_utility_evaluation(
    client, mocker, example_dataset, example_features, dummy_server_args
):
    for data_split in ["tuning", "validation"]:
        # Initiate training to have something to evaluate
        _mock_get_numpy_arrays(mocker, example_dataset)
        client.simulate_post("/fit")

        data_mock = _mock_get_numpy_arrays(mocker, dict(X=example_features))
        utility_mock_json = {
            "mae": 13.37,
            "rmse": 4.20,
            "coeff_determ": 0.82,
        }
        _mock_post_json(mocker, utility_mock_json)
        response = client.simulate_post("/evaluate", params=dict(data_split=data_split))
        assert (
            data_mock.call_args.kwargs["url"]
            == dummy_server_args[
                "tuning_data_url" if data_split == "tuning" else "validation_data_url"
            ]
        )

        assert response.status == falcon.HTTP_CREATED
        assert response.json == dict(
            message=f"The anonymizer has been evaluated based on {data_split} data.",
            evaluation=utility_mock_json,
        )


def _mock_post_json(_mocker, _json, status_code: int = 201) -> MagicMock:
    mock_response = _mocker.MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = _json
    return _mocker.patch("requests.post", return_value=mock_response)


def test_successful_predict(client, dummy_anonymizer, example_features):
    batch_size = 8
    response = client.simulate_post(
        "/predict",
        params=dict(batch_size=batch_size),
        body=utils.named_ndarrays_to_bytes(dict(X=example_features)),
    )
    assert response.status == falcon.HTTP_CREATED
    prediction = utils.bytes_to_named_ndarrays(response.content)
    assert np.array_equal(
        prediction["prediction"],
        dummy_anonymizer.predict(example_features, batch_size=batch_size),
    )
