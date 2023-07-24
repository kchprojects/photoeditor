from functools import partial
from PySide6.QtWidgets import QMainWindow,QFileDialog,QVBoxLayout,QPushButton,QSpacerItem,QSizePolicy
from PySide6.QtGui import QAction,QKeySequence
from photoeditor.filter_factory import get_all_filters
from photoeditor.ui.ui_diagram import Ui_MainWindow
import cv2

from photoeditor.base.layer import FilterLayer,ImageLayer
from photoeditor.UiLayer import UiLayer

class Diagram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_actions()
        self.setup_filters()
        self.setup_layers()
        
    def setup_actions(self):
        self.open_action = QAction("Open image")
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.triggered.connect(self.open_image)
        
        self.save_action = QAction("Save image")
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self.save_image)
        
        filemenu = self.ui.menubar.addMenu("File")
        filemenu.addAction(self.open_action)
        filemenu.addAction(self.save_action)
        
    def setup_filters(self):
        self.filters = {}
        self.filter_layout = QVBoxLayout()
        self.ui.filters.setLayout(self.filter_layout)
        for tag,f in get_all_filters().items():
            btn = QPushButton(tag)
            curr_filter = f()
            self.filters[tag] = curr_filter
            btn.clicked.connect(partial(self.add_filter_layer,curr_filter))
            self.filter_layout.addWidget(btn)
        self.filter_layout.addSpacerItem(QSpacerItem(0,10, QSizePolicy.Expanding, QSizePolicy.Expanding))
    
    def setup_layers(self):
        self.ui.layer_layout.addSpacerItem(QSpacerItem(0,10, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.layers = []
        
    def add_filter_layer(self,f):
        f.show_argument_dialog()
        self.add_layer(FilterLayer(f))
    
    def add_image_layer(self,img):
        self.add_layer(ImageLayer(img))
        
    def add_layer(self,layer):
        if not isinstance(layer,UiLayer):
            layer = UiLayer(layer)
        self._connect_layer(layer)
        self.layers.append(layer)
        self.ui.layer_layout.insertWidget(0,layer)
        self.update_view()
        
    def remove_layer(self,layer):
        self.layers.remove(layer)
        self.ui.layer_layout.removeWidget(layer)
        layer.deleteLater()
        self.update_view()
        
    def _connect_layer(self,layer:UiLayer):
        def enable():
            should_enable = layer.ui.enable_button.text() == "enable"
            layer._layer.set_enable(should_enable)
            if should_enable:
                layer.ui.enable_button.setText("disable")
            else:
                layer.ui.enable_button.setText("enable")
            self.update_view()
        layer.ui.enable_button.clicked.connect(enable)
        
        layer.ui.delete_button.clicked.connect(partial(self.remove_layer,layer))
        
    def update_view(self):
        img = None
        for l in self.layers:
            img = l.apply(img)
        self.ui.canvas.set_image(img)
                
    def save_image(self):
        img = self.ui.canvas.get_current_image()
        if img is None:
            print("No image to save")
        else:
            file,_ = QFileDialog.getSaveFileName(self,"Save image","*.png;*.jpg;*.bmp")
            img = cv2.imwrite(file,img)
    
    def clear_layers(self):
        for i in range(self.ui.layer_layout.count()-1):
            child = self.ui.layer_layout.itemAt(i).widget()
            child.deleteLater()
        self.layers.clear()
    
    def open_image(self):
        file,_ = QFileDialog.getOpenFileName(self,"Save image","*.png;*.jpg;*.bmp")
        img = cv2.imread(file,cv2.IMREAD_UNCHANGED)
        self.clear_layers()
        self.add_image_layer(img)
        
        