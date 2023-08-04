from photoeditor.ui.ui_command_line import Ui_Form
from PySide6.QtCore import QEvent,Qt
from PySide6.QtWidgets import QWidget
from photoeditor.filter_factory import get_segmentation_filters

class ComandLine(QWidget):
    
    commands = ["segment","select", "filter"]
    
    def __init__(self,diagram,dialog=None,parent=None):
        super().__init__(parent)
        self.dialog = dialog
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.diagram = diagram
        self.ui.edit.textChanged.connect(self.on_text_change)
        self.ui.edit.returnPressed.connect(self.on_return)
        self.seg_filters = get_segmentation_filters()

    def event(self,event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key.Key_Tab:
                self.autocomplete()
                return True
        return super().event(event)
    
    def autocomplete(self):
        text = self.ui.edit.text()
        words = text.split(" ")
        changes = 0
        new_word = None
        if len(words) == 1:
            for cmd in self.commands:
                if cmd.lower().startswith(words[-1].lower()):
                    new_word = cmd
                    changes += 1
        if changes == 0 and len(words) > 1:
            if words[-2] == "filter":
                for f_name in self.diagram.filters:
                    if f_name.lower().startswith(words[-1].lower()):
                        new_word = f_name
                        changes += 1
            if words[-2] == "segment":
                for f_name in self.seg_filters:
                    if f_name.lower().startswith(words[-1].lower()):
                        new_word = f_name
                        changes += 1
        if changes == 1:
            words[-1] = new_word + " "
        self.ui.edit.setText(" ".join(words))
        
    def text(self):
        return self.ui.edit.text()
    
    def on_return(self):
        words = self.text().split(" ")        
        if not words:
            return
        try:
            if words[0] in self.commands:
                if words[0] == "filter":
                    self.diagram.add_filter(words[1])
                elif words[0] == "segment":
                    self.diagram.add_filter_layer(self.seg_filters[words[1]])
        except Exception as e:
            print(str(e))
        self.dialog.close()
                
    def on_text_change(self):
        pass