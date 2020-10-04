import ac

from memory.data.server import Server


class Players:
    def __init__(self, server: Server):
        self._server = server
        self._player = 0

    def __getitem__(self, player: int):
        if 0 <= player <= self._server.cars:
            self._player = player
        return self

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
