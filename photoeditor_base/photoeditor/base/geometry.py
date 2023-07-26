from typing import Union,Generic,TypeVar

try:
    HAS_QT = True
    from PySide6.QtCore import QPoint,QPointF
except:
    HAS_QT = False
    

T = TypeVar('T',int,float)

class Point(Generic[T]):
    def __init__(self,x:T,y:T):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


    def __str__(self):
        return f"{self.x},{self.y}"
    
    def __add__(self,other:"Point"):
        return Point(self.x+other.x,self.y+other.y)
    
    def __sub__(self,other:"Point"):
        return Point(self.x-other.x,self.y-other.y)
        
    def split(self):
        return self.x,self.y
    
    if HAS_QT:
        @staticmethod
        def from_QPoint(qpoint:Union[QPoint,QPointF]) -> "Point":
            return Point(qpoint.x(),qpoint.y())

        def to_qpoint(self) -> QPoint:
            return QPoint(int(self.x),int(self.y))