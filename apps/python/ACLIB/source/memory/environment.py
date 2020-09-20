import json
import os

from settings import METADATA_DIR
from storage.config import Config


class EnvironmentData:
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


class EnvironmentMeta:
    @staticmethod
    def parse_track_length(length: str):
        if length.endswith('m'):
            return int(length[-1])
        return int(length)

    def __init__(self, track_name: str, track_config: str):
        if track_config != '':
            file = open('content/tracks/' + track_name + '/ui/ui_track.json', 'r')
        else:
            file = open('content/tracks/' + track_name + '/ui/' + track_config + '/ui_track.json', 'r')

        self._track_config = json.loads(file.read(), strict=False)
        file.close()
        self._track_meta = Config(os.path.join(METADATA_DIR, track_name, 'ACLIB_track.ini'))

        self._track_meta.set('length', EnvironmentMeta.parse_track_length(self._track_config['length']))

    def get_track_length(self):
        return self._track_meta['length']
