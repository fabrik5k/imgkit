import pytest

from pictokit.utils import gerar_imagem_aleatoria


@pytest.mark.parametrize(
    ('x', 'y', 'channels', 'max_value', 'seed', 'shape'),
    [
        (1, 1, 1, None, None, (1, 1)),
        (1, 1, 1, 1, None, (1, 1)),
        (26, 26, 3, 10, 10, (26, 26, 3)),
    ],
)
def test_generate_random_image_accept(x, y, channels, max_value, seed, shape):
    arr = gerar_imagem_aleatoria(x, y, channels, max_value, seed)
    assert arr.shape == shape


@pytest.mark.parametrize(
    ('x', 'y', 'channels', 'max_value', 'error_message'),
    [
        # x and y
        (0, 1, 1, 1, 'x and y must be'),
        (1, 0, 1, 1, 'x and y must be'),
        # max_value
        (1, 1, 1, 0, 'max_value must be'),
        (1, 1, 1, 256, 'max_value must be'),
    ],
)
def test_generate_random_image_value_error(x, y, channels, max_value, error_message):
    with pytest.raises(ValueError, match=error_message):
        gerar_imagem_aleatoria(x, y, channels, max_value)
