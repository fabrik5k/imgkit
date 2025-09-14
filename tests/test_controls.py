# ruff: noqa: PLR2004
import cv2 as _cv2
import numpy as np
import pytest

from pictokit.constants import GREY_SCALE_DIM, RGB_CHANNELS, RGB_DIM
from pictokit.controls import calculate_histogram, load_image


@pytest.mark.parametrize(
    ('kwargs', 'check'),
    [
        (
            {'img_arr': 'gray_u8', 'mode': 'color', 'auto_convert': True},
            lambda out: out.ndim == RGB_DIM and out.shape[2] == RGB_CHANNELS,
        ),
        (
            {'path': 'fake_gray.png', 'mode': 'gray'},
            lambda out: out.ndim == GREY_SCALE_DIM and out.dtype == np.uint8,
        ),
        (
            {'path': 'fake_color.png', 'mode': 'color'},
            lambda out: out.ndim == RGB_DIM
            and out.shape[2] == RGB_CHANNELS
            and out.dtype == np.uint8,
        ),
        (
            {
                'path': 'fake_gray_for_color.png',
                'mode': 'color',
                'auto_convert': True,
            },
            lambda out: out.ndim == RGB_DIM and out.shape[2] == RGB_CHANNELS,
        ),
        (
            {'img_arr': 'gray_u8', 'mode': 'any'},
            lambda out: out.ndim in {2, 3} and out.dtype == np.uint8,
        ),
        (
            {'img_arr': 'color_u8', 'mode': 'any'},
            lambda out: out.ndim in {2, 3} and out.dtype == np.uint8,
        ),
        (
            {'img_arr': 'gray_u8', 'mode': 'gray'},
            lambda out: out.ndim == GREY_SCALE_DIM and out.dtype == np.uint8,
        ),
        (
            {'img_arr': 'color_u8', 'mode': 'color'},
            lambda out: out.ndim == RGB_DIM
            and out.shape[2] == RGB_CHANNELS
            and out.dtype == np.uint8,
        ),
    ],
)
def test_load_image_accept(kwargs, check, monkeypatch, gray_u8, color_u8):
    def fake_imread(path, flag):
        if 'gray' in path:
            return gray_u8.copy()
        elif 'color' in path:
            return color_u8.copy()
        return None

    def fake_cvt_color(img, code):
        if img.ndim == GREY_SCALE_DIM and code == _cv2.COLOR_GRAY2BGR:
            h, w = img.shape
            out = np.stack([img, img, img], axis=2)
            assert out.shape == (h, w, RGB_DIM)
            return out
        return img

    monkeypatch.setattr('cv2.imread', fake_imread)
    monkeypatch.setattr('cv2.cvtColor', fake_cvt_color)

    if isinstance(kwargs.get('img_arr'), str):
        kwargs = dict(kwargs)
        kwargs['img_arr'] = {'gray_u8': gray_u8, 'color_u8': color_u8}[
            kwargs['img_arr']
        ]

    out = load_image(**kwargs)
    assert check(out)


@pytest.mark.parametrize(
    ('kwargs'),
    [
        ({'mode': 'any'}),
        ({
            'path': 'x.png',
            'img_arr': np.zeros((2, 2), dtype=np.uint8),
            'mode': 'any',
        }),
        ({
            'img_arr': np.zeros((5, 5, 3), dtype=np.uint8),
            'mode': 'gray',
            'auto_convert': False,
        }),
        ({
            'img_arr': np.zeros((5, 7), dtype=np.uint8),
            'mode': 'color',
            'auto_convert': False,
        }),
        ({'img_arr': np.zeros((6, 6, 4), dtype=np.uint8), 'mode': 'color'}),
    ],
)
def test_load_image_value_error(kwargs):
    with pytest.raises(ValueError, match=''):  # noqa: PT011
        load_image(**kwargs)


@pytest.mark.parametrize(
    ('kwargs', 'expected_exception'),
    [
        ({'img_arr': [[1, 2], [3, 4]], 'mode': 'any'}, Exception),
        ({'img_arr': np.zeros((2, 2), dtype=np.uint8), 'mode': 'INVALID'}, Exception),
        ({'img_arr': np.zeros((4, 4), dtype=np.float32), 'mode': 'any'}, TypeError),
    ],
)
def test_load_image_type_error(kwargs, expected_exception):
    with pytest.raises(expected_exception, match=''):  # noqa: PT011
        load_image(**kwargs)


@pytest.mark.parametrize(
    ('path', 'mode'),
    [
        ('dont_exist.png', 'any'),
        ('dont_exist_gray.png', 'gray'),
        ('dont_exist_color.png', 'color'),
    ],
)
def test_load_image_file_not_found_error(path, mode, monkeypatch):
    def fake_imread_fail(_path, _flag):
        return None

    monkeypatch.setattr('cv2.imread', fake_imread_fail)

    with pytest.raises(FileNotFoundError):
        load_image(path=path, mode=mode)


@pytest.mark.parametrize(
    ('arr', 'mode', 'auto_convert', 'should_pass'),
    [
        (np.zeros((3, 5), dtype=np.uint8), 'gray', False, True),
        (np.zeros((3, 5), dtype=np.uint8), 'color', False, False),
        (np.zeros((3, 5), dtype=np.uint8), 'color', True, True),
        (np.zeros((4, 4, 3), dtype=np.uint8), 'color', False, True),
        (np.zeros((4, 4, 4), dtype=np.uint8), 'color', False, False),
    ],
)
def test_load_image_limits_on_dims(arr, mode, auto_convert, should_pass, monkeypatch):
    def fake_cvt_color(img, code):
        if img.ndim == GREY_SCALE_DIM and code == _cv2.COLOR_GRAY2BGR:
            return np.stack([img, img, img], axis=2)
        return img

    monkeypatch.setattr('cv2.cvtColor', fake_cvt_color)

    if should_pass:
        out = load_image(img_arr=arr, mode=mode, auto_convert=auto_convert)
        if mode == 'gray':
            assert out.ndim == GREY_SCALE_DIM
        if mode == 'color':
            assert out.ndim == RGB_DIM
            assert out.shape[2] == RGB_CHANNELS
    else:
        with pytest.raises(ValueError, match=''):  # noqa: PT011
            load_image(img_arr=arr, mode=mode, auto_convert=auto_convert)


@pytest.mark.parametrize(
    ('img', 'bins', 'expected_check'),
    [
        # basic cases
        (
            np.array([0, 0, 1, 2, 2, 2, 255]),
            256,
            lambda h: h[0] == 2
            and h[1] == 1
            and h[2] == 3
            and h[255] == 1
            and np.sum(h) == 7,
        ),
        # Empty Images
        (
            np.array([]),
            256,
            lambda h: np.all(h == 0) and h.shape == (256,),
        ),
        # Repeated single pixel
        (
            np.full((10,), 128),
            256,
            lambda h: h[128] == 10 and np.sum(h) == 10,
        ),
        # Custom bins
        (
            np.array([0, 1, 1, 2, 3]),
            4,
            lambda h: h.tolist() == [1, 2, 1, 1],
        ),
        # A big random image
        (
            np.random.randint(0, 256, size=(1000, 1000), dtype=int),
            256,
            lambda h: np.sum(h) == 1_000_000,  # noqa: PLR2004
        ),
    ],
)
def test_calculate_histogram_accept(img, bins, expected_check):
    h = calculate_histogram(img, bins=bins)
    assert expected_check(h)
