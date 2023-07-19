from os import path
import sys
sys.path.insert(0,path.abspath("."))



from PySide6.QtWidgets import QApplication
from src.diagram import Diagram

def main():
    app = QApplication()
    diagram = Diagram()
    diagram.show()
    app.exec()

if __name__ == "__main__":
    main()