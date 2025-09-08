import numpy as np
import pytest

from pictokit.utils import gerar_imagem_aleatoria


@pytest.fixture
def image_obj():
    args = {'x': 256, 'y': 256, 'channels': 3, 'max_value': None, 'seed': None}
    img = gerar_imagem_aleatoria(**args)
    return img


@pytest.fixture
def gray_u8():
    return np.random.default_rng(0).integers(0, 256, size=(10, 12), dtype=np.uint8)


@pytest.fixture
def color_u8():
    return np.random.default_rng(1).integers(0, 256, size=(8, 9, 3), dtype=np.uint8)


@pytest.fixture
def gray_f32():
    return np.random.default_rng(2).random(size=(7, 11)).astype(np.float32)


@pytest.fixture
def color_bad_channels_u8():
    # 4 canais em vez de 3 (BGRX, por ex.)
    return np.random.default_rng(3).integers(0, 256, size=(6, 6, 4), dtype=np.uint8)
