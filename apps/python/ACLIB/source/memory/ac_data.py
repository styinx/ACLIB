import time
from threading import Thread

from memory.sim_info import SimInfo
from memory.data.driver import Driver
from memory.data.car import Car
from memory.data.tyres import Tyres
from memory.data.session import Session
from memory.data.environment import Environment
from memory.data.timing import Timing
from util.event import EventListener


def get_property(obj, property_str: str):
    for sub_property in property_str.split('.'):
        if hasattr(obj, sub_property):
            obj = getattr(obj, sub_property)
    return obj


class Property:
    def __init__(self, parent, value: int, event: str, callback_param: str = ''):
        self._parent = parent
        self._value = value
        self._event = event
        self._callback_param = callback_param

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: int):
        if self._value != new_value:
            self._value = new_value

            if self._callback_param == '':
                self._parent.fire(self._event)
            else:
                self._parent.fire(self._event, get_property(self._parent, self._callback_param))


class BoolProperty:
    def __init__(self, parent, value: bool, event1: str, event2: str):
        self._parent = parent
        self._value = value
        self._event1 = event1
        self._event2 = event2

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: bool):
        if self._value != new_value:
            self._value = new_value
            if self._value:
                self._parent.fire(self._event1)
            else:
                self._parent.fire(self._event2)


