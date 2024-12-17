from collections.abc import Iterator

import numpy as np
import numpy.typing as npt

from .coords import CoordsTuple


def get_bright_rect(binary: npt.NDArray[np.uint8 | np.bool_]) -> CoordsTuple | None:
    """Return rect around all bright (non-zero) blobs.

    Returns:
        None: if there is no bright blobs
        x1_y1_x2_y2: coords of a single rect around every blob

    """
    color_img_dims = 3
    if binary.ndim == color_img_dims:
        binary = binary.any(axis=2)
    nonzeros = binary.nonzero()
    try:
        y1, x1 = np.minimum.reduce(nonzeros, axis=1)
        y2, x2 = np.maximum.reduce(nonzeros, axis=1)
    except ValueError:
        return None
    return CoordsTuple(x1, y1, x2 + 1, y2 + 1)


def get_all_borders(bool_array: npt.NDArray[np.bool_]) -> Iterator[tuple[int, int]]:
    """Return the coordinates for each blob in 1-dim array.

    Yields:
        tuple[int, int]: for each bright blob in the array

    """
    a = np.r_[False, bool_array, False]
    start = np.r_[False, ~a[:-1] & a[1:]]
    end = np.r_[a[:-1] & ~a[1:], False]
    for x1, x2 in zip(np.nonzero(start)[0] - 1, np.nonzero(end)[0], strict=False):
        if x1 + 1 == x2:
            continue
        yield x1, x2
