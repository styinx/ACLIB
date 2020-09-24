import json

from settings import METADATA_DIR, AC_CAR_DIR, path
from storage.config import Config


class Car:
    def __init__(self, data, acd: dict):
        car_file = open(path(AC_CAR_DIR, data.car.model, 'ui', 'ui_car.json'), 'r', encoding='utf-8')
        self._car_config = json.loads(car_file.read(), strict=False)
        car_file.close()
        self._car_meta = Config(path(METADATA_DIR, data.car.model, 'ACLIB_car.ini'))

        self._car_meta.select('Car')
        self._car_meta.set('name', self._car_config['name'])
        self._car_meta.set('class', self._car_config['tags'][0][1:])
        self._car_meta.set('type', self._car_config['class'])
        self._car_meta.set('brand', self._car_config['brand'])
        self._car_meta.set('brand_badge', 'content/cars/' + data.car.model + '/ui/badge.png')

        self._car_meta.select('Engine')
        engine_file = Config(acd['engine.ini']).dict
        self._car_meta.set('rpm_min', engine_file['ENGINE_DATA']['MINIMUM'])
        self._car_meta.set('rpm_max', engine_file['ENGINE_DATA']['LIMITER'])
        self._car_meta.set('rpm_damage', engine_file['DAMAGE']['RPM_THRESHOLD'])

    @property
    def name(self):
        return self._car_meta.get('Car', 'name')

    @property
    def class_name(self):
        return self._car_meta.get('Car', 'class')

    @property
    def type(self):
        return self._car_meta.get('Car', 'type')

    @property
    def brand(self):
        return self._car_meta.get('Car', 'brand')

    @property
    def badge(self):
        return self._car_meta.get('Car', 'badge')

    @property
    def rpm_min(self):
        return self._car_meta.get('Engine', 'rpm_min')

    @property
    def rpm_max(self):
        return self._car_meta.get('Engine', 'rpm_max')

    @property
    def rpm_damage(self):
        return self._car_meta.get('Engine', 'rpm_damage')