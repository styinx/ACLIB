from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.gui.ac_widget import ACApp, ACLabel
from ui.gui.layout import ACGrid

from util.format import Format


class Time(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Time', 200, 200, 160, 80)

        self.hide_decoration()
        self.border = False

        self._data = data
        self._meta = meta

        self._row = 0
        self._col = 0

        self._grid = ACGrid(2, 3, self)
        self._local_time = ACLabel(self._grid, '', 'right')
        self._session_time = ACLabel(self._grid, '', 'right')
        self._time_left = ACLabel(self._grid, '', 'right', 'bottom')

        self._grid.add(ACLabel(self._grid, 'Local time:'), self.col(), self.row())
        self._grid.add(self._local_time, self.col(1), self.row())

        self._grid.add(ACLabel(self._grid, 'Session time:'), self.col(-1), self.row(1))
        self._grid.add(self._session_time, self.col(1), self.row())

        self._grid.add(ACLabel(self._grid, 'Time left:'), self.col(-1), self.row(1))
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
