class Session:
    STATUS = {0: 'None', 1: 'Replay', 2: 'Live', 3: 'Pause'}
    TYPE = {-1: 'Unknown', 0: 'Practice', 1: 'Qualifying', 2: 'Race', 3: 'Hotlap', 4: 'Time Attack', 5: 'Drift',
            6:  'Drag'}
    FLAG = {0: 'None', 1: 'Blue', 2: 'Yellow', 3: 'Black', 4: 'White', 5: 'Checkered', 6: 'Penalty'}

    def __init__(self, info):
        self._info = info

    @property
    def status(self):
        return self._info.graphics.status

    @property
    def status_name(self):
        return Session.STATUS[self.status]

    @property
    def session(self):
        return self._info.graphics.session

    @property
    def name(self):
        return Session.TYPE[self.session]

    @property
    def number_of_sessions(self):
        return self._info.static.numberOfSessions

    @property
    def time_left(self):
        return self._info.static.sessionTimeLeft

    @property
    def laps(self):
        return self._info.graphics.numberOfLaps

    @property
    def flag(self):
        return self._info.graphics.flag

    @property
    def flag_name(self):
        return Session.FLAG[self.flag]

    @property
    def pit_window_start(self):
        return self._info.static.pitWindowStart

    @property
    def pit_window_end(self):
        return self._info.static.pitWindowEnd

    @property
    def is_timed_race(self):
        return self._info.static.isTimedRace

    @property
    def has_reversed_grid(self):
        return self._info.static.reverseGridPositions

    @property
    def number_of_drivers(self):
        return self._info.static.numCars

    @property
    def fuel_rate(self):
        return self._info.static.aidFuelRate

    @property
    def tyre_rate(self):
        return self._info.static.aidTireRate

    @property
    def damage_rate(self):
        return self._info.static.aidMechanicalDamage

    @property
    def has_tyre_blankets(self):
        return self._info.static.aidAllowTyreBlankets

    @property
    def has_stability_control(self):
        return self._info.static.aidStability

    @property
    def has_auto_clutch(self):
        return self._info.static.aidAutoClutch

    @property
    def has_auto_blip(self):
        return self._info.static.aidAutoBlip
