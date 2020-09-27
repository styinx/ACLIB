from memory.ac_data import ACData
from memory.meta.car import Car
from memory.meta.environment import Environment
from memory.meta.tyres import Tyres
from settings import get, AC_CAR_DIR, METADATA_DIR, path
from util.acd import write_ACD, decrypt_ACD
from util.event import EventListener


class ACMeta(EventListener):
    class EVENT:
        READY = 'READY'

    def __init__(self, data: ACData):
        super().__init__()

        self._data = data
        self._acd = None
        self._ready = False

        self._car = None
        self._tyres = None
        self._environment = None

        data.on(ACData.EVENT.READY, self.init)

    def init(self):
        car_model = self._data.car.model
        self._acd = decrypt_ACD(path(AC_CAR_DIR, car_model, 'data.acd'))

        if get('write_acd'):
            source_dir = path(AC_CAR_DIR, car_model, 'data.acd')
            target_dir = path(METADATA_DIR, car_model)
            write_ACD(source_dir, target_dir, self._acd)

        self._car = Car(self._data, self._acd[1])
        self._tyres = Tyres(self._data, self._acd[1])
        self._environment = Environment(self._data)

        self._fire(ACMeta.EVENT.READY)

    @property
    def car(self):
        return self._car

    @property
    def tyres(self):
        return self._tyres

    @property
    def environment(self):
        return self._environment
