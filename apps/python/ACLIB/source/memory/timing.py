from memory.ac_info import active_car_only

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
    def current_sector_index(self):
        return self._info.graphics.currentSectorIndex