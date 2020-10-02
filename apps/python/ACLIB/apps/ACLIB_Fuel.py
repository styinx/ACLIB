from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.color import Color
from ui.gui.font import Font
from ui.gui.layout import ACGrid
from ui.gui.ac_widget import ACApp, ACLabel, ACProgressBar


class Fuel(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Fuel', 200, 200, 250, 60)

        self.hide_decoration()

        self._data = data
        self._meta = meta

        self._data.on(ACData.EVENT.READY, self.init)
        self._data.on(ACData.EVENT.KM_CHANGED, self.on_km)
        self._data.on(ACData.EVENT.LAP_CHANGED, self.on_lap)
        self._data.on(ACData.EVENT.FUEL_CHANGED, self.on_fuel)

        self._normal_font = Font('Roboto Mono')
        self._normal_font.bold = 1
        self._normal_font.size = 12
        self._small_font = Font('Roboto Mono')
        self._small_font.size = 11

        self._grid = ACGrid(3, 4, self)
        self._fuel = ACLabel(self._grid, '', 'left', 'middle', self._normal_font)
        self._fuel_bar = ACProgressBar(self._grid)
        self._fuel_bar.background_color = Color(0.8, 0.8, 0.0, 0.75)
        self._fuel_bar.border_color = Color(0.0, 0.0, 0.0, 1.0)
        self._fuel_km = ACLabel(self._grid, '0.0 l/km', 'right', 'middle', self._small_font)
        self._avg_km = ACLabel(self._grid, 'Ø 0.0 l/km', 'right', 'middle', self._small_font)
        self._km = ACLabel(self._grid, '+ 0.0   km', 'right', 'middle', self._small_font)
        self._fuel_lap = ACLabel(self._grid, '0.0  l/L', 'right', 'middle', self._small_font)
        self._avg_lap = ACLabel(self._grid, 'Ø 0.0  l/L', 'right', 'middle', self._small_font)
        self._laps = ACLabel(self._grid, '+ 0.0 Laps', 'right', 'middle', self._small_font)

        self._grid.add(self._fuel, 0, 0, 1, 2)
        self._grid.add(self._fuel_bar, 1, 0, 2, 2)
        self._grid.add(self._fuel_km, 0, 2)
        self._grid.add(self._avg_km, 1, 2)
        self._grid.add(self._km, 2, 2)
        self._grid.add(self._fuel_lap, 0, 3)
        self._grid.add(self._avg_lap, 1, 3)
        self._grid.add(self._laps, 2, 3)

        self._fuel_lap_val = 0
        self._fuel_per_lap_avg = 0
        self._fuel_per_lap_ref = 0
        self._fuel_km_val = 0
        self._fuel_per_km_avg = 0
        self._fuel_per_km_ref = 0

    def init(self):
        self._fuel_per_lap_ref = self._data.car.fuel
        self._fuel_per_km_ref = self._data.car.fuel

        self._fuel_bar.value = round(self._data.car.fuel / self._data.car.max_fuel, 1)

    def on_fuel(self, fuel: float):
        self._fuel.text = '{} l'.format(round(fuel, 1))
        self._fuel_bar.value = round(fuel / self._data.car.max_fuel, 1)

    def on_lap(self, lap: int):
        self._fuel_lap_val = max(0.0, round(self._fuel_per_lap_ref - self._data.car.fuel, 1))

        if self._fuel_per_lap_avg == 0:
            self._fuel_per_lap_avg = self._fuel_lap_val
        else:
            self._fuel_per_lap_avg = round((self._fuel_per_lap_avg + self._fuel_lap_val) / 2, 1)

        self._fuel_lap.text = '{}  l/L'.format(self._fuel_lap_val)
        self._avg_lap.text = 'Ø {}  l/L'.format(self._fuel_per_lap_avg)
        self._laps.text = '+ {} Laps'.format(round(self._data.car.fuel / max(1.0, self._fuel_lap_val), 1))
        self._fuel_per_lap_ref = self._data.car.fuel

    def on_km(self, km: int):
        self._fuel_km_val = max(0.0, round(self._fuel_per_km_ref - self._data.car.fuel, 1))

        if self._fuel_per_km_avg == 0:
            self._fuel_per_km_avg = self._fuel_km_val
        else:
            self._fuel_per_km_avg = round((self._fuel_per_km_avg + self._fuel_km_val) / 2, 1)

        self._fuel_km.text = '{} l/km'.format(self._fuel_km_val)
        self._avg_km.text = 'Ø {} l/km'.format(self._fuel_per_km_avg)
        self._km.text = '+ {}   km'.format(round(self._data.car.fuel / max(1.0, self._fuel_km_val), 1))
        self._fuel_per_km_ref = self._data.car.fuel