from beartype import beartype


@beartype
def expansao_de_pixel(pixel: int, limite_L: int, limite_H: int) -> int:
    """
    Aplica uma transformação de expansão de contraste em um pixel,
    mapeando valores dentro de um intervalo [limite_L, limite_H] para o
    intervalo [0, 255].

    Se o valor do `pixel` estiver dentro do intervalo definido por
    (`limite_L`, `limite_H`), o valor é reescalonado linearmente para o
    intervalo [0, 255]. Caso contrário, o pixel é retornado sem alteração.

    Além disso, são realizadas validações nos parâmetros:
      - `pixel`, `limite_L` e `limite_H` devem estar no intervalo [0, 255].
      - `limite_L` deve ser estritamente menor que `limite_H`.

    Args:
        pixel (int): Valor do pixel (0–255).
        limite_L (int): Limite inferior do intervalo (0–255).
        limite_H (int): Limite superior do intervalo (0–255).

    Returns:
        int: Valor transformado do pixel no intervalo [0, 255].
    """
    MIN_VALUE_PIXEL = 0
    MAX_VALUE_PIXEL = 255
    args = {'pixel': pixel, 'limite_L': limite_L, 'limite_H': limite_H}
    for name, value in args.items():
        if not (MIN_VALUE_PIXEL <= value <= MAX_VALUE_PIXEL):
            raise ValueError(
                f'Expected {name} to be in the range 0 to 255, but received {value}'
            )
    if limite_L >= limite_H:
        raise ValueError(
            f'Lower limit must be strictly less than upper limit, '
            f'but received limite_L={limite_L}, limite_H={limite_H}'
        )
    if pixel > limite_L and pixel < limite_H:
        result = 255 / (limite_H - limite_L) * (pixel - limite_L)
    else:
        result = pixel

    result = int(result)
    return result
