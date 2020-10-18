import ac
import acsys


class Timing:
    def __init__(self, info):
        self._info = info

    @property
    def lap(self):
        return self._info.graphics.completedLaps

    @property
    def current_lap_time(self):
        return self._info.graphics.iCurrentTime

    @property
    def last_lap_time(self):
        return self._info.graphics.iLastTime

    @property
    def best_lap_time(self):
        return self._info.graphics.iBestTime

    @property
    def current_sector_index(self):
        return self._info.graphics.currentSectorIndex

    @property
    def valid_lap(self):
        return ac.getCarState(0, acsys.CS.LapInvalidated)