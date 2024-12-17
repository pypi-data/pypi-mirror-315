import cv2
import numpy as np
import pytest

from pycvutils import convert


def test_bgr_to_gray():
    img = np.empty((5, 5, 3), dtype=np.uint8)
    assert convert.bgr_to_gray(img).shape == (5, 5)


def test_gray_to_bgr():
    img = np.empty((5, 5), dtype=np.uint8)
    assert convert.gray_to_bgr(img).shape == (5, 5, 3)


def test_bgr_to_hsv():
    img = np.empty((5, 5, 3), dtype=np.uint8)
    assert convert.bgr_to_hsv(img).shape == (5, 5, 3)


def test_bgr_to_gray_empty():
    img = np.empty((0,), dtype=np.uint8)
    with pytest.raises(cv2.error):
        convert.bgr_to_hsv(img)
