class Environment:
    def __init__(self, info):
        self._info = info

    @property
    def surface_grip(self):
        return self._info.graphics.surfaceGrip

    @property
    def wind_speed(self):
        return self._info.graphics.windSpeed

    @property
    def wind_direction(self):
        return self._info.graphics.windDirection

    @property
    def road_temperature(self):
        return self._info.static.roadTemp

    @property
    def air_temperature(self):
        return self._info.static.airTemp

    @property
    def track_name(self):
        return self._info.static.track

    @property
    def track_configuration(self):
        return self._info.static.trackConfiguration

    @property
    def track_length(self):
        return self._info.static.trackSPlineLength
