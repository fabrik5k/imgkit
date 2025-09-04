import pytest
from beartype.roar import BeartypeCallHintParamViolation

import pictokit.transformations as tfm


class TestExpansaoDePixel:
    @staticmethod
    @pytest.mark.parametrize(
        ("pixel", "limite_L", "limite_H", "resultado_esperado"),
        [
            (99, 100, 110, 99),
            (100, 100, 110, 100),
            (101, 100, 110, 25),
            (109, 100, 110, 229),
            (110, 100, 110, 110),
            (111, 100, 110, 111),
            (0, 0, 255, 0),
            (255, 0, 255, 255),
        ]
    )
    def test_expansao_de_pixel_accept(pixel, limite_L, limite_H, resultado_esperado):
        resultado = tfm.expansao_de_pixel(pixel, limite_L, limite_H)
        assert resultado_esperado == resultado

    @staticmethod
    @pytest.mark.parametrize(
        ("pixel", "limite_L", "limite_H"),
        [
            ("99", 100, 110),
            (100, 100.0, 110),
            (['101'], 100, 110),
            (109, 100, [110]),
        ]
    )
    def test_expansao_de_pixel_raise_type_error(pixel, limite_L, limite_H):
        with pytest.raises(BeartypeCallHintParamViolation):
            tfm.expansao_de_pixel(pixel, limite_L, limite_H)

    @staticmethod
    @pytest.mark.parametrize(
        ("pixel", "limite_L", "limite_H", "msg"),
        [
            (-1, 100, 110, r"range 0 to 255.*-1"),
            (256, 100, 110, r"range 0 to 255.*256"),

            (101, -1, 110, r"range 0 to 255.*-1"),
            (101, 256, 110, r"range 0 to 255.*256"),

            (101, 100, -1, r"range 0 to 255.*-1"),
            (101, 100, 256, r"range 0 to 255.*256"),

            # limites inconsistentes
            (101, 110, 110, r"must be strictly less.*received.*110.*110"),
            (101, 111, 110, r"must be strictly less.*received.*111.*110"),
        ]
    )
    def test_expansao_de_pixel_raise_value_error(pixel, limite_L, limite_H, msg):
        with pytest.raises(ValueError, match=msg):
            tfm.expansao_de_pixel(pixel, limite_L, limite_H)
