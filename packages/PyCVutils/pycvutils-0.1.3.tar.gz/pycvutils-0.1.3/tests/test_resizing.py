import numpy as np

from pycvutils import resizing


def test_nearest_width_only():
    img = np.empty((2, 3), dtype=np.uint8)
    res = resizing.nearest(img, width=6)
    assert res.shape == (4, 6)


def test_nearest_height_only():
    img = np.empty((2, 3), dtype=np.uint8)
    res = resizing.nearest(img, height=4)
    assert res.shape == (4, 6)


def test_nearest_no_args():
    img = np.empty((3, 3), dtype=np.uint8)
    res = resizing.nearest(img)
    assert (res == img).all()


def test_nearest_empty_both_args():
    img = np.empty((0,), dtype=np.uint8)
    res = resizing.nearest(img, 5, 3)
    assert res is None


def test_nearest_by_ratio_width_only():
    img = np.empty((2, 3), dtype=np.uint8)
    res = resizing.by_ratio.nearest(img, fx=2)
    assert res.shape == (4, 6)


def test_nearest_by_ratio_height_only():
    img = np.empty((2, 3), dtype=np.uint8)
    res = resizing.by_ratio.nearest(img, fy=2)
    assert res.shape == (4, 6)


def test_nearest_by_ratio_no_args():
    img = np.empty((3, 3), dtype=np.uint8)
    res = resizing.by_ratio.nearest(img)
    assert (res == img).all()


def test_nearest_by_ratio_empty_both_args():
    img = np.empty((0,), dtype=np.uint8)
    res = resizing.by_ratio.nearest(img, 5, 3)
    assert res is None
