from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from settings import path, TEXTURE_DIR
from ui.color import Color, BLACK, WHITE
from ui.gui.aclib_widget import ACLIBProgressBar, ACLIBScaler
from ui.gui.font import Font
from ui.gui.layout import ACGrid
from ui.gui.ac_widget import ACApp, ACLabel


class Fuel(ACApp):
    TEXTURES = {
        'left': path(TEXTURE_DIR, 'left.png'),
        'center': path(TEXTURE_DIR, 'center.png'),
        'right': path(TEXTURE_DIR, 'right.png'),
        'fuel': path(TEXTURE_DIR, 'fuel.png'),
        'background': path(TEXTURE_DIR, 'background.png')
    }

    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Fuel', 200, 200, 300, 66)

        self.hide_decoration()

        self._data = data
        self._meta = meta
        self._init = False

        self._normal_font = Font('Roboto Mono')
        self._normal_font.bold = 1
        self._normal_font.color = BLACK

        self._small_font = Font('Roboto Mono')
        self._small_font.color = BLACK


        self._main_grid = ACGrid(10, 3, self)

        self._grid = ACGrid(3, 3, self._main_grid)
        self._fuel_bar = ACLIBProgressBar(self._grid, 0)
        self._fuel_bar.show_progress = True
        self._fuel_bar.progress_color = Color(0.8, 0.8, 0.0, 1.0)
        self._fuel_bar.background_color = BLACK
        self._fuel = ACLabel(self._grid, '', 'center', self._normal_font)
        self._fuel.background_color = WHITE

        self._fuel_km = ACLabel(self._grid, '', 'center', self._small_font)
        self._fuel_km.background_color = WHITE
        self._avg_km = ACLabel(self._grid, 'Ø 0.0 l/km', 'center', self._small_font)
        self._avg_km.background_color = WHITE
        self._km = ACLabel(self._grid, '', 'center', self._small_font)
        self._km.background_color = WHITE

        self._fuel_lap = ACLabel(self._grid, '', 'center', self._small_font)
        self._fuel_lap.background_texture = Fuel.TEXTURES['left']
        self._avg_lap = ACLabel(self._grid, 'Ø 0.0  l/L', 'center', self._small_font)
        self._avg_lap.background_color = WHITE
        self._laps = ACLabel(self._grid, '', 'center', self._small_font)
        self._laps.background_texture = Fuel.TEXTURES['right']

        self._scaler = ACLIBScaler(self._grid, self._grid, 0.1)

        self._main_grid.add(self._scaler, 0, 0, 1, 2)
        self._main_grid.add(self._grid, 1, 0, 9, 3)

        self._grid.add(self._fuel, 0, 0, 1, 1)
        self._grid.add(self._fuel_bar, 1, 0, 2, 1)

        self._grid.add(self._fuel_km, 0, 1)
        self._grid.add(self._avg_km, 1, 1)
        self._grid.add(self._km, 2, 1)

        self._grid.add(self._fuel_lap, 0, 2)
        self._grid.add(self._avg_lap, 1, 2)
        self._grid.add(self._laps, 2, 2)

        self._fuel_lap_val = 0
        self._fuel_lap_avg = 0
        self._fuel_lap_ref = 0
        self._fuel_km_val = 0
        self._fuel_km_avg = 0
        self._fuel_km_ref = 0

        self._data.on(ACData.EVENT.READY, self.init)
        self._data.on(ACData.EVENT.PIT_ENTERED, self.init)
        self._data.on(ACData.EVENT.KM_CHANGED, self.on_km)
        self._data.on(ACData.EVENT.LAP_CHANGED, self.on_lap)
        self._data.on(ACData.EVENT.FUEL_CHANGED, self.on_fuel)

    def init(self):
        self._init = True
        self._fuel_lap_ref = self._data.car.fuel
        self._fuel_km_ref = self._data.car.fuel

        self._fuel_bar.range = (0, self._data.car.max_fuel)

        self._fuel.text = '{} l'.format(round(self._data.car.fuel, 1))
        self._fuel_bar.value = self._data.car.fuel

        self._fuel_km.text = '0.0 l/km'
        self._km.text = '+ 0.0   km'

        self._fuel_lap.text = '0.0  l/L'
        self._laps.text = '+ 0.0 Laps'

    def on_fuel(self, fuel: float):
        self._fuel.text = '{} l'.format(round(fuel, 1))
        self._fuel_bar.value = fuel

    def on_lap(self, lap: int):
        if self._init:
            self._fuel_lap_val = self._fuel_lap_ref - self._data.car.fuel
            self._fuel_lap_ref = self._data.car.fuel

            if self._fuel_lap_avg == 0:
                self._fuel_lap_avg = self._fuel_lap_val
            else:
                self._fuel_lap_avg = (self._fuel_lap_avg + self._fuel_lap_val) / 2

            self._fuel_lap.text = '{}  l/L'.format(round(self._fuel_lap_val, 1))
            self._avg_lap.text = 'Ø {}  l/L'.format(round(self._fuel_lap_avg, 1))
            if self._fuel_lap_val > 0:
                self._laps.text = '+ {} Laps'.format(round(self._data.car.fuel / self._fuel_lap_val, 1))

    def on_km(self, km: int):
        if self._init:
            self._fuel_km_val = self._fuel_km_ref - self._data.car.fuel
            self._fuel_km_ref = self._data.car.fuel

            if self._fuel_km_avg == 0:
                self._fuel_km_avg = self._fuel_km_val
            else:
                self._fuel_km_avg = (self._fuel_km_avg + self._fuel_km_val) / 2

            self._fuel_km.text = '{} l/km'.format(round(self._fuel_km_val, 1))
            self._avg_km.text = 'Ø {} l/km'.format(round(self._fuel_km_avg, 1))
            if self._fuel_km_val > 0:
                self._km.text = '+ {}   km'.format(round(self._data.car.fuel / self._fuel_km_val, 1))
