from typing import Any

import numpy.typing as npt


def split_view(img: npt.NDArray[Any]) -> tuple[npt.NDArray[Any], ...] | None:
    """Split image by channels without making copies.

    Can slow down next processing in comparison to 'cv2.split'

    Returns:
        None: if 'img' is empty image array
        npt.NDArray[Any]: for any not empty numpy image array

    """
    gray_img_dims = 2
    if img.ndim == gray_img_dims:
        return (img.copy(),)
    try:
        return tuple(img[:, :, n] for n in range(img.shape[2]))
    except IndexError:
        return None
