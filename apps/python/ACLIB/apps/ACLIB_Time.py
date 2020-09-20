from time import strftime, localtime

from memory.ac_data import ACData
from ui.gui.widget import Font, ACApp, ACLabel
from ui.gui.layout import ACGrid

from ui.color import Color
from util.util import Format


class Time(ACApp):
    def __init__(self, data: ACData = None, meta = None):
        super().__init__('ACLIB_Time', 200, 200, 160, 80)

        self._data = data
        self._font = Font("Roboto Mono")
        self._font.color = Color(1.0, 1.0, 1.0)
        self._font.size = 12

        self._row = 0
        self._col = 0

        self._grid = ACGrid(2, 3, self)
        self._local_time = ACLabel('', self._font, 'right', 'top', parent=self)
        self._session_time = ACLabel('', self._font, 'right', 'middle', parent=self)
        self._time_left = ACLabel('', self._font, 'right', 'bottom', parent=self)

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

        self.hide_decoration()

    def row(self, add: int = 0):
        self._row += add
        return self._row

    def col(self, add: int = 0):
        self._col += add
        return self._col

    def update(self, delta: int):
        self._local_time.text = Format.time()

        if self._data.session.is_timed_race:
            self._time_left.text = Format.duration(self._data.session.time_left)
        else:
            if self._data.session.laps > 0:
                self._time_left.text = Format.s(self._data.session.laps - self._data.timing.lap, ' Lap')

    def render(self, delta: int):
        pass
