from functools import partial
from PySide6.QtWidgets import QMainWindow,QFileDialog,QVBoxLayout,QPushButton,QSpacerItem,QSizePolicy,QDialog
from PySide6.QtGui import QAction,QKeySequence,QCursor
from PySide6.QtCore import Qt
from photoeditor.filter_factory import get_all_filters
from photoeditor.ui.ui_diagram import Ui_MainWindow
import cv2


from photoeditor.comand_line import ComandLine

from photoeditor.base.layer import FilterLayer,ImageLayer
from photoeditor.base.selection import UiRectangleSelection
from photoeditor.UiLayer import UiLayer

class Diagram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_actions()
        self.setup_filters()
        self.setup_layers()
        self.setup_tools()
    
    def setup_tools(self):
        self.activeTool = None
        self.tool_buttons:list[QPushButton] = []
        
        self.ui.select_rect_button.clicked.connect(partial(self.activate_tool,UiRectangleSelection,self.ui.select_rect_button))
        self.tool_buttons.append(self.ui.select_rect_button)
        
        for b in self.tool_buttons:
            b.setCheckable(True)
            b.setChecked(False)
        
    def activate_tool(self,tool_type,btn:QPushButton):
        if not btn.isChecked():
            self.activeTool = None
            self.ui.canvas.set_tool(None)
            return
        for b in self.tool_buttons:
            if b is not btn:
                b.setChecked(False)
        self.activeTool = tool_type()
        self.ui.canvas.set_tool(self.activeTool)
        
    def setup_actions(self):
        self.open_action = QAction("Open image")
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.triggered.connect(self.open_image)
        
        self.save_action = QAction("Save image")
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self.save_image)
        
        self.prompt_edit = QAction("Prompt action")
        self.prompt_edit.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_Space))
        self.prompt_edit.triggered.connect(self.prompt_action)
        
        filemenu = self.ui.menubar.addMenu("File")
        filemenu.addAction(self.open_action)
        filemenu.addAction(self.save_action)
        
        edit_menu = self.ui.menubar.addMenu("Edit")
        edit_menu.addAction(self.prompt_edit)
        
    def setup_filters(self):
        self.filters = {}
        self.filter_layout = QVBoxLayout()
        self.ui.filters.setLayout(self.filter_layout)
        for tag,f in get_all_filters().items():
            btn = QPushButton(tag)
            curr_filter = f
            self.filters[tag] = curr_filter
            btn.clicked.connect(partial(self.add_filter_layer,curr_filter))
            self.filter_layout.addWidget(btn)
        self.filter_layout.addSpacerItem(QSpacerItem(0,10, QSizePolicy.Expanding, QSizePolicy.Expanding))
    
    def setup_layers(self):
        self.ui.layer_layout.addSpacerItem(QSpacerItem(0,10, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.layers = []
    
    def add_filter(self,name:str):
        if name in self.filters:
            self.add_filter_layer(self.filters[name])
        else:
            print("Unknown filter")
            
    def add_filter_layer(self,f):
        instance = f()
        instance.show_argument_dialog()
        self.add_layer(FilterLayer(instance))
    
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
        
        def set_alpha(x):
            layer._layer.set_alpha(x/1000)
            self.update_view()
        layer.ui.alpha_slider.valueChanged.connect(set_alpha)
        
    def update_view(self):
        img = None
        for l in self.layers:
            img = l.apply(img, self.activeTool)
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
    
    def prompt_action(self):
        d = QDialog()
        w = ComandLine(self,d)
        layout = QVBoxLayout()
        layout.addWidget(w)
        d.setLayout(layout)
        d.setWindowFlag(Qt.FramelessWindowHint)
        d.move(QCursor.pos())
        d.exec()
        
        