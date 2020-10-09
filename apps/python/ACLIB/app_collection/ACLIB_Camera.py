from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.color import RED, TRANSPARENT, DARKGRAY, BLACK, WHITE
from ui.gui.font import Font
from ui.gui.layout import ACGrid
from ui.gui.ac_widget import ACApp, ACLabel, ACWidget
import ac

from util.log import console


class Camera(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Camera', 200, 200, 150, 250)

        self.hide_decoration()
        self.background_color = TRANSPARENT

        self._data = data

        self._grid = ACGrid(2, 11, self)
        self._prev = ACLabel(self._grid, '<-', 'center')
        self._next = ACLabel(self._grid, '->', 'center')

        self._prev.background_color = DARKGRAY
        self._next.background_color = DARKGRAY

        self._grid.add(self._prev, 0, 0)
        self._grid.add(self._next, 1, 0)

        self._prev.on(ACWidget.EVENT.CLICK, self.prev)
        self._next.on(ACWidget.EVENT.CLICK, self.next)

        self._cameras = ['Cockpit', 'Car', 'Drivable', 'Track', 'Helicopter', 'OnBoardFree', 'Free', 'Random', 'ImageGeneratorCamera', 'Start']

        self._labels = []
        self._cam_id = 0

        self._active_font = Font('Roboto Mono')
        self._active_font.size = 12
        self._active_font.color = WHITE

        self._inactive_font = Font('Roboto Mono')
        self._inactive_font.size = 12
        self._inactive_font.color = WHITE

        i = 0
        for cam_id, name in enumerate(self._cameras):
            label = ACLabel(self._grid, name, 'center', self._inactive_font)
            label.background_color = BLACK
            label.on(ACWidget.EVENT.CLICK, self.select)
            setattr(label, 'cam', cam_id)
            self._labels.append(label)

            self._grid.add(label, 0, i + 1, 2, 1)
            i += 1
            console(label.size)

        self._data.on(ACData.EVENT.READY, self.init)

    def init(self):
        self._cam_id = ac.getCameraMode()
        self._labels[self._cam_id].font = self._active_font
        self._labels[self._cam_id].background_color = RED

    def by_id(self, cam_id):
        if 0 <= cam_id <= 9:
            self._labels[self._cam_id].font = self._inactive_font
            self._labels[self._cam_id].background_color = BLACK

            ac.setCameraMode(cam_id)
            self._cam_id = cam_id

            self._labels[self._cam_id].font = self._active_font
            self._labels[self._cam_id].background_color = RED

    def select(self, widget: ACWidget):
        self.by_id(widget.cam)

    def next(self, widget: ACWidget):
        if self._cam_id == 9:
            self.by_id(0)
        else:
            self.by_id(self._cam_id + 1)

    def prev(self, widget: ACWidget):
        if self._cam_id == 0:
            self.by_id(9)
        else:
            self.by_id(self._cam_id - 1)
