from typing import Any
import cv2
from photoeditor.base.filter import Filter

class ToGrayscale(Filter):
    def __call__(self,img,selection=None):
        if img is None or len(img.shape) == 2:
            return img
        if len(img.shape) == 3 and img.shape[2] == 3:
            return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

class Invert(Filter):
    def __call__(self,img,selection=None):
        if img is None:
            return img
        if len(img.shape) == 2 or (len(img.shape) == 3 and img.shape[2] == 3):
            return 255-img