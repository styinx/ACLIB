from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from settings import RESOURCE_DIR, path
from ui.gui.widget import ACApp, ACLabel, ACIcon, ACWidget
from ui.gui.font import Font
from ui.gui.layout import ACGrid, ACHBox

from ui.color import Color


class Comparator(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Comparator', 200, 200, 300, 300)

        self.hide_decoration()
        self.background_color = Color(0.1, 0.1, 0.1, 0.5)
        self.border = False

        self._data = data

        self._grid = ACGrid(1, 4, self)

        self._header = ComparatorRow(self, data, -1)
        self._driver = ComparatorRow(self, data, 0)
        self._opponent1 = ComparatorRow(self, data, 1)
        self._opponent2 = ComparatorRow(self, data, 2)

        self._grid.add(self._header, 0, 0)
        self._grid.add(self._driver, 0, 1)
        self._grid.add(self._opponent1, 0, 2)
        self._grid.add(self._opponent2, 0 , 3)

        self._header.init()
        self._driver.init()
        self._opponent1.init()
        self._opponent2.init()

    def update(self, delta: int):
        super().update(delta)

    def render(self, delta: int):
        pass


class ComparatorRow(ACWidget):
    def __init__(self, parent: ACApp, data: ACData, driver: int):
        super().__init__(parent)
        self._header = driver == -1
        self._mode = ''
        self._data = data

        self._header_font = Font("Roboto Mono")
        self._header_font.color = Color(0.9, 0.2, 0.2)
        self._header_font.size = 14

        self._grid = None
        self._label = None

        self._top_box = None
        self._bottom_box = None
        self._left = None
        self._right = None
        self._top = []
        self._bottom = []

    def init(self):
        self._grid = ACGrid(10, 3, self)
        self._label = ACLabel('', font=self._header_font, parent=self)

        self._top_box = ACHBox(self)
        self._bottom_box = ACHBox(self)
        self._left = ACIcon(path(RESOURCE_DIR, 'textures', 'arrow-left-slim.png'), self)
        self._right = ACIcon(path(RESOURCE_DIR, 'textures', 'arrow-right-slim.png'), self)
        self._top = []
        self._bottom = []

        self._grid.add(self._label, 1, 0, 8, 1)
        self._grid.add(self._left, 0, 1, 1, 2)
        self._grid.add(self._right, 9, 1, 1, 2)
        self._grid.add(self._top_box, 1, 1, 8, 1)
        self._grid.add(self._bottom_box, 1, 2, 8, 1)

        for i in range(0, 4):
            temp1 = ACLabel('--:--', h_alignment='center', parent=self)
            temp2 = ACLabel('--:--', h_alignment='center', parent=self)
            self._top.append(temp1)
            self._top_box.add(self._top[i])

            self._bottom.append(temp2)
            self._bottom_box.add(self._bottom[i])

        if not self._header:
            self._label.text = self._data.driver.firstname
        else:
            self._label.text = 'Sectors'
