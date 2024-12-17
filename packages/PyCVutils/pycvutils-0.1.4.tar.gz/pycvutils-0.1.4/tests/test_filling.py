import numpy as np
import pytest

from pycvutils.filling import (
    brighten_areas_near_borders,
    darken_areas_near_borders,
    flood_fill_binary,
)


def test_flood_fill_binary_whole_black():
    img = np.zeros((5, 5), dtype=np.uint8)
    assert (flood_fill_binary(img, (2, 2)) == np.full_like(img, fill_value=255)).all()


def test_flood_fill_binary_whole_white():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    assert (flood_fill_binary(img, (2, 2)) == np.zeros_like(img)).all()


def test_flood_fill_binary_white_dot_on_point():
    img = np.zeros((5, 5), dtype=np.uint8)
    img[2, 2] = 255
    assert (flood_fill_binary(img, (2, 2)) == np.zeros_like(img)).all()


def test_flood_fill_binary_black_dot_not_on_point():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    img[2, 2] = 0
    assert (flood_fill_binary(img, (1, 1)) == np.zeros_like(img)).all()


def test_flood_fill_binary_gray():
    img = np.empty((5, 5), dtype=np.uint8)
    img[2, 2] = 125

    with pytest.raises(ValueError, match="non-binary"):
        flood_fill_binary(img, (2, 2))


def test_flood_fill_binary_empty():
    img = np.empty((0,), dtype=np.uint8)
    assert (flood_fill_binary(img, (2, 2)) == img).all()


def test_darken_areas_near_borders_whole_black():
    img = np.zeros((5, 5), dtype=np.uint8)
    assert (darken_areas_near_borders(img) == img).all()


def test_darken_areas_near_borders_whole_white():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    assert (darken_areas_near_borders(img) == np.zeros_like(img)).all()


def test_darken_areas_near_borders_gray():
    img = np.empty((5, 5), dtype=np.uint8)
    img[2, 2] = 125
    with pytest.raises(ValueError, match="non-binary"):
        darken_areas_near_borders(img)


def test_darken_areas_near_borders_empty():
    img = np.empty((0,), dtype=np.uint8)
    assert (darken_areas_near_borders(img) == img).all()


def test_brighten_areas_near_borders_whole_black():
    img = np.zeros((5, 5), dtype=np.uint8)
    assert (brighten_areas_near_borders(img) == np.full_like(img, fill_value=255)).all()


def test_brighten_areas_near_borders_whole_white():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    assert (brighten_areas_near_borders(img) == img).all()


def test_brighten_areas_near_borders_gray():
    img = np.empty((5, 5), dtype=np.uint8)
    img[2, 2] = 125
    with pytest.raises(ValueError, match="non-binary"):
        brighten_areas_near_borders(img)


def test_brighten_areas_near_borders_empty():
    img = np.empty((0,), dtype=np.uint8)
    assert (brighten_areas_near_borders(img) == img).all()
