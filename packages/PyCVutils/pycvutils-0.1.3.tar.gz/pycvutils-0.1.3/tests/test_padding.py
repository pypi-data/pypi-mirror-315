import numpy as np

from pycvutils import padding


def test_equal_empty_one_value():
    img = np.empty((0,), dtype=np.uint8)
    res = padding.equal(img, 0, 1)
    assert res.shape == (2, 3)


def test_equal_empty_three_value():
    img = np.empty((0,), dtype=np.uint8)
    res = padding.equal(img, (0, 0, 0), 1)
    assert res.shape == (2, 3)


def test_equal_1x1():
    img = np.empty((1, 1), dtype=np.uint8)
    res = padding.equal(img, 0, 1)
    assert res.shape == (3, 3)
    assert (res[0] == 0).all()
    assert (res[-1] == 0).all()
    assert (res[:, 0] == 0).all()
    assert (res[:, -1] == 0).all()


def test_equal_1_channel_3_values():
    img = np.empty((1, 1), dtype=np.uint8)
    res = padding.equal(img, (0, 0, 0), 1)
    assert res.shape == (3, 3)


def test_equal_3_channels_1_value():
    img = np.empty((1, 1, 3), dtype=np.uint8)
    res = padding.equal(img, 0, 1)
    assert res.shape == (3, 3, 3)
    assert (res[0] == 0).all()
    assert (res[-1] == 0).all()
    assert (res[:, 0] == 0).all()
    assert (res[:, -1] == 0).all()


def test_unequal_empty_one_value():
    img = np.empty((0,), dtype=np.uint8)
    res = padding.unequal(img, 0, top=1, right=1)
    assert res.shape == (1, 2)


def test_unequal_empty_three_value():
    img = np.empty((0,), dtype=np.uint8)
    res = padding.unequal(img, (0, 0, 0), top=1, right=1)
    assert res.shape == (1, 2)


def test_unequal_1x1():
    img = np.empty((1, 1), dtype=np.uint8)
    res = padding.unequal(img, 0, top=1, right=1)
    assert res.shape == (2, 2)
    assert (res[0] == 0).all()
    assert (res[:, -1] == 0).all()


def test_unequal_1_channel_3_values():
    img = np.empty((1, 1), dtype=np.uint8)
    res = padding.unequal(img, (0, 0, 0), top=1, right=1)
    assert res.shape == (2, 2)


def test_unequal_3_channels_1_value():
    img = np.empty((1, 1, 3), dtype=np.uint8)
    res = padding.unequal(img, 0, top=1, right=1)
    assert res.shape == (2, 2, 3)
    assert (res[0] == 0).all()
    assert (res[:, -1] == 0).all()
