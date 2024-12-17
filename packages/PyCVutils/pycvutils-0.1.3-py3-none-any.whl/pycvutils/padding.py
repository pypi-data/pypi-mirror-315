import cv2
import numpy as np
import numpy.typing as npt


def equal(
    img: npt.NDArray[np.uint8],
    value: int | tuple[int, ...],
    size: int,
) -> npt.NDArray[np.uint8]:
    """Pad each side by equal count of pixels.

    Returns:
        npt.NDArray[np.uint8]: for any numpy image array

    """
    return cv2.copyMakeBorder(
        img,
        top=size,
        bottom=size,
        left=size,
        right=size,
        borderType=cv2.BORDER_CONSTANT,
        value=value,
    )


def unequal(  # noqa: PLR0917, PLR0913
    img: npt.NDArray[np.uint8],
    value: int | tuple[int, ...],
    top: int = 0,
    bottom: int = 0,
    left: int = 0,
    right: int = 0,
) -> npt.NDArray[np.uint8]:
    """Pad each side by different count of pixels.

    Returns:
        npt.NDArray[np.uint8]: for any numpy image array

    """
    return cv2.copyMakeBorder(
        img,
        top=top,
        bottom=bottom,
        left=left,
        right=right,
        borderType=cv2.BORDER_CONSTANT,
        value=value,
    )
