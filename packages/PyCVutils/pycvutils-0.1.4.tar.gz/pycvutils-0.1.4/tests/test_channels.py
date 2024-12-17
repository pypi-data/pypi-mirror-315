import numpy as np

from pycvutils.channels import split_view


def test_split_view_3_channels():
    img = np.empty((5, 5, 3))
    assert len(split_view(img)) == 3


def test_split_view_1_channel():
    img = np.empty((5, 5, 1))
    assert len(split_view(img)) == 1


def test_split_view_2_dims():
    img = np.empty((5, 5))
    assert len(split_view(img)) == 1


def test_split_view_empty():
    img = np.empty((0,))
    assert split_view(img) is None
