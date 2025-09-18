import numpy as np
import pytest
from beartype.roar import BeartypeCallHintParamViolation

import pictokit.element_wise as elw


class TestExpansaoDePixel:
    @staticmethod
    @pytest.mark.parametrize(
        ('pixel', 'low_limit', 'high_limit', 'expect_result'),
        [
            (99, 100, 110, 99),
            (100, 100, 110, 100),
            (101, 100, 110, 25),
            (109, 100, 110, 229),
            (110, 100, 110, 110),
            (111, 100, 110, 111),
            (0, 0, 255, 0),
            (255, 0, 255, 255),
        ],
    )
    def test_pixel_expansion_accept(pixel, low_limit, high_limit, expect_result):
        resultado = elw.pixel_expansion(np.uint8(pixel), low_limit, high_limit)
        assert expect_result == resultado

    @staticmethod
    @pytest.mark.parametrize(
        ('pixel', 'low_limit', 'high_limit'),
        [
            ('99', 100, 110),
            (np.uint8(100), 100.0, 110),
            (['101'], 100, 110),
            (np.uint(109), 100, [110]),
        ],
    )
    def test_pixel_expansion_raise_type_error(pixel, low_limit, high_limit):
        with pytest.raises(BeartypeCallHintParamViolation):
            elw.pixel_expansion(pixel, low_limit, high_limit)

    @staticmethod
    @pytest.mark.parametrize(
        ('pixel', 'low_limit', 'high_limit', 'msg'),
        [
            (101, -1, 110, r'range 0 to 255.*-1'),
            (101, 256, 110, r'range 0 to 255.*256'),
            (101, 100, -1, r'range 0 to 255.*-1'),
            (101, 100, 256, r'range 0 to 255.*256'),
            # limites inconsistentes
            (101, 110, 110, r'must be strictly less.*received.*110.*110'),
            (101, 111, 110, r'must be strictly less.*received.*111.*110'),
        ],
    )
    def test_pixel_expansion_raise_value_error(pixel, low_limit, high_limit, msg):
        with pytest.raises(ValueError, match=msg):
            elw.pixel_expansion(np.uint8(pixel), low_limit, high_limit)


@pytest.mark.parametrize(
    ('pixel', 'T', 'A', 'expected'),
    [
        # Lower bound
        (0, 0, 255, 0),  # pixel == T → returns pixel
        (0, 1, 255, 0),  # pixel < T → returns pixel
        # Upper bound
        (255, 127, 255, 255),  # pixel > T → returns A
        (255, 255, 100, 255),  # pixel == T → returns pixel
        (254, 255, 200, 254),  # pixel < T → returns pixel
        # Intermediate cases
        (128, 127, 255, 255),  # pixel > T → returns A
        (126, 127, 200, 126),  # pixel < T → returns pixel
        (200, 100, 123, 123),  # pixel > T → returns A
    ],
)
def test_thresholding_pixel_accept(pixel, T, A, expected):
    result = elw.pixel_thresholding(pixel, T, A)
    assert result == expected
    assert result.dtype == np.uint8


@pytest.mark.parametrize(
    ('pixel', 'T', 'A'),
    [
        # Invalid pixel values
        (-1, 127, 255),
        (256, 127, 255),
        # Invalid threshold values
        (128, -5, 255),
        (128, 300, 255),
        # Invalid A values
        (128, 127, -10),
        (128, 127, 999),
    ],
)
def test_thresholding_pixel_raise_value_error(pixel, T, A):
    with pytest.raises(ValueError, match='must be in the range'):
        elw.pixel_thresholding(pixel, T, A)


@pytest.mark.parametrize(
    ('pixel', 'expected'),
    [
        (0, 255),  # black becomes white
        (255, 0),  # white becomes black
        (100, 155),  # intermediate value
        (128, 127),  # symmetry around the middle
    ],
)
def test_pixel_digital_negative_accept(pixel, expected):
    """Test that valid pixel values return the correct digital negative."""
    result = elw.pixel_digital_negative(np.uint8(pixel))
    assert result == expected


@pytest.mark.parametrize(
    ('invalid_pixel'),
    [
        -1,  # just below the lower bound
        256,  # just above the upper bound
    ],
)
def test_pixel_digital_negative_raise_value_error(invalid_pixel):
    """Test that out-of-range values raise a ValueError."""
    with pytest.raises(ValueError, match='must be in the range'):
        elw.pixel_digital_negative(invalid_pixel)
