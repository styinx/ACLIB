import time
from threading import Thread

from memory.data.server import Server
from memory.sim_info import SimInfo
from memory.data.car import Car
from memory.data.driver import Driver
from memory.data.environment import Environment
from memory.data.players import Players
from memory.data.session import Session
from memory.data.timing import Timing
from memory.data.tyres import Tyres
from util.event import EventListener
from util.observer import BoolObservable, Observable, IntervalObservable, RangeObservable


def avg(iterable):
    return sum(iterable) / len(iterable)


class ACData(EventListener):
    class EVENT:
        READY = 'READY'

        LAP_CHANGED = 'Lap Changed'
        SECTOR_CHANGED = 'Sector Changed'
        MINI_SECTOR_CHANGED = 'Minisector Changed'
        KM_SECTOR_CHANGED = 'KM Sector Changed'
        KM_CHANGED = 'KM Changed'
        POSITION_CHANGED = 'Position Changed'
        POSITION_GAINED = 'Position Gained'
        POSITION_LOST = 'Position Lost'

        FUEL_CHANGED = 'Fuel Changed'
        COMPOUND_CHANGED = 'Compound Changed'
        TYRE_WEAR_CHANGED = 'Tyre Wear Changed'
        TYRE_TEMP_CHANGED = 'Tyre Temperature Changed'

        FLAG_CHANGED = 'Flag Changed'
        PIT_ENTERED = 'Pit Entered'
        PIT_LEFT = 'Pit Left'
        PITLINE_ENTERED = 'Box Entered'
        PITLINE_LEFT = 'Box Left'
        LAP_INVALIDATED = 'Lap Invalidated'
        PENALTY_RECEIVED = 'Penalty Received'
        PENALTY_SERVED = 'Penalty Served'

        PLAYER_JOINED = 'Player Joined'
        PLAYER_LEFT = 'Player Left'

    class PROPERTY:
        IS_IN_PIT = 'Is in Pit'

    def __init__(self):
        super().__init__()

        self._ready = False
        self._timer = 0

        # Categories

        self._info = SimInfo()
        self._car = Car(self._info)
        self._driver = Driver(self._info)
        self._environment = Environment(self._info)
        self._session = Session(self._info)
        self._timing = Timing(self._info)
        self._tyres = Tyres(self._info)

        self._server = Server()
        self._players = Players(self._server)

        # Properties

        self._properties = {
            ACData.PROPERTY.IS_IN_PIT: BoolObservable(self, False, ACData.EVENT.PIT_ENTERED, ACData.EVENT.PIT_LEFT)
        }

        self._is_in_pit = BoolObservable(self, False, ACData.EVENT.PIT_ENTERED, ACData.EVENT.PIT_LEFT)
        self._is_in_pitline = BoolObservable(self, False, ACData.EVENT.PITLINE_ENTERED, ACData.EVENT.PITLINE_LEFT)
        self._has_penalty = BoolObservable(self, False, ACData.EVENT.PENALTY_RECEIVED, ACData.EVENT.PENALTY_SERVED)
        self._is_lap_valid = Observable(self, False, ACData.EVENT.LAP_INVALIDATED)
        self._position = Observable(self, 0, ACData.EVENT.POSITION_CHANGED)
        self._compound = Observable(self, 0, ACData.EVENT.COMPOUND_CHANGED)
        self._flag = Observable(self, 0, ACData.EVENT.FLAG_CHANGED)
        self._fuel = RangeObservable(self, 0, 0.01, ACData.EVENT.FUEL_CHANGED)
        self._tyre_temp = RangeObservable(self, 0, 0.1, ACData.EVENT.TYRE_TEMP_CHANGED)
        self._tyre_wear = RangeObservable(self, 0, 0.1, ACData.EVENT.TYRE_WEAR_CHANGED)
        self._lap = Observable(self, 0, ACData.EVENT.LAP_CHANGED)
        self._sector = Observable(self, 0, ACData.EVENT.SECTOR_CHANGED)
        self._mini_sector = Observable(self, 0, ACData.EVENT.MINI_SECTOR_CHANGED)
        self._km_sector = Observable(self, 0, ACData.EVENT.KM_SECTOR_CHANGED)
        self._km_traveled = Observable(self, 0, ACData.EVENT.KM_CHANGED)
        self._player_count = IntervalObservable(self, 0, ACData.EVENT.PLAYER_LEFT, ACData.EVENT.PLAYER_JOINED)

    def init(self):
        thread = Thread(target=self._check_ready_loop, daemon=True)
        thread.start()

    def _check_ready_loop(self):
        while len(self._tyres.compound) < 2:
            time.sleep(0.1)
        self._ready = True
        self.fire(ACData.EVENT.READY)

    # Checks if any values have changed and call the callback functions.
    def update(self, delta: float):
        if self._ready:

            self._timer += delta
            temp_timer = self._timer * 10

            # update every 10 ms
            if temp_timer % 1:
                self._players.update(delta)

                self._flag.value = self._session.flag
                self._fuel.value = self._car.fuel
                self._lap.value = self._timing.lap
                self._sector.value = self._timing.current_sector_index
                self._mini_sector.value = int(self._car.location * 12)
                self._km_sector.value = int(self._car.location * self._environment.track_length / 1000)
                self._km_traveled.value = int(self._car.distance_traveled / 1000)

            # update every 50 ms
            if temp_timer % 5:
                pass

            # update every 100 ms
            if temp_timer % 10:
                # Requires some more accurate calculation.
                self._tyre_wear.value = avg(self._tyres.wear)
                self._tyre_temp.value = avg(self._tyres.outer_temperature)

            # update every 200 ms
            if temp_timer % 20:
                pass

            # update every 300 ms
            if temp_timer % 30:
                self._compound.value = self._tyres.compound

            # update every 500 ms
            if temp_timer % 50:
                self._position.value = self._car.position
                self._is_in_pit.value = self._car.is_in_pit
                self._is_in_pitline.value = self._car.is_in_pit_line
                self._has_penalty.value = self._car.has_penalty
                self._is_lap_valid.value = self._timing.valid_lap

            # update every second
            if self._timer > 1:
                pass

            # update every 5 seconds
            if self._timer > 5:
                self._timer = 0
                self._player_count.value = self._server.slots

    def shutdown(self):
        pass

    @property
    def players(self):
        return self._players

    @property
    def server(self):
        return self._server

    @property
    def driver(self):
        return self._driver

    @property
    def car(self):
        return self._car

    @property
    def tyres(self):
        return self._tyres

    @property
    def session(self):
        return self._session

    @property
    def environment(self):
        return self._environment

    @property
    def timing(self):
        return self._timing

    @property
    def minisector(self):
        return self._mini_sector.value

    @property
    def km(self):
        return self._km_sector.value
