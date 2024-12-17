from collections.abc import Callable

import cv2
import numpy as np
import numpy.typing as npt


def _resize_by_ratio_wrapper(interpolation: int) -> Callable:
    def _resize(
        img: npt.NDArray[np.uint8],
        fx: float | None = None,
        fy: float | None = None,
    ) -> npt.NDArray[np.uint8] | None:
        if img.size == 0:
            return None

        if fx is None and fy is None:
            return img
        if fx is None:
            fx = fy
        if fy is None:
            fy = fx

        return cv2.resize(img, dsize=None, fx=fx, fy=fy, interpolation=interpolation)

    return _resize


nearest = _resize_by_ratio_wrapper(cv2.INTER_NEAREST)
area = _resize_by_ratio_wrapper(cv2.INTER_AREA)
linear = _resize_by_ratio_wrapper(cv2.INTER_LINEAR)
cubic = _resize_by_ratio_wrapper(cv2.INTER_CUBIC)
lanczos4 = _resize_by_ratio_wrapper(cv2.INTER_LANCZOS4)
