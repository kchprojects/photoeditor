from PySide6.QtWidgets import QGraphicsView,QGraphicsScene,QSizePolicy
from PySide6.QtGui import QImage,QPixmap

class ImagePreview(QGraphicsView):
    def __init__(self,parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene()
        self.setScene(self._scene)
        self.curr_zoom = 1
        self.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        
    def set_image(self,image):
        self.current_image = image
        qim = None
        if image is None:
            self.scene().addPixmap(QPixmap())       
            return 
        if len(image.shape) == 2:
            qim = QImage(image, image.shape[1],\
                                        image.shape[0], image.shape[1],QImage.Format_Grayscale8)
        elif len(image.shape) == 3 and image.shape[2] == 3:
            qim = QImage(image, image.shape[1],\
                                        image.shape[0], image.shape[1] * 3,QImage.Format_BGR888)
        else:
            self.scene().addPixmap(QPixmap())
            raise ValueError("Unsupported image")
        pix = QPixmap(qim).scaledToWidth(self.geometry().width())
        self.scene().addPixmap(pix)
    