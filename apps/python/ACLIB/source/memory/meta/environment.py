import json

from settings import METADATA_DIR, AC_TRACK_DIR, path
from storage.config import Config


class Environment:
    @staticmethod
    def parse_track_length(length: str):
        if length.endswith('m'):
            return int(length[-1])
        return int(length)

    def __init__(self, data):
        track_name = data.environment.track_name
        track_config = data.environment.track_configuration

        if not track_config:
            file = open(path(AC_TRACK_DIR, track_name, 'ui', 'ui_track.json'), 'r')
        else:
            file = open(path(AC_TRACK_DIR, track_name, 'ui', track_config, 'ui_track.json'), 'r')

        self._track_config = json.loads(file.read(), strict=False)
        file.close()
        self._track_meta = Config(path(METADATA_DIR, track_name, 'ACLIB_track.ini'))

        self._track_meta.set('length', Environment.parse_track_length(self._track_config['length']))

    def get_track_length(self):
        return self._track_meta['length']