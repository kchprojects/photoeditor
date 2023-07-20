from typing import Any
import cv2
from photoeditor.base.filter import Filter,IntArgument

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
    
class Blurr(Filter):
    
    def __init__(self):
        super().__init__()
        self.kernel_size = IntArgument("kernel size", 11,step=2,min_val=3)
        self.sigma = IntArgument("sigma", 1,step=1,min_val=1)
        
    def __call__(self,img,selection=None):
        return cv2.GaussianBlur(img,(self.kernel_size.get(),)*2,self.sigma.get())