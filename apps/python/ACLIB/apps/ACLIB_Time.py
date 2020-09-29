from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.gui.widget import ACApp, ACLabel
from ui.gui.font import Font
from ui.gui.layout import ACGrid

from ui.color import Color
from util.format import Format


class Time(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Time', 200, 200, 160, 80)

        self.hide_decoration()
        self.border = False

        self._data = data
        self._font = Font("Roboto Mono")
        self._font.color = Color(1.0, 1.0, 1.0)
        self._font.size = 12

        self._row = 0
        self._col = 0

        self._grid = ACGrid(2, 3, self)
        self._local_time = ACLabel('', 'right', 'top', self._font, self)
        self._session_time = ACLabel('', 'right', 'middle', self._font, self)
        self._time_left = ACLabel('', 'right', 'bottom', self._font, self)

        self._grid.add(ACLabel('Local time:', parent=self), self.col(), self.row())
        self._grid.add(self._local_time, self.col(1), self.row())

        self._grid.add(ACLabel('Session time:', parent=self), self.col(-1), self.row(1))
        self._grid.add(self._session_time, self.col(1), self.row())

        self._grid.add(ACLabel('Time left:', parent=self), self.col(-1), self.row(1))
        self._grid.add(self._time_left, self.col(1), self.row())

        if self._data.session.is_timed_race:
            self._session_time.text = Format.duration(self._data.session.time_left)
        else:
            self._session_time.text = Format.s(self._data.session.laps, ' Lap')

    def row(self, add: int = 0):
        self._row += add
        return self._row

    def col(self, add: int = 0):
        self._col += add
        return self._col

    def update(self, delta: int):
        super().update(delta)

        self._local_time.text = Format.time()

        if self._data.session.is_timed_race:
            self._time_left.text = Format.duration(self._data.session.time_left)
        else:
            if self._data.session.laps > 0:
                self._time_left.text = Format.s(self._data.session.laps - self._data.timing.lap, ' Lap')

    def render(self, delta: int):
        super().render(delta)
