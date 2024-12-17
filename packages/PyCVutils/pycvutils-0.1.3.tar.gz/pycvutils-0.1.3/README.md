# PyCVutils
A bunch of useful wrappers around opencv-python library

### Installation:

`pip install pycvutils`

> before using you should manually install any opencv version you like:
`pip install opencv-python` or `opencv-python-headless` or 
`opencv-contrib-python` or `opencv-contrib-python-headlesss`

### Examples:

Let's work with such binary image:

![face_large.png](docs%2Fimg_samples%2Fface_large.png)

```Python
import cv2
from pycvutils import convert
from pycvutils.blobs import get_bright_rect

face_img = cv2.imread("docs/img_samples/face.png")
assert get_bright_rect(face_img) == (1, 2, 10, 7)

# works with 3 channels arrays and boolean arrays too
face_img = convert.bgr_to_gray(face_img)
assert get_bright_rect(face_img) == (1, 2, 10, 7)
```

```Python
import cv2
from pycvutils.blobs import get_all_borders

face_img = cv2.imread("docs/img_samples/face.png", flags=cv2.IMREAD_GRAYSCALE)
face_img = face_img.any(axis=0)
assert tuple(get_all_borders(face_img)) == ((3, 6), (7, 10))
```

```Python
import cv2
from pycvutils.brightness import crop_bright_area_and_pad

face_img = cv2.imread("docs/img_samples/face.png")
# useful for colored images
assert crop_bright_area_and_pad(face_img, pad_size=5).shape == (15, 19, 3)
```

![face_crop_pad.png](docs%2Fimg_samples%2Fface_crop_pad.png)


```Python
import cv2
from pycvutils.brightness import has_any_bright_border, has_any_bright_corner

face_img = cv2.imread("docs/img_samples/face.png")
# returns True if any border has non-zero pixel
assert not has_any_bright_border(face_img)
# returns True if any corner pixel is non-zero
assert not has_any_bright_corner(face_img)
```

```Python
import cv2
from pycvutils.channels import split_view

face_img = cv2.imread("docs/img_samples/face.png")
# works like cv2.split, but returns views instead of copies
views = split_view(face_img)
assert isinstance(views, tuple)
assert len(views) == 3
assert (views[0].base == face_img).all()  # 'is' doesn't work for some reason
```

```Python
import cv2
from pycvutils.filling import brighten_areas_near_borders, flood_fill_binary

face_img = cv2.imread("docs/img_samples/face.png", flags=cv2.IMREAD_GRAYSCALE)
# wrapper around cv2.floodFill
assert (flood_fill_binary(face_img, x_y=(1, 1)) == 255).all()
# fills with white any black area touching borders of image
assert (brighten_areas_near_borders(face_img) == 255).all()
```

```Python
import cv2
from pycvutils.matching import compare_one_to_one, compare_with_crop

face_img = cv2.imread("docs/img_samples/face.png")
template = face_img[5:-2, 6:-2]

# makes small crop before making comparison
assert compare_with_crop(face_img, template, crop_ratio=0.1) == 1.0
# resize template to size of original img before making comparison
assert compare_one_to_one(face_img, template) != 1.0
```

```Python
import cv2
from pycvutils import padding

face_img = cv2.imread("docs/img_samples/face.png", flags=cv2.IMREAD_GRAYSCALE)

padded = padding.unequal(face_img, value=125, top=2, left=2, right=1)
assert padded.shape[0] == face_img.shape[0] + 2
assert padded.shape[1] == face_img.shape[1] + 3
```

![face_padded.png](docs%2Fimg_samples%2Fface_padded.png)