from photoeditor.ui.ui_layer import Ui_Layer
from PySide6.QtWidgets import QWidget

class UiLayer(QWidget):
    def __init__(self,layer,parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Layer()
        self.ui.setupUi(self)
        self._layer = layer
    
    def apply(self,img=None,mask=None):
        new_img = self._layer.apply(img,mask)
        self.ui.preview.set_image(new_img)
        return new_img
    
        
        
    