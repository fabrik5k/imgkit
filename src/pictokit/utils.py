from typing import Literal

import numpy as np
from beartype import beartype


@beartype
def gerar_imagem_aleatoria(x: int, y: int,
                           channels: Literal[1, 3] = 3,
                           max_value: int | None = None,
                           seed: int | None = None) -> np.ndarray:
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
    rng = np.random.default_rng(seed)

    # teto permitido (0..255); se max_value vier, respeita o teto
    high = 256 if max_value is None else int(min(255, max(0, max_value))) + 1

    if channels == 1:
        return rng.integers(0, high, size=(x, y), dtype=np.uint8)
    else:
        return rng.integers(0, high, size=(x, y, 3), dtype=np.uint8)
