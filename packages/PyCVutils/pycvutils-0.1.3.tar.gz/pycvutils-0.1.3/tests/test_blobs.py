import numpy as np

from pycvutils.blobs import get_all_borders, get_bright_rect


def test_get_bright_rect_empty_image():
    img = np.empty((0,), dtype=np.uint8)
    assert get_bright_rect(img) is None


def test_get_bright_rect_whole_black():
    img = np.zeros((5, 5), dtype=np.uint8)
    assert get_bright_rect(img) is None


def test_get_bright_rect_whole_white():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    assert get_bright_rect(img) == (0, 0, 5, 5)


def test_get_bright_rect_white_dot():
    img = np.zeros((5, 5), dtype=np.uint8)
    img[2, 2] = 255
    assert get_bright_rect(img) == (2, 2, 3, 3)


def test_get_bright_rect_bool():
    img = np.zeros((5, 5), dtype=np.uint8)
    img[2, 2] = 255
    img = img > 0
    assert get_bright_rect(img) == (2, 2, 3, 3)


def test_get_bright_rect_non_gray():
    img = np.empty((5, 5, 3), dtype=np.uint8)
    assert get_bright_rect(img) is not None


def test_get_all_borders_whole_black():
    array = np.empty((5,), dtype=np.uint8) < 0
    assert not tuple(get_all_borders(array))


def test_get_all_borders_whole_white():
    array = np.empty((5,), dtype=np.uint8) >= 0
    assert tuple(get_all_borders(array)) == ((0, 5),)


def test_get_all_borders_empty():
    array = np.empty((0,), dtype=np.bool_)
    assert not tuple(get_all_borders(array))
