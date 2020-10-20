import ac
import acsys

from time import time
from memory.data.server import Server


class Players:
    def __init__(self, server: Server):
        self._server = server
        self._player = 0
        self._valid = {}

        self._lap_index = {}
        self._lap_progress = {}
        self._current_lap_time = {}
        self._start_lap_time = {}
        self._pb_lap_time = {}
        self._gb_lap_time = float('inf')

        self._sector_index = {}
        self._current_sector_time = {}
        self._pb_sector_time = {}
        self._gb_sector_time = [float('inf')] * 3

        #self._mini_sector_index = {}
        #self._mini_sector_time = {}

        for c in range(0, self._server.cars):
            self._valid[c] = False
            self._lap_index[c] = 0
            self._lap_progress[c] = 0.0
            self._current_lap_time[c] = 0.0
            self._start_lap_time[c] = time() * 1000
            self._pb_lap_time[c] = float('inf')

            self._sector_index[c] = 0
            self._current_sector_time[c] = [0.0] * 3
            self._pb_sector_time[c] = [float('inf')] * 3

            #self._mini_sector_index[c] = 0
            #self._mini_sector_time[c] = {}

    def __getitem__(self, player: int):
        if 0 <= player <= self._server.cars:
            self._player = player
        return self

    def update(self, delta: int):
        for c in range(0, self._server.cars):
            if ac.isCarInPit(c) or not ac.isConnected(c):
                continue

            lap = ac.getCarState(c, acsys.CS.LapCount)
            pos = ac.getCarState(c, acsys.CS.NormalizedSplinePosition)
            invalid = ac.getCarState(c, acsys.CS.LapInvalidated) and self._valid[c]
            sec = int(pos * 3)
            #msec = int(pos * 12)

            if lap != self._lap_index[c]:
                self._valid[c] = True
                self._start_lap_time[c] = time() * 1000
                best_lap = ac.getCarState(c, acsys.CS.BestLap)
                if not invalid and best_lap > 0:
                    if best_lap < self._gb_lap_time:
                        self._gb_lap_time = best_lap
                        self._pb_lap_time[c] = best_lap
                    elif best_lap < self._pb_lap_time[c]:
                        self._pb_lap_time[c] = best_lap

                self._lap_index[c] = lap

            self._current_lap_time[c] = time() * 1000 - self._start_lap_time[c]

            if sec > 0:
                self._current_sector_time[c][sec] = self._current_lap_time[c] - sum(self._current_sector_time[c][:sec])
            else:
                self._current_sector_time[c][sec] = self._current_lap_time[c]

            if sec != self._sector_index[c]:
                last_sec = self._sector_index[c]

                if not invalid and self._current_sector_time[c][last_sec] > 0:
                    if self._current_sector_time[c][last_sec] < self._gb_sector_time[last_sec]:
                        self._gb_sector_time[last_sec] = self._current_sector_time[c][last_sec]
                        self._pb_sector_time[c][last_sec] = self._current_sector_time[c][last_sec]
                    elif self._current_sector_time[c][last_sec] < self._pb_sector_time[c][last_sec]:
                        self._pb_sector_time[c][last_sec] = self._current_sector_time[c][last_sec]

                self._sector_index[c] = sec

            # if msec != self._sector_index[c]:
            #     self._mini_sector_index[c] = msec

    @property
    def position(self):
        return ac.getLeaderboardPosition(self._player)

    @property
    def real_position(self):
        return ac.getRealTimeLeaderboardPosition(self._player)

    @property
    def name(self):
        return ac.getDriverName(self._player)

    @property
    def connected(self):
        return ac.isConnected(self._player)

    @property
    def car(self):
        return ac.getCarName(self._player)

    @property
    def splits(self):
        return ac.getLastSplits(self._player)

    @property
    def in_pit_line(self):
        return ac.isCarInPitline(self._player)

    @property
    def in_pit(self):
        return ac.isCarInPit(self._player)

    @property
    def best_lap(self):
        return ac.getCarState(self._player, acsys.CS.BestLap)

    @property
    def last_lap(self):
        return ac.getCarState(self._player, acsys.CS.LastLap)

    @property
    def pb_lap_time(self):
        return self._pb_lap_time[self._player]

    @property
    def gb_lap_time(self):
        return self._gb_lap_time

    @property
    def sector_index(self):
        return self._sector_index[self._player]

    def sector_time(self, sec: int):
        if 0 <= sec < 3:
            return self._current_sector_time[self._player][sec]
        return 0

    def pb_sector_time(self, sec: int):
        if 0 <= sec < 3:
            return self._pb_sector_time[self._player][sec]
        return 0

    def gb_sector_time(self, sec: int):
        if 0 <= sec < 3:
            return self._gb_sector_time[sec]
        return 0

    # def mini_sector_time(self, msec: int):
    #     if 0 <= msec <= 12 and msec in self._mini_sector_time[self._player]:
    #         return self._mini_sector_time[self._player][msec]
    #     return 0
