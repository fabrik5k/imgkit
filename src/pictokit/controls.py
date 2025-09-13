from typing import Literal

import cv2
import numpy as np
from beartype import beartype

from pictokit.common import validate_imgarray
from pictokit.constants import GREY_SCALE_DIM


@beartype
def load_image(
    path: str | None = None,
    img_arr: np.ndarray | None = None,
    mode: Literal['gray', 'color', 'any'] = 'any',
    auto_convert: bool = True,
) -> np.ndarray:
    """Load and validate an image from either a file path or a NumPy array.

    Exactly one of `path` or `img_arr` must be provided.
    If `path` is given, the image will be read with OpenCV (`cv2.imread`).
    If `img_arr` is given, it will be validated directly.

    Args:
        path (str | None): Path to the image file. Mutually exclusive with `img_arr`.
        img_arr (np.ndarray | None): Image array to validate. Mutually exclusive with
            `path`.
        mode (Literal["gray", "color", "any"]): Expected image type.
            - "gray": grayscale only (shape `(H, W)`).
            - "color": color only (shape `(H, W, 3)`).
            - "any": accept both.
            Defaults to "any".
        auto_convert (bool): If True, automatically converts grayscale to BGR when
            `mode="color"`. Defaults to True.

    Returns:
        np.ndarray: A valid NumPy array (dtype `uint8`).
            - For grayscale: `(H, W)`
            - For color: `(H, W, 3)` (BGR format, OpenCV standard).

    Raises:
        ValueError: If neither or both `path` and `img_arr` are provided.
        FileNotFoundError: If the file at `path` cannot be read.
        TypeError: If `img_arr` is not a NumPy array or has invalid dtype.
        ValueError: If the image shape does not match the expected mode.

    """
    if (path is None) == (img_arr is None):
        raise ValueError("Provide exactly one of 'path' or 'img_arr'.")

    if path is not None:
        if mode == 'gray':
            flag = cv2.IMREAD_GRAYSCALE
        elif mode == 'color':
            flag = cv2.IMREAD_COLOR
        else:
            flag = cv2.IMREAD_UNCHANGED

        img = cv2.imread(path, flag)
        if img is None:
            raise FileNotFoundError(f'Could not read image from path: {path}')

        if mode == 'color' and img.ndim == GREY_SCALE_DIM and auto_convert:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        return validate_imgarray(img, mode=mode)

    img = validate_imgarray(img_arr, mode='any')  # aceita tanto gray quanto color

    if mode == 'color':
        if img.ndim == GREY_SCALE_DIM and auto_convert:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        img = validate_imgarray(img, mode='color')

    elif mode == 'gray':
        img = validate_imgarray(img, mode='gray')

    return img
