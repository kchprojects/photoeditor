from typing import Any
import cv2


class Filter:
    def __call__(self, img,selection=None) -> Any:
        return img