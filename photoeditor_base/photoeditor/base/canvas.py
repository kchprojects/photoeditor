from PySide6.QtWidgets import QGraphicsView,QGraphicsScene,QGraphicsPixmapItem
from PySide6.QtGui import QImage,QPixmap,Qt
from photoeditor.base.geometry import Point

class ClickablePixmap(QGraphicsPixmapItem):
    def __init__(self,*args,**kwargs):
        super().__init__(QPixmap(*args,**kwargs))
        self.setAcceptHoverEvents(True)
    
    def set_tool(self,tool):
        self.tool = tool
    
    def mouseMoveEvent(self, event) -> None:
        if self.tool is None:
            return
        self.tool.on_mouse_move(Point.from_QPoint(event.pos()))

    def mousePressEvent(self,event):
        if self.tool is None:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.tool.on_leftclick(Point.from_QPoint(event.pos()))
    
    def mouseReleaseEvent(self,event):
        if self.tool is None:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.tool.on_leftclick_release(Point.from_QPoint(event.pos()))
            
    
class Canvas(QGraphicsView):
    def __init__(self,parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene()
        self.setScene(self._scene)
        self.curr_zoom = 1
        self.current_image = None
        self.tool = None 
        self.pix = ClickablePixmap()
        self.scene().addItem(self.pix)
           
    def set_tool(self,tool):
        if self.tool is not None:
            self._scene.removeItem(self.tool)
        self.tool = tool
        if self.tool is not None:
            self._scene.addItem(tool)
        self.update_image()
        
    def set_image(self,image):
        self.scene().removeItem(self.pix)
        self.current_image = image
        qim = None
        if image is None:
            self.pix = ClickablePixmap()
            self.scene().addItem(self.pix)       
            return 
        if len(image.shape) == 2:
            qim = QImage(image, image.shape[1],\
                                        image.shape[0], image.shape[1],QImage.Format_Grayscale8)
        elif len(image.shape) == 3 and image.shape[2] == 3:
            qim = QImage(image, image.shape[1],\
                                        image.shape[0], image.shape[1] * 3,QImage.Format_BGR888)
        else:
            self.scene().addPixmap(QPixmap())
            self.current_image = None
            raise ValueError("Unsupported image")
        self.pix = ClickablePixmap(qim)
        self.pix.set_tool(self.tool)
        self.scene().addItem(self.pix)

    def get_current_image(self):
        return self.current_image
    
    def update_image(self):
        self.set_image(self.current_image)
    
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