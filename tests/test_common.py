import numpy as np
import pytest
from beartype.roar import BeartypeCallHintParamViolation

from pictokit.common import validate_imgarray


# -----------------------------
# Helpers
# -----------------------------
def gray(h=10, w=20, dtype=np.uint8):
    return np.zeros((h, w), dtype=dtype)

def color(h=10, w=20, c=3, dtype=np.uint8):
    return np.zeros((h, w, c), dtype=dtype)


@pytest.mark.parametrize(
    "arr, mode",
    [
        (gray(1, 1), "gray"),
        (gray(7, 13), "any"),
        (color(1, 1, 3), "color"),
        (color(5, 8, 3), "any"),
    ],
)
def test_validate_imgarray_accept(arr, mode):
    out = validate_imgarray(arr, mode=mode)
    assert out is arr
    assert out.dtype == np.uint8


@pytest.mark.parametrize(
    "arr, mode",
    [
        (gray(10, 10), "color"),
        (color(10, 10, 3), "gray"),

        (np.zeros((10,), dtype=np.uint8), "any"),
        (np.zeros((10, 20, 1), dtype=np.uint8), "any"),
        (np.zeros((10, 20, 2), dtype=np.uint8), "any"),
        (np.zeros((10, 20, 4), dtype=np.uint8), "any"),
        (np.zeros((10, 20, 3, 1), dtype=np.uint8), "any"),
    ],
)
def test_validate_imgarray_value_error(arr, mode):
    with pytest.raises(ValueError):
        validate_imgarray(arr, mode=mode)


@pytest.mark.parametrize(
    "arr",
    [
        gray(10, 20, dtype=np.float32),
        color(10, 20, 3, dtype=np.float32),
        gray(5, 6, dtype=np.int16),
        color(5, 6, 3, dtype=np.int16),
    ],
)
def test_validate_imgarray_type_error(arr):
    with pytest.raises(TypeError):
        validate_imgarray(arr, mode="any")


@pytest.mark.parametrize(
    "bad_img, mode",
    [
        (None, "any"),
        (123, "any"),
        ("not-an-array", "any"),
        (object(), "any"),
        ([1, 2, 3], "any"),
    ],
)
def test_validate_imgarray_type_error_param_img_arr(bad_img, mode):
    with pytest.raises(BeartypeCallHintParamViolation):
        validate_imgarray(bad_img, mode=mode)

@pytest.mark.parametrize(
    "good_img, bad_mode",
    [
        (gray(2, 2), "rgba"),
        (gray(2, 2), "grey"),
        (gray(2, 2), 1),
        (gray(2, 2), None),
    ],
)
def test_validate_imgarray_type_error_param_mode(good_img, bad_mode):
    with pytest.raises(BeartypeCallHintParamViolation):
        validate_imgarray(good_img, mode=bad_mode)

