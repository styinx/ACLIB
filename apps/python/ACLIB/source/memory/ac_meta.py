import os

from memory.ac_data import ACData
from memory.car import CarMeta, TyresMeta
from memory.environment import EnvironmentMeta
from settings import config, AC_CAR_DIR, METADATA_DIR
from util.acd import write_ACD, decrypt_ACD

class ACMeta:
    def __init__(self, data: ACData):
        car_model = data.car.model
        self._acd = decrypt_ACD(os.path.join(AC_CAR_DIR, car_model, 'data.acd'))

        if config('write_acd'):
            source_dir = os.path.join(AC_CAR_DIR, car_model, 'data.acd')
            target_dir = os.path.join(METADATA_DIR, car_model)
            write_ACD(source_dir, target_dir, self._acd)

        self._car = CarMeta(car_model)
        self._tyres = TyresMeta(car_model, self._acd[1])
        self._environment = EnvironmentMeta(data.environment.track_name, data.environment.track_configuration)

    @property
    def car(self):
        return self._car

    @property
    def tyres(self):
        return self._tyres

    @property
    def environment(self):
        return self._environment