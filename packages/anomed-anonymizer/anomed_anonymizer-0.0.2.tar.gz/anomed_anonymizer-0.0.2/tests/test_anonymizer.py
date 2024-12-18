import tempfile
from pathlib import Path

import numpy as np
import pytest

from anomed_anonymizer import anonymizer


@pytest.fixture()
def empty_ndarray() -> np.ndarray:
    return np.array([])


@pytest.fixture()
def ten_elem_ndarray() -> np.ndarray:
    return np.arange(10)


@pytest.fixture()
def ten_ones_ndarray() -> np.ndarray:
    return np.ones(shape=(10,))


class Dummy:
    def __init__(self) -> None:
        pass

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        pass

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.ones(shape=(len(X),))

    def validate_input(self, X: np.ndarray) -> None:
        pass


@pytest.fixture()
def dummy_anonymizer():
    return Dummy()


def test_WrappedAnonymizer(
    dummy_anonymizer, empty_ndarray, ten_elem_ndarray, ten_ones_ndarray
):
    wrapped_anon = anonymizer.WrappedAnonymizer(
        dummy_anonymizer, anonymizer.pickle_anonymizer
    )
    wrapped_anon.fit(ten_elem_ndarray, ten_elem_ndarray)
    assert np.array_equal(wrapped_anon.predict(empty_ndarray), empty_ndarray)
    assert np.array_equal(wrapped_anon.predict(ten_elem_ndarray), ten_ones_ndarray)
    assert np.array_equal(wrapped_anon.predict(ten_elem_ndarray, 4), ten_ones_ndarray)
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_dir = Path(tmpdirname)
        wrapped_anon.save(tmp_dir / "foo.bar")
        assert (tmp_dir / "foo.bar").exists()


def test_batch_views(empty_ndarray, ten_elem_ndarray):
    [batch] = anonymizer._batch_views(empty_ndarray, 0)
    assert len(batch) == 0

    assert [] == anonymizer._batch_views(ten_elem_ndarray, -1)
    assert [] == anonymizer._batch_views(ten_elem_ndarray, 0)

    [batch] = anonymizer._batch_views(ten_elem_ndarray, None)
    assert np.array_equal(batch, ten_elem_ndarray)

    [batch] = anonymizer._batch_views(ten_elem_ndarray, 10)
    assert np.array_equal(batch, ten_elem_ndarray)

    [batch] = anonymizer._batch_views(ten_elem_ndarray, 11)
    assert np.array_equal(batch, ten_elem_ndarray)

    batches = anonymizer._batch_views(ten_elem_ndarray, 3)
    assert np.array_equal(np.concatenate(batches), ten_elem_ndarray)
