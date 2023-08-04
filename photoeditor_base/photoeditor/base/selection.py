from abc import ABC,abstractmethod
from typing import Optional

from photoeditor.base.geometry import Point
from photoeditor_base.photoeditor.base.geometry import Point

try:
    from PySide6.QtGui import Qt,QPainter
    from PySide6.QtWidgets import QGraphicsRectItem 
    HAS_QT = True
except:
    HAS_QT = False

class Selection():
    
    def on_rightclick(self,coords:Point):
        pass

    def on_leftclick(self, coords:Point):
        pass

    def on_rightclick_release(self,coords:Point):
        pass

    def on_leftclick_release(self, coords:Point):
        pass

    def on_mouse_move(self, coords:Point):
        pass
    
    def wheel(self, delta):
        pass

class RectangleSelection(Selection):
    def __init__(self,update_callback=None):
        Selection.__init__(self)
        self._left_top: Optional[Point] = None
        self._right_bottom: Optional[Point] = None
        self._update = update_callback 
        self._is_moving = False
        
    def set_update_callback(self,update_callback):
        self._update = update_callback()
    
    def set_left_top(self,val:Point):
        self._left_top = val
    
    def set_right_bottom(self,val:Point):
        self._right_bottom = val
        if self._update is not None:
            self._update()
        
    def on_leftclick(self, coords: Point): 
        self.set_left_top(coords)
        self.set_right_bottom(None)
        self._is_moving = True
    
    def on_leftclick_release(self, coords: Point):
        if self._is_moving and self._left_top is not None:
            self.set_right_bottom(coords)
            self._is_moving = False
    
    def on_mouse_move(self, coords: Point):
        if self._is_moving and self._left_top is not None:
            self.set_right_bottom(coords)
        
    def get_rect(self):
        if self._left_top is not None and self._right_bottom is not None:
            ax,ay = self._left_top.split()
            bx,by = self._right_bottom.split()
            if ax > bx:
                ax,bx = bx,ax
            if ay > by:
                ay,by = by,ay
            lt = Point(ax,ay)
            rb= Point(bx,by)
            return [*lt.split(), *(rb - lt).split()]
        return None

if HAS_QT:
    class UiRectangleSelection(QGraphicsRectItem,RectangleSelection):
        def __init__(self,parent=None):
            QGraphicsRectItem.__init__(self,parent)
            RectangleSelection.__init__(self,self.on_update)
            self.setZValue(10)
            self.hide()
        
        def paint(self, painter,option, widget) -> None:
            p = painter.pen()
            p.setWidth(5)
            p.setColor(Qt.blue)
            painter.setPen(p)
            painter.drawRect(self.rect())
            
        def on_update(self):
            rect = self.get_rect()                
            if rect is not None:
                self.setRect(*rect)
                self.show()
            else:
                self.hide()
        