from ui.color import TRANSPARENT
from ui.gui.ac_widget import ACWidget, ACButton


class ACLIBIcon(ACButton):
    def __init__(self, file: str, parent: ACWidget = None):
        super().__init__(parent)

        self.background_texture = file
        self.background_color = TRANSPARENT
        self.border = False
