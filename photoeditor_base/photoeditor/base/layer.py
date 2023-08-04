from abc import ABC,abstractmethod
import cv2
import numpy as np

class Layer(ABC):
    def __init__(self):
        self._is_enabled = True 
        self._alpha = 1.0 
    
    def apply(self,img=None,mask=None):
        if self.is_enabled():
            if img is None:
                return self._apply_implementation(img,mask)
            computed = self._apply_implementation(img,mask)
            if computed is None:
                return None
            if computed.dtype == bool:
                computed = (computed*255).astype(np.uint8)
            if len(computed.shape) == 2 and len(img.shape) == 3:
                computed = cv2.cvtColor(computed,cv2.COLOR_GRAY2BGR)
            elif len(img.shape) == 2 and len(computed.shape) == 3:
                img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
            return (self.alpha() * computed + img*(1 - self.alpha())).astype(img.dtype)
        return img
    
    @abstractmethod
    def _apply_implementation(self,img=None,mask=None):
        return img

    def enable(self) -> None:
        self.set_enabled(True)
    
    def disable(self)-> None:
        self.set_enabled(False)
    
    def set_enable(self,value:bool) -> None:
        self._is_enabled = value
    
    def is_enabled(self) -> bool:
        return self._is_enabled        
    
    def set_alpha(self,alpha:float) -> None:
        if  0 <= alpha <= 1:
            self._alpha = alpha
        else:
            raise ValueError("Alpha can be only float from interval 0-1")
        
    def alpha(self)->float:
        return self._alpha
    
    def tag(self)->str:
        return self.__class__.__name__

class FilterLayer(Layer):
    
    def __init__(self,filter):
        super().__init__()
        self._filter = filter
    
    def _apply_implementation(self,img=None,mask=None):
        if self._filter is not None:
            return self._filter(img,mask)
        return img
    
    def tag(self)->str:
        return self._filter.__class__.__name__

class ImageLayer(Layer):
    
    def __init__(self,img):
        super().__init__()
        self._img = img
    
    def _apply_implementation(self,img=None,mask=None):
        return self._img
    