from collections.abc import Callable

import cv2
import numpy as np
import numpy.typing as npt

from pycvutils import resizing


def _match_template_wrapper(method: int) -> Callable:
    def _match_template(
        img: npt.NDArray[np.uint8],
        template: npt.NDArray[np.uint8],
        mask: npt.NDArray[np.uint8] | None = None,
    ) -> npt.NDArray[np.uint8]:
        return cv2.matchTemplate(img, template, mask=mask, method=method)

    return _match_template


ccoeff_norm = _match_template_wrapper(cv2.TM_CCOEFF_NORMED)
ccoeff = _match_template_wrapper(cv2.TM_CCOEFF)
ccorr_norm = _match_template_wrapper(cv2.TM_CCORR_NORMED)
ccorr = _match_template_wrapper(cv2.TM_CCORR)
sqdiff_norm = _match_template_wrapper(cv2.TM_SQDIFF_NORMED)
sqdiff = _match_template_wrapper(cv2.TM_SQDIFF)


def compare_with_crop(
    img: npt.NDArray[np.uint8],
    template: npt.NDArray[np.uint8],
    crop_ratio: float = 0.1,
) -> float | None:
    """Use CCOEFF_NORMED matching after center cropping template by some ratio.

    Returns:
        None: if 'img' or 'template' is empty numpy array
        float: for any not empty numpy image array

    """
    if img.size == 0 or template.size == 0:
        return None
    h, w, *_ = template.shape
    h_gap = int(crop_ratio * h) + 1
    w_gap = int(crop_ratio * w) + 1
    template = template[
        h_gap : h - h_gap,
        w_gap : w - w_gap,
    ]

    result = ccoeff_norm(img, template)
    return float(result.max())


def compare_one_to_one(img: npt.NDArray[np.uint8], template: npt.NDArray[np.uint8]) -> float | None:
    """Use CCOEFF_NORMED matching after resizing template to 'img' size.

    Returns:
        None: if 'img' or 'template' is empty numpy array
        float: for any not empty numpy image array

    """
    if img.size == 0 or template.size == 0:
        return None

    if img.shape != template.shape:
        h, w, *_ = img.shape
        template = resizing.nearest(template, width=w, height=h)

    result = ccoeff_norm(img, template)
    return float(result.max())
