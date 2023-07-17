from PySide6.QtWidgets import QGraphicsView,QGraphicsScene
from PySide6.QtGui import QImage,QPixmap

class Canvas(QGraphicsView):
    def __init__(self,parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene()
        self.setScene(self._scene)
        self.curr_zoom = 1
        self.current_image = None
        
    def set_image(self,image):
        qim = None
        if len(image.shape) == 2:
            qim = QImage(image, image.shape[1],\
                                        image.shape[0], image.shape[1],QImage.Format_Grayscale8)
        elif len(image.shape) == 3 and image.shape[2] == 3:
            qim = QImage(image, image.shape[1],\
                                        image.shape[0], image.shape[1] * 3,QImage.Format_BGR888)
        else:
            raise ValueError("Unsupported image")
        self.current_image = image
        pix = QPixmap(qim)
        self.scene().addPixmap(pix)

    def get_current_image(self):
        return self.current_image
    
    def mouseDoubleClickEvent(self, event) -> None:
        self.reset_scale()
        return super().mouseDoubleClickEvent(event)
    
    def reset_scale(self):
        self.scale(1/self.curr_zoom,1/self.curr_zoom)
        self.curr_zoom = 1
        
    def wheelEvent(self, event):
        """
        Zoom in or out of the view.
        """
        zoomInFactor = 1.1
        zoomOutFactor = 1 / zoomInFactor
        ev_pos = event.position().toPoint()
        # Save the scene pos
        oldPos = self.mapToScene(ev_pos)

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)
        self.curr_zoom *= zoomFactor
        # Get the new position
        newPos = self.mapToScene(ev_pos)

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())