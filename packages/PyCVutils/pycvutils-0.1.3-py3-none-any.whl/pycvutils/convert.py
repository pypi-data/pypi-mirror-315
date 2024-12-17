# ideas from: https://github.com/gorodion/pycv/blob/main/cv3/color_spaces.py
from collections.abc import Callable

import cv2
import numpy as np
import numpy.typing as npt


def _cvt_color_wrapper(code: int) -> Callable:
    def cvt_color(img: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
        """Change color space of image.

        Returns:
            npt.NDArray[np.uint8]: for any numpy image array

        """
        return cv2.cvtColor(img, code=code)

    return cvt_color


rgb_to_bgr = bgr_to_rgb = bgr = rgb = _cvt_color_wrapper(cv2.COLOR_RGB2BGR)
rgba_to_bgra = bgra_to_rgba = bgra = rgba = _cvt_color_wrapper(cv2.COLOR_RGBA2BGRA)
gray_to_bgr = gray_to_rgb = _cvt_color_wrapper(cv2.COLOR_GRAY2RGB)
gray_to_bgra = gray_to_rgba = _cvt_color_wrapper(cv2.COLOR_GRAY2RGBA)
bgr_to_gray = _cvt_color_wrapper(cv2.COLOR_BGR2GRAY)
rgb_to_gray = _cvt_color_wrapper(cv2.COLOR_RGB2GRAY)
bgr_to_hsv = _cvt_color_wrapper(cv2.COLOR_BGR2HSV)
rgb_to_hsv = _cvt_color_wrapper(cv2.COLOR_RGB2HSV)
hsv_to_bgr = _cvt_color_wrapper(cv2.COLOR_HSV2BGR)
hsv_to_rgb = _cvt_color_wrapper(cv2.COLOR_HSV2RGB)
