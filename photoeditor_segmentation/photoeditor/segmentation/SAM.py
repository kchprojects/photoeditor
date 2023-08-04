
#%%
from typing import Any
from segment_anything import SamPredictor, sam_model_registry,SamAutomaticMaskGenerator
from photoeditor.base.filter import SegmentationFilter
import cv2
import matplotlib.pyplot as plt
import numpy as np
from photoeditor.base.selection import UiRectangleSelection

class SamModel:
    checkpoint = "/home/kch/libs/segment-anything/models/sam_vit_h_4b8939.pth"
    model_type = "default"
    __instance = None
    
    @staticmethod
    def get_instance():
        if SamModel.__instance is None:
            SamModel.__instance = sam_model_registry[SamModel.model_type](checkpoint=SamModel.checkpoint)
        
        return SamModel.__instance
SamModel.get_instance()

class SAMMaskPredictor(SegmentationFilter):
    def __init__(self):
        super().__init__()
        self._predictor = SamPredictor(SamModel.get_instance())
        
    def __call__(self, img, selection=None) -> Any:
        self._predictor.set_image(img)
        if selection is None:
            masks, _, _ = self._predictor.predict()
            return masks[-1,:,:]
        if isinstance(selection,UiRectangleSelection):
            rect = selection.get_rect()
            if rect is not None:
                masks, _, _ = self._predictor.predict(box=np.asarray(rect))
                return masks[-1,:,:]
        return None