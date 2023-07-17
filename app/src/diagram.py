from PySide6.QtWidgets import QMainWindow,QFileDialog
from PySide6.QtGui import QAction,QKeySequence
from ui.ui_diagram import Ui_MainWindow
import cv2

class Diagram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_actions()
    
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
        
        