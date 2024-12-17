import cv2
import numpy as np
import numpy.typing as npt

from pycvutils import padding


def flood_fill_binary(binary: npt.NDArray[np.uint8 | bool], x_y: tuple[int, int]) -> npt.NDArray[np.uint8]:
    """cv2.floodFill wrapper only for binary images.

    Fill value is calculating automatically

    Returns:
        npt.NDArray[np.uint8 | bool]: for any numpy image array

    Raises:
        ValueError: if image is non-binary

    """
    binary = binary.astype(np.uint8)

    light_color = 255
    black_color = 0
    black_part = (binary == black_color)
    if not (black_part | (binary == light_color)).all():
        light_color = 1
        if not (black_part | (binary == light_color)).all():
            err = "You passed non-binary image. Allowed values are {0, 1} or {0, 255}"
            raise ValueError(err)
    x, y = x_y
    try:
        fill_value = light_color if int(binary[y, x]) == black_color else black_color
    except IndexError:
        return binary

    flags = 4 | (fill_value << 8) | cv2.FLOODFILL_FIXED_RANGE
    binary = cv2.floodFill(
        binary,
        mask=None,
        seedPoint=(x, y),
        newVal=fill_value,
        loDiff=0,
        upDiff=0,
        flags=flags,
    )[1]
    return binary


def darken_areas_near_borders(binary: npt.NDArray[np.uint8 | np.bool_]) -> npt.NDArray[np.uint8]:
    """Remove white blobs touching image borders.

    Returns:
        npt.NDArray[np.uint8]: for any numpy image array

    """
    binary = binary.astype(np.uint8)
    try:
        max_value = int(binary.max())
    except ValueError:
        return binary
    if max_value == 0:
        return binary
    binary = padding.equal(binary, size=1, value=max_value)
    binary = flood_fill_binary(binary, (0, 0))
    binary = binary[1:-1, 1:-1]

    return binary


def brighten_areas_near_borders(binary: npt.NDArray[np.uint8 | np.bool_]) -> npt.NDArray[np.uint8]:
    """Remove black blobs touching image borders.

    Returns:
        npt.NDArray[np.uint8]: for any numpy image array

    """
    binary = binary.astype(np.uint8)

    binary = padding.equal(binary, size=1, value=0)
    binary = flood_fill_binary(binary, (0, 0))
    binary = binary[1:-1, 1:-1]

    return binary
