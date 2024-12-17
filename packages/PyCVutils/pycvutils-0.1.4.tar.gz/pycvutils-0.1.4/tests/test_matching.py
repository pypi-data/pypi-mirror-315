import numpy as np

from pycvutils.matching import ccoeff_norm, compare_one_to_one, compare_with_crop


def test_ccoeff_norm():
    img = np.empty((5, 5, 3), dtype=np.uint8)
    tmplt = np.empty((3, 3, 3), dtype=np.uint8)
    res = ccoeff_norm(img, tmplt)
    assert res.shape == (3, 3)
    assert 0 <= res.max() <= 1.0


def test_compare_with_crop_img_size_eq_tmplt_size():
    img = np.empty((5, 5, 3), dtype=np.uint8)
    tmplt = np.empty((5, 5, 3), dtype=np.uint8)
    res = compare_with_crop(img, tmplt)
    assert isinstance(res, float)


def test_compare_with_crop_tmplt_empty():
    img = np.empty((5, 5, 3), dtype=np.uint8)
    tmplt = np.empty((0,), dtype=np.uint8)
    res = compare_with_crop(img, tmplt)
    assert res is None


def test_compare_with_crop_img_empty():
    img = np.empty((0,), dtype=np.uint8)
    tmplt = np.empty((5, 5, 3), dtype=np.uint8)
    res = compare_with_crop(img, tmplt)
    assert res is None


def test_compare_with_crop_img_size_less_tmplt():
    img = np.empty((3, 3, 3), dtype=np.uint8)
    tmplt = np.empty((7, 7, 3), dtype=np.uint8)
    res = compare_with_crop(img, tmplt)
    assert 0.0 <= res <= 1.0


def test_compare_one_to_one_equal():
    img = np.empty((5, 5, 3), dtype=np.uint8)
    tmplt = np.empty((5, 5, 3), dtype=np.uint8)
    res = compare_one_to_one(img, tmplt)
    assert 0.0 <= res <= 1.0


def test_compare_one_to_one_img_empty():
    img = np.empty((0,), dtype=np.uint8)
    tmplt = np.empty((5, 5, 3), dtype=np.uint8)
    res = compare_one_to_one(img, tmplt)
    assert res is None


def test_compare_one_to_one_tmplt_empty():
    img = np.empty((5, 5, 3), dtype=np.uint8)
    tmplt = np.empty((0,), dtype=np.uint8)
    res = compare_one_to_one(img, tmplt)
    assert res is None
