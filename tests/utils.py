import numpy as np
from beartype import beartype


@beartype
def gerar_imagem_aleatoria(x: int, y: int, dtype: str = "uint8",
                           max_value=None, seed: int | None = None) -> np.ndarray:
    """
    Gera um array aleatório com shape (x, y, 3) que se comporta como imagem RGB.

    Args:
        x (int): Altura.
        y (int): Largura.
        dtype (str): 'uint8' (0..255) ou 'float' (0.0..1.0). Padrão: 'uint8'.
        max_value (int|float|None, optional): Valor máximo permitido para os
            pixels:
            - Se None (padrão), usa o limite do dtype:
              - 255 para 'uint8'.
              - 1.0 para 'float'.
            - Se informado:
              - Deve ser int quando dtype='uint8'.
              - Deve ser float quando dtype='float'.
            O valor informado é limitado ao intervalo válido do dtype.
        seed (int|None): Semente para reprodutibilidade.

    Returns:
        np.ndarray: Imagem aleatória (x, y, 3).
    """
    rng = np.random.default_rng(seed)

    if dtype == "uint8":
        # teto permitido (0..255); se max_value vier, respeita o teto do tipo
        high = 256 if max_value is None else int(min(255, max(0, max_value))) + 1
        img = rng.integers(0, high, size=(x, y, 3), dtype=np.uint8)

    elif dtype == "float":
        # teto permitido (0.0..1.0); se max_value vier, clipa ao intervalo
        maxv = 1.0 if max_value is None else float(max(0.0, min(1.0, max_value)))
        img = (rng.random((x, y, 3), dtype=np.float32) * maxv).astype(np.float32)

    else:
        raise ValueError("dtype deve ser 'uint8' ou 'float'.")

    return img
