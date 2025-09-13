from beartype import beartype

from pictokit.constants import PIXEL_MAX, PIXEL_MIN


@beartype
def pixel_expansion(pixel: int, low_limit: int, high_limit: int) -> int:
    """
    Applies a contrast expansion transformation to a pixel by mapping values
    within a given range [low_limit, high_limit] to the full range [0, 255].

    If the `pixel` value falls within the specified interval, it is linearly
    rescaled to [0, 255]. Otherwise, the pixel value is returned unchanged.

    Args:
        pixel (int): Pixel value (0–255).
        low_limit (int): Lower bound of the intensity range (0–255).
        high_limit (int): Upper bound of the intensity range (0–255).

    Returns:
        int: The transformed pixel value in the range [0, 255].

    Raises:
        ValueError: If `pixel`, `low_limit`, or `high_limit` are outside the
            range [0, 255], or if `low_limit >= high_limit`.
    """
    args = {'pixel': pixel, 'low_limit': low_limit, 'high_limit': high_limit}
    for name, value in args.items():
        if not (PIXEL_MIN <= value <= PIXEL_MAX):
            raise ValueError(
                f'Expected {name} to be in the range 0 to 255, but received {value}'
            )
    if low_limit >= high_limit:
        raise ValueError(
            f'Lower limit must be strictly less than upper limit, '
            f'but received low_limit={low_limit}, high_limit={high_limit}'
        )
    if pixel > low_limit and pixel < high_limit:
        result = 255 / (high_limit - low_limit) * (pixel - low_limit)
    else:
        result = pixel

    result = int(result)
    return result
