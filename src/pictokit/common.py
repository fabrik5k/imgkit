import numpy as np
from beartype import beartype

from pictokit.constants import GREY_SCALE_DIM, RGB_CHANNELS, RGB_DIM, Mode


@beartype
def validate_imgarray(img_arr: np.ndarray, mode: Mode = 'any') -> np.ndarray:
    """Validate whether an image array is valid according to type and shape.

    Returns the array itself if valid; otherwise, raises a clear exception.
    The validation rules are:
    - dtype: must be ``uint8``
    - shape: ``(H, W)`` for grayscale or ``(H, W, 3)`` for color
    - mode: enforces ``"gray"``, ``"color"``, or accepts both (``"any"``)

    Args:
        img_arr (np.ndarray): Image array to be validated.
        mode (Mode, optional): Validation mode. Can be ``"gray"``, ``"color"``,
            or ``"any"``. Defaults to ``"any"``.

    Returns:
        np.ndarray: The same array if it is valid.

    Raises:
        TypeError: If the array dtype is not ``uint8``.
        ValueError: If the array shape does not match the specified mode.
    """
    if img_arr.dtype != np.uint8:
        raise TypeError(f'img_arr must have dtype uint8, got {img_arr.dtype}.')

    if img_arr.ndim == GREY_SCALE_DIM:
        if mode in {'gray', 'any'}:
            return img_arr
        raise ValueError(
            f'Expected color image, got grayscale with shape {img_arr.shape}.'
        )

    if img_arr.ndim == RGB_DIM and img_arr.shape[2] == RGB_CHANNELS:
        if mode in {'color', 'any'}:
            return img_arr
        raise ValueError(
            f'Expected grayscale image, got color with shape {img_arr.shape}.'
        )

    raise ValueError(
        f'Invalid image shape {img_arr.shape}. '
        'Expected (H, W) for grayscale or (H, W, 3) for color.'
    )
