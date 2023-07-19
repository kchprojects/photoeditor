from functools import partial
from PySide6.QtWidgets import QMainWindow,QFileDialog,QVBoxLayout,QPushButton,QSpacerItem,QSizePolicy
from PySide6.QtGui import QAction,QKeySequence
from photoeditor.filter_factory import all_filters
from photoeditor.ui.ui_diagram import Ui_MainWindow
import cv2

class Diagram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_actions()
        self.setup_filters()
    
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
        for tag,f in all_filters.items():
            btn = QPushButton(tag)
            curr_filter = f()
            self.filters[tag] = curr_filter
            btn.clicked.connect(partial(self.apply_filter,curr_filter))
            self.filter_layout.addWidget(btn)
        self.filter_layout.addSpacerItem(QSpacerItem(0,10, QSizePolicy.Expanding, QSizePolicy.Expanding))
                
    def apply_filter(self,f):
        self.ui.canvas.set_image(f(self.ui.canvas.get_current_image()))
        
    def save_image(self):
        img = self.ui.canvas.get_current_image()
        if img is None:
            print("No image to save")
        else:
            file,_ = QFileDialog.getSaveFileName(self,"Save image","*.png;*.jpg;*.bmp")
            img = cv2.imwrite(file,img)
    
    def open_image(self):
        file,_ = QFileDialog.getOpenFileName(self,"Save image","*.png;*.jpg;*.bmp")
        img = cv2.imread(file,cv2.IMREAD_UNCHANGED)
        self.ui.canvas.set_image(img)
        
        