import pytest
import numpy as np

from pictokit.utils import gerar_imagem_aleatoria


@pytest.fixture
def image_obj():
    args = {'x': 256, 'y': 256, 'channels': 3, 'max_value': None, 'seed': None}
    img = gerar_imagem_aleatoria(**args)
    return img
