import cv2
import numpy as np
import numpy.typing as npt


def show_image(img: npt.NDArray[np.uint8], title: str = "Show_image") -> None:
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
