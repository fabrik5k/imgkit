from typing import Literal

import numpy as np
from beartype import beartype

from pictokit.constants import (
    GREY_SCALE_CHANNEL_DIM,
    PIXEL_MAX,
    PIXEL_MIN,
    RGB_CHANNELS,
)


@beartype
def gerar_imagem_aleatoria(
    x: int,
    y: int,
    channels: Literal[1, 3] = 3,
    max_value: int | None = None,
    seed: int | None = None,
) -> np.ndarray:
    """
    Gera um array aleatório que se comporta como imagem, sempre no formato uint8.

    Args:
        x (int): Altura.
        y (int): Largura.
        channels (int): Número de channels da imagem:
            - 1 → grayscale (shape (x, y)).
            - 3 → RGB (shape (x, y, 3)).
        max_value (int|None, optional): Valor máximo permitido para os pixels:
            - Se None (padrão), usa 255.
            - Se informado, deve estar no intervalo [0, 255].
        seed (int|None): Semente para reprodutibilidade.

    Returns:
        np.ndarray: Imagem aleatória no formato uint8.
    """
    if max_value is not None:
        if not (max_value >= PIXEL_MIN + 1 and max_value <= PIXEL_MAX):
            raise ValueError(
                f'max_value must be between {PIXEL_MIN + 1} and {PIXEL_MAX}'
                f', but got {max_value}'
            )
        high = max_value
    else:
        high = 256

    if not (x > 0 and y > 0):
        raise ValueError(f'x and y must be greater then 0, but x={x} y={y}')

    rng = np.random.default_rng(seed)

    if channels == GREY_SCALE_CHANNEL_DIM:
        return rng.integers(0, high, size=(x, y), dtype=np.uint8)
    else:
        return rng.integers(0, high, size=(x, y, RGB_CHANNELS), dtype=np.uint8)