class ACData(EventListener):
    class EVENT:
        READY = 'READY'
        LAP_CHANGED = 'Lap Changed'
        SECTOR_CHANGED = 'Sector Changed'
        MINISECTOR_CHANGED = 'Minisector Changed'
        KM_CHANGED = 'KM Changed'
        POSITION_CHANGED = 'Position Changed'
        POSITION_GAINED = 'Position Gained'
        POSITION_LOST = 'Position Lost'
        FLAG_CHANGED = 'Flag Changed'
        PIT_ENTERED = 'Pit Entered'
        PIT_LEFT = 'Pit Left'
        COMPOUND_CHANGED = 'Compound Changed'
        LAP_INVALIDATED = 'Lap Invalidated'
        PENALTY_RECEIVED = 'Penalty Received'
        PENALTY_SERVED = 'Penalty Served'

    def __init__(self):
        super().__init__()

        self._ready = False

        self._info = SimInfo()
        self._driver = Driver(self._info)
        self._car = Car(self._info)
        self._tyres = Tyres(self._info)
        self._session = Session(self._info)
        self._environment = Environment(self._info)
        self._timing = Timing(self._info)

        self._is_in_pit = BoolProperty(self, False, ACData.EVENT.PIT_ENTERED, ACData.EVENT.PIT_LEFT)
        self._has_penalty = BoolProperty(self, False, ACData.EVENT.PENALTY_RECEIVED, ACData.EVENT.PENALTY_SERVED)
        self._position = Property(self, 0, ACData.EVENT.POSITION_CHANGED)
        self._compound = Property(self, 0, ACData.EVENT.COMPOUND_CHANGED, '_compound.value')
        self._flag = Property(self, 0, ACData.EVENT.FLAG_CHANGED, '_flag.value')
        self._lap = Property(self, 0, ACData.EVENT.LAP_CHANGED, '_lap.value')
        self._sector = Property(self, 0, ACData.EVENT.SECTOR_CHANGED)
        self._mini_sector = Property(self, 0, ACData.EVENT.MINISECTOR_CHANGED)
        self._km_sector = Property(self, 0, ACData.EVENT.KM_CHANGED)

        self._check_ready()

    def _check_ready(self):
        thread = Thread(target=self._check_ready_loop, daemon=True)
        thread.start()

    def _check_ready_loop(self):
        while len(self._tyres.compound) < 5:
            time.sleep(0.1)
        self._fire(ACData.EVENT.READY)
        self._ready = True

    def fire(self, event: str, *args):
        self._fire(event, *args)

    # Checks if any values have changed and call the callback functions.
    def update(self, delta: int):
        if self._ready:
            self._is_in_pit.value = self._car.is_in_pit
            self._has_penalty.value = self._car.has_penalty
            self._position.value = self._car.position
            self._flag.value = self._session.flag
            self._lap.value = self._timing.lap
            self._sector.value = self._timing.current_sector_index
            # self._mini_sector.value = self._car.position
            # self._km_sector.value = self._car.position

            self._compound.value = self._tyres.compound

            # Only check when car is in the box.
            if self._is_in_pit:
                self._compound.value = self._tyres.compound

    def shutdown(self):
        pass

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
#
#         # # Time and Distance to next and previous cars (relative and absolute)
#         min_prev = float('-inf')
#         min_next = float('inf')
#         for c in range(0, ACLIB.getCarsCount()):
#             if c != self.number:
#                 lap = self.lap
#                 pos = self.location
#                 track_len = ACLIB.getTrackLength()
#                 c_pos = ACLIB.getLocation(c)
#                 c_lap = ACLIB.getLap(c)
#
#                 if min_next > c_pos - self.location > 0:
#                     min_next = c_pos - self.location
#                     self.rel_next = c
#                     self.rel_next_dist = max(0, ((c_pos + c_lap) * track_len) - ((pos + lap) * track_len))
#                     self.rel_next_time = max(0.0, self.rel_next_dist / max(10.0, ACLIB.getSpeed(self.number, 'ms')))
#
#                 if min_prev < c_pos - self.location < 0:
#                     min_prev = c_pos - self.location
#                     self.rel_prev = c
#                     self.rel_prev_dist = max(0, ((pos + lap) * track_len) - ((c_pos + c_lap) * track_len))
#                     self.rel_prev_time = max(0.0, self.rel_prev_dist / max(10.0, ACLIB.getSpeed(self.number, 'ms')))
#
#                 if ACLIB.getPosition(c) == self.position - 1:
#                     self.next = c
#                     self.next_dist = max(0, ((c_pos + c_lap) * track_len) - ((pos + lap) * track_len))
#                     self.next_time = max(0.0, self.next_dist / max(10.0, ACLIB.getSpeed(self.number, 'ms')))
#
#                 elif ACLIB.getPosition(c) == self.position + 1:
#                     self.prev = c
#                     self.prev_dist = max(0, ((pos + lap) * track_len) - ((c_pos + c_lap) * track_len))
#                     self.prev_time = max(0.0, self.prev_dist / max(10.0, ACLIB.getSpeed(self.number, 'ms')))
#
#         # invalid Lap
#         invalid = ACLIB.isLapInvalidated(self.number)
#         if invalid != self.lap_invalid and not self.lap_invalid:
#             self.lap_invalid = invalid
#
#             self.dispatchEvent(LIB_EVENT.ON_LAP_INVALIDATED)
#
#         # Next lap
#         lap = ACLIB.getLap(self.number)
#         if lap != self.lap:
#
#             self.benefit = 0
#
#             if self.lap_time == self.best_time:
#                 self.best_performance = self.last_performance
#
#             self.last_performance = self.lap_performance
#             self.lap_performance = {}
#             self.last_invalid = self.lap_invalid
#             self.lap_invalid = False
#             self.lap = ACLIB.getLap(self.number)
#             self.last_time = ACLIB.getLastLapTime(self.number)
#             self.best_time = ACLIB.getBestLapTime(self.number)
#
#             if not self.last_invalid and 0 < self.last_time < SESSION.best_lap_time and lap > 1:
#                 SESSION.best_lap_time = self.last_time
#
#             self.last_sector_time = self.sector_time
#             self.last_sector_time[2] = self.last_time - sum(self.sector_time[:2])
#             self.last_mini_sector_time = self.mini_sector_time
#             self.last_mini_sector_time[11] = self.last_time - sum(self.mini_sector_time[:11])
#             self.last_km_time = self.km_time
#             self.last_km_time[int(ACLIB.getTrackLength() / 1000)] = self.last_time - sum(
#                 self.km_time[:int(ACLIB.getTrackLength() / 1000)])
#
#             if self.lap_fuel_level - self.fuel > 0:
#                 self.lap_fuel = self.lap_fuel_level - self.fuel
#                 self.lap_fuel_range = self.fuel / self.lap_fuel
#                 self.lap_fuel_level = self.fuel
#
#             self.dispatchEvent(LIB_EVENT.ON_LAP_CHANGED)
#
#         # Next sector
#         sector = min(int(self.location * 3.33), 2)
#         if sector != self.sector_index:
#             sector_time = 0
#
#             if sector == 0:
#                 self.last_sector_time[2] = self.last_time - sum(self.last_sector_time[:2])
#             else:
#                 sector_time = self.lap_time - sum(self.sector_time[:self.sector_index])
#                 self.sector_time[self.sector_index] = sector_time
#
#             if 0 < sector_time < self.best_sector_time[self.sector_index] and self.lap > 1:
#                 self.best_sector_time[self.sector_index] = sector_time
#
#                 # if sector_time < SESSION.best_sector_time[self.sector_index]:
#                 #     SESSION.best_sector_time[self.sector_index] = sector_time
#
#             if self.sector_fuel_level - self.fuel > 0:
#                 self.sector_fuel = self.sector_fuel_level - self.fuel
#                 self.sector_fuel_range = self.fuel / self.sector_fuel
#                 self.sector_fuel_level = self.fuel
#
#             self.sector_index = sector
#             self.sector = sector + 1
#             self.dispatchEvent(LIB_EVENT.ON_SECTOR_CHANGED)
#
#         mini_sector = min(int(self.location * 12), 11)
#         if mini_sector != self.mini_sector_index:
#
#             mini_sector_time = 0
#
#             if mini_sector == 0:
#                 self.last_mini_sector_time[11] = self.last_time - sum(self.last_mini_sector_time[:11])
#             else:
#                 mini_sector_time = self.lap_time - sum(self.mini_sector_time[:self.mini_sector_index])
#                 self.mini_sector_time[self.mini_sector_index] = mini_sector_time
#
#             if 0 < mini_sector_time < self.best_mini_sector_time[self.mini_sector_index] and self.lap > 1:
#                 self.best_mini_sector_time[self.mini_sector_index] = mini_sector_time
#
#                 # if mini_sector_time < SESSION.best_mini_sector_time[self.mini_sector_index]:
#                 #     SESSION.best_mini_sector_time[self.mini_sector_index] = mini_sector_time
#
#             if self.mini_sector_fuel_level - self.fuel > 0:
#                 self.mini_sector_fuel = self.mini_sector_fuel_level - self.fuel
#                 self.mini_sector_fuel_range = self.fuel / self.mini_sector_fuel
#                 self.mini_sector_fuel_level = self.fuel
#
#             self.mini_sector_index = mini_sector
#             self.mini_sector = mini_sector + 1
#             self.dispatchEvent(LIB_EVENT.ON_MINISECTOR_CHANGED)
#
#         # Next km
#         km = int(self.location * ACLIB.getTrackLength() / 1000)
#         if km != self.km_index:
#
#             km_time = 0
#
#             if km == 0:
#                 index = int(ACLIB.getTrackLength() / 1000) - 1
#                 self.last_km_time[index] = self.last_time - sum(self.last_km_time[:index])
#             else:
#                 km_time = self.lap_time - sum(self.km_time[:self.km_index])
#                 self.km_time[self.km_index] = km_time
#
#             self.km_time[self.km_index] = km_time
#             self.last_km_time[self.km_index] = km_time
#             if 0 < km_time < self.best_km_time[self.km_index] and self.lap > 1:
#                 self.best_km_time[self.km_index] = km_time
#
#                 # if km_time < SESSION.best_km_time[self.km_index]:
#                 #     SESSION.best_km_time[self.km_index] = km_time
#
#             if self.km_fuel_level - self.fuel > 0:
#                 self.km_fuel = self.km_fuel_level - self.fuel
#                 self.km_fuel_range = self.fuel / self.km_fuel
#                 self.km_fuel_level = self.fuel
#                 self.fuel_session = max(ACLIB.getLaps() - self.lap, 1) * ACLIB.getTrackLength() / 1000 * self.km_fuel
#
#             self.km_index = km
#             self.km = km + 1
#             self.dispatchEvent(LIB_EVENT.ON_KM_CHANGED)
#
#
# class ACLIB:
#     @staticmethod
#     def getRaceTimeLeftFormated():
#         time = ACLIB.getRaceTimeLeft()
#
#         if not isinf(time):
#             if ACLIB.isTimedRace():
#                 return 'time left: ' + Format.time(time)
#             elif time > 0:
#                 return 'next session in: ' + Format.time(time)
#         return ''
#
#     @staticmethod
#     def getSector(car=0, form=None):
#         return int(ACLIB.getLocation(car) * 3.33)
#
#     @staticmethod
#     def getMiniSector(car=0, form=None):
#         return int(ACLIB.getLocation(car) * 12)
#
#     @staticmethod
#     def getKm(car=0, form=None):
#         return int(ACLIB.getLocation(car) * ACLIB.getTrackLength() / 1000)
#
#     @staticmethod
#     def getLapDeltaTime(car=0, form=None):
#         return ac.getCarState(car, AC_PROP.PerformanceMeter)
#
#     @staticmethod
#     def getLapDelta(car=0):
#         if car == ACLIB.getFocusedCar():
#             time = ACLIB.getLapDeltaTime(car) * 1000
#             if time != 0:
#                 if time < 0:
#                     return '-' + Format.time(abs(time))
#                 elif time > 0:
#                     return '+' + Format.time(abs(time))
#             else:
#                 return '-00:00.000'
#         else:
#             return -1
#
#     @staticmethod
#     def isLapInvalidated(car=0):
#         return ac.getCarState(car, AC_PROP.LapInvalidated) or ACLIB.getTyresOut(car) > 2 or ACLIB.isInPit(car)
#
#     @staticmethod
#     def getCarSuspensionDamage(car=0, tyre=0, form=None):
#         if car == ACLIB.getFocusedCar():
#             travel = ACLIB.getSuspensionTravel(car, tyre=tyre)
#             travel_max = ACLIB.getMaxSuspensionTravel(car, tyre=tyre)
#             if form:
#                 return form.format(travel / max(1, travel_max))
#             return travel / max(1, travel_max)
#         else:
#             return -1
#
#     # other cars
#
#     @staticmethod
#     def getPrevCarDiffTimeDist(car=0, form=None):
#         if car == ACLIB.getFocusedCar():
#             time = 0
#             dist = 0
#             track_len = ACLIB.getTrackLength()
#             lap = ACLIB.getLap(0)
#             pos = ACLIB.getLocation(0)
#
#             for car in range(ACLIB.getCarsCount()):
#                 if ACLIB.getPosition(car) == ACLIB.getPosition(0) - 1:
#                     lap_next = ACLIB.getLap(car)
#                     pos_next = ACLIB.getLocation(car)
#
#                     dist = max(0, (pos_next * track_len + lap_next * track_len) - (pos * track_len + lap * track_len))
#                     time = max(0.0, dist / max(10.0, ACLIB.getSpeed(0, 'ms')))
#                     break
#             if form:
#                 if dist > track_len:
#                     laps = dist / max(track_len, 1)
#                     if laps > 1:
#                         return '+{:3.1f}'.format(laps) + ' Laps'
#                     else:
#                         return '+{:3.1f}'.format(laps) + '   Lap'
#                 else:
#                     if time > 60:
#                         minute = time / 60
#                         if minute > 1.05:
#                             return '+{:3.1f}'.format(minute) + ' Mins'
#                         elif minute < 1.05:
#                             return '+{:3.0f}'.format(minute) + '   Min'
#                     else:
#                         return '+' + Format.time(int(time * 1000))
#             return time, dist
#         else:
#             return -1
#
#     @staticmethod
#     def getNextCarDiffTimeDist(car=0, form=None):
#         if car == ACLIB.getFocusedCar():
#             time = 0
#             dist = 0
#             track_len = ACLIB.getTrackLength()
#             lap = ACLIB.getLap(0)
#             pos = ACLIB.getLocation(0)
#
#             for car in range(ACLIB.getCarsCount()):
#                 if ACLIB.getPosition(car) == ACLIB.getPosition(0) + 1:
#                     lap_next = ACLIB.getLap(car)
#                     pos_next = ACLIB.getLocation(car)
#
#                     dist = max(0.0, (pos * track_len + lap * track_len) - (pos_next * track_len + lap_next * track_len))
#                     time = max(0.0, dist / max(10.0, ACLIB.getSpeed(car, 'ms')))
#                     break
#             if form:
#                 if dist > track_len:
#                     laps = dist / max(track_len, 1)
#                     if laps > 1:
#                         return '-{:3.1f}'.format(laps) + ' Laps'
#                     else:
#                         return '-{:3.1f}'.format(laps) + '   Lap'
#                 else:
#                     if time > 60:
#                         minute = time / 60
#                         if minute > 1.05:
#                             return '-{:3.1f}'.format(minute) + ' Mins'
#                         elif minute < 1.05:
#                             return '-{:3.0f}'.format(minute) + '   Min'
#                     else:
#                         return '-' + Format.time(int(time * 1000))
#             return time, dist
#         else:
#             return -1
