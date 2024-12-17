from collections.abc import Callable

import cv2
import numpy as np
import numpy.typing as npt


def _resize_wrapper(interpolation: int) -> Callable:
    def _resize(
        img: npt.NDArray[np.uint8],
        width: int | None = None,
        height: int | None = None,
    ) -> npt.NDArray[np.uint8] | None:
        if img.size == 0:
            return None

        h, w, *_ = img.shape
        if width is None and height is None:
            return img
        if width is None:
            width = int(w * (height / h))
        if height is None:
            height = int(h * (width / w))

        return cv2.resize(img, (width, height), interpolation=interpolation)

    return _resize


nearest = _resize_wrapper(cv2.INTER_NEAREST)
area = _resize_wrapper(cv2.INTER_AREA)
linear = _resize_wrapper(cv2.INTER_LINEAR)
cubic = _resize_wrapper(cv2.INTER_CUBIC)
lanczos4 = _resize_wrapper(cv2.INTER_LANCZOS4)
