from PySide6.QtWidgets import QApplication
from photoeditor.diagram import Diagram

def main():
    app = QApplication()
    diagram = Diagram()
    diagram.show()
    app.exec()

if __name__ == "__main__":
    main()