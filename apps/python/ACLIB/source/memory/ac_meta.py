from memory.ac_data import ACData
from memory.meta.car import Car
from memory.meta.environment import Environment
from memory.meta.tyres import Tyres
from settings import get, AC_CAR_DIR, METADATA_DIR, path
from util.acd import write_ACD, decrypt_ACD


# def active_car_only(func):
#     if ac.getFocusedCar() == 0:
#         return func()
#     else:
#         return - 1

class ACMeta:
    def __init__(self, data: ACData):
        car_model = data.car.model
        self._acd = decrypt_ACD(path(AC_CAR_DIR, car_model, 'data.acd'))

        if get('write_acd'):
            source_dir = path(AC_CAR_DIR, car_model, 'data.acd')
            target_dir = path(METADATA_DIR, car_model)
            write_ACD(source_dir, target_dir, self._acd)

        self._car = Car(data, self._acd[1])
        self._tyres = Tyres(data, self._acd[1])
        self._environment = Environment(data)

    @property
    def car(self):
        return self._car

    @property
    def tyres(self):
        return self._tyres

    @property
    def environment(self):
        return self._environment
