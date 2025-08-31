from beartype import beartype


@beartype
def expansao_de_pixel(pixel: int, limite_L: int, limite_H: int) -> int:
    MIN_VALUE_PIXEL = 0
    MAX_VALUE_PIXEL = 255
    args = {'pixel': pixel, 'limite_L': limite_L, 'limite_H': limite_H}
    for name, value in args.items():
        if not (MIN_VALUE_PIXEL <= value <= MAX_VALUE_PIXEL):
            raise ValueError(
                f'Expected {name} to be in the range 0 to 255, but received {value}'
            )
    if pixel > limite_L and pixel < limite_H:
        result = 255 / (limite_H - limite_L) * (pixel - limite_L)
    else:
        result = pixel

    result = int(result)
    return result
