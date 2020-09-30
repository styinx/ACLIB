from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.gui.layout import ACGrid
from ui.gui.widget import ACApp, ACLabel


class Fuel(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Fuel', 200, 200, 250, 50)

        self.hide_decoration()

        self._data = data
        self._meta = meta

        self._data.on(ACData.EVENT.READY, self.init)
        self._data.on(ACData.EVENT.KM_CHANGED, self.on_km)
        self._data.on(ACData.EVENT.LAP_CHANGED, self.on_lap)

        self._grid = ACGrid(2, 3, self)
        self._fuel = None
        self._fuel_km = None
        self._fuel_lap = None

        self._fuel_per_lap_ref = 0
        self._fuel_per_km_ref = 0

    def init(self):
        self._fuel = ACLabel('', 'right', 'middle', parent=self)
        self._fuel_km = ACLabel('', 'right', 'middle', parent=self)
        self._fuel_lap = ACLabel('', 'right', 'middle', parent=self)

        self._grid.add(self._fuel, 0, 0)
        self._grid.add(self._fuel_km, 0, 1)
        self._grid.add(self._fuel_lap, 0, 2)

        self._fuel_per_lap_ref = self._data.car.fuel
        self._fuel_per_km_ref = self._data.car.fuel

    def update(self, delta: int):
        self._fuel.text = '{} l'.format(round(self._data.car.fuel))

    def on_lap(self, lap: int):
        self._fuel_lap.text = '{}  l/L'.format(round(self._fuel_per_lap_ref - self._data.car.fuel))
        self._fuel_per_lap_ref = self._data.car.fuel

    def on_km(self):
        self._fuel_km.text = '{} l/Km'.format(round(self._fuel_per_km_ref - self._data.car.fuel))
        self._fuel_per_km_ref = self._data.car.fuel