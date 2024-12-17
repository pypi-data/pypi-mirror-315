import numpy as np

from pycvutils.threshold import binary, inv_binary, inv_otsu, otsu


def test_binary_whole_black_thr_125():
    img = np.zeros((5, 5), dtype=np.uint8)
    res = binary(img, 125)
    assert (res == img).all()


def test_binary_whole_black_eq_thr():
    img = np.zeros((5, 5), dtype=np.uint8)
    res = binary(img, int(img.min()))
    assert (res == img).all()


def test_binary_whole_white_thr_125():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    res = binary(img, 125)
    assert (res == img).all()


def test_binary_whole_white_eq_thr():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    res = binary(img, int(img.max()))
    assert (res != img).all()


def test_binary_empty():
    img = np.empty((0,), dtype=np.uint8)
    res = binary(img, 125)
    assert res is None


def test_inv_binary_whole_black_thr_125():
    img = np.zeros((5, 5), dtype=np.uint8)
    res = inv_binary(img, 125)
    assert (res != img).all()


def test_inv_binary_whole_black_eq_thr():
    img = np.zeros((5, 5), dtype=np.uint8)
    res = inv_binary(img, int(img.min()))
    assert (res != img).all()


def test_inv_binary_whole_white_thr_125():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    res = inv_binary(img, 125)
    assert (res != img).all()


def test_inv_binary_whole_white_eq_thr():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    res = inv_binary(img, int(img.max()))
    assert (res == img).all()


def test_inv_binary_empty():
    img = np.empty((0,), dtype=np.uint8)
    res = inv_binary(img, 125)
    assert res is None


def test_inv_otsu_whole_black():
    img = np.zeros((5, 5), dtype=np.uint8)
    res = inv_otsu(img)
    assert (res != img).all()


def test_inv_otsu_whole_white():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    res = inv_otsu(img)
    assert (res != img).all()


def test_inv_otsu_empty():
    img = np.empty((0,), dtype=np.uint8)
    res = inv_otsu(img)
    assert res is None


def test_otsu_whole_black():
    img = np.zeros((5, 5), dtype=np.uint8)
    res = otsu(img)
    assert (res == img).all()


def test_otsu_whole_white():
    img = np.full((5, 5), fill_value=255, dtype=np.uint8)
    res = otsu(img)
    assert (res == img).all()


def test_otsu_empty():
    img = np.empty((0,), dtype=np.uint8)
    res = otsu(img)
    assert res is None
