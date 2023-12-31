from typing import Any
import cv2
from abc import ABC,abstractmethod

from PySide6.QtWidgets import QHBoxLayout,QLabel,QWidget,QDoubleSpinBox,QSpinBox,QDialog,QVBoxLayout,QPushButton

class Argument(ABC):
    def __init__(self,label,value):
        self._value = value
        self._label=label
        self._widget = None
    
    def get(self):
        return self._value
    
    def set(self,value):
        self._value = value
    
    @abstractmethod
    def get_widget(self):
        self._widget = QWidget()
        layout=QHBoxLayout()
        self._widget.setLayout(layout)
        layout.addWidget(QLabel(self._label))
        layout.addWidget(QLabel(str(self._value)))
        return self._widget

class IntArgument(Argument):
    def __init__(self,label,value,step=1,min_val=None,max_val=None):
        super().__init__(label,value)
        self._step = step
        self._min_val = min_val
        self._max_val = max_val
    
    def get_widget(self):
        self._widget = QWidget()
        layout=QHBoxLayout()
        self._widget.setLayout(layout)
        layout.addWidget(QLabel(self._label))
        spinbox = QSpinBox()
        spinbox.setSingleStep(self._step)
        spinbox.valueChanged.connect(self.set)
        if self._min_val is not None:
            spinbox.setMinimum(self._min_val)
        if self._max_val is not None:
            spinbox.setMaximum(self._max_val)
        layout.addWidget(spinbox)
        return self._widget

class FloatArgument(Argument):
    def __init__(self,label,value,step=0.1,min_val=None,max_val=None):
        super().__init__(label,value)
        self._step = step
        self._min_val = min_val
        self._max_val = max_val
    
    def get_widget(self):
        self._widget = QWidget()
        layout=QHBoxLayout()
        self._widget.setLayout(layout)
        layout.addWidget(QLabel(self._label))
        spinbox = QDoubleSpinBox()
        spinbox.setSingleStep(self._step)
        spinbox.valueChanged.connect(self.set)
        if self._min_val is not None:
            spinbox.setMinimum(self._min_val)
        if self._max_val is not None:
            spinbox.setMaximum(self._max_val)
        layout.addWidget(spinbox)
        return self._widget
    
class Filter(ABC):
    @abstractmethod
    def __call__(self, img,selection=None) -> Any:
        return img

    def show_argument_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle(self.__class__.__name__)
        layout = self.get_attrib_layout()
        if layout.count() == 0:
            return
        button = QPushButton("OK")
        button.clicked.connect(dialog.close)
        layout.addWidget(button)
        dialog.setLayout(layout)        
        dialog.exec()
    
    def get_attrib_layout(self):
        layout = QVBoxLayout()
        for attr in [self.__getattribute__(v) for v in vars(self)]:
            if isinstance(attr,Argument):
                layout.addWidget(attr.get_widget())
        return layout
class SegmentationFilter(Filter,ABC):
    pass
    
class CombinedFilter(Filter):
    def __init__(self,filters:list[Filter]):
        super().__init__()
        self._filters = filters
    
    def get_attrib_layout(self):
        #TODO: decide if this should return only empty layout or not
        layout = QVBoxLayout()
        for f in self._filters:
            layout.addLayout(f.get_attrib_layout())
        return layout

    
