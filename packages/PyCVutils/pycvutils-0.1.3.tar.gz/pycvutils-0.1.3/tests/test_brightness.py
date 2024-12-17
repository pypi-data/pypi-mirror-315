import cv2
import numpy as np
import pytest

from pycvutils.brightness import (
    crop_bright_area_and_pad,
    has_any_bright_border,
    has_any_bright_corner,
)


def test_has_any_bright_border_whole_black():
    img = np.zeros((5, 5), dtype=np.uint8)
    assert not has_any_bright_border(img)


def test_has_any_bright_border_whole_white():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    assert has_any_bright_border(img)


def test_has_any_bright_border_bool():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    img = img > 0
    assert has_any_bright_border(img)


def test_has_any_bright_border_non_gray():
    img = np.full((5, 5, 3), fill_value=255, dtype=np.uint8)
    img = img > 0
    assert has_any_bright_border(img)


def test_has_any_bright_border_empty_image():
    img = np.empty((0,), dtype=np.uint8)
    assert has_any_bright_border(img) is None


def test_has_any_bright_corner_whole_black():
    img = np.zeros((5, 5), dtype=np.uint8)
    assert not has_any_bright_corner(img)


def test_has_any_bright_corner_whole_white():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    assert has_any_bright_corner(img)


def test_has_any_bright_corner_bool():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    img = img > 0
    assert has_any_bright_corner(img)


def test_has_any_bright_corner_non_gray():
    img = np.full((5, 5, 3), fill_value=255, dtype=np.uint8)
    img = img > 0
    assert has_any_bright_corner(img)


def test_has_any_bright_corner_empty_image():
    img = np.empty((0,), dtype=np.uint8)
    assert has_any_bright_corner(img) is None


def test_crop_bright_area_and_pad_whole_black():
    img = np.zeros((5, 5), dtype=np.uint8)
    assert crop_bright_area_and_pad(img) is None


def test_crop_bright_area_and_pad_whole_white():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    assert (
        crop_bright_area_and_pad(img, pad_size=1) == np.full((7, 7), fill_value=255, dtype=np.uint8)
    ).all()


def test_crop_bright_area_and_pad_whole_black_inv():
    img = np.zeros((5, 5), dtype=np.uint8)
    assert (
        crop_bright_area_and_pad(img, pad_size=1, inverse=True) == np.zeros((7, 7), dtype=np.uint8)
    ).all()


def test_crop_bright_area_and_pad_bool():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    img = img > 0
    with pytest.raises(cv2.error):
        crop_bright_area_and_pad(img, pad_size=1)


def test_crop_bright_area_and_pad_non_gray():
    img = np.full((5, 5, 3), fill_value=255, dtype=np.uint8)
    assert (
        crop_bright_area_and_pad(img, pad_size=1)
        == np.full((7, 7, 3), fill_value=255, dtype=np.uint8)
    ).all()


def test_crop_bright_area_and_pad_empty():
    img = np.empty((0,), dtype=np.uint8)
    assert (crop_bright_area_and_pad(img, pad_size=1) == img).all()
