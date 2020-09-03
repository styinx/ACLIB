import sys
import os
import platform
from math import isinf
import ac

from util.util import Format

if platform.architecture()[0] == '64bit':
    sysdir = os.path.dirname(__file__) + '/../stdlib64'
else:
    sysdir = os.path.dirname(__file__) + '/../stdlib'

sys.path.insert(0, sysdir)
sys.path.insert(0, os.path.dirname(__file__) + '/../third_party')
os.environ['PATH'] = os.environ['PATH'] + ';.'

from source.memory.sim_info import SimInfo, AC_PROP
from source.memory.driver import Driver
from source.memory.car import Car
from source.memory.session import Session
from source.memory.environment import Environment

info = SimInfo()
driver = Driver(info)
car = Car(info)
session = Session(info)
environment = Environment(info)


class LIB_EVENT:
    ON_LAP_CHANGED = 0
    ON_SECTOR_CHANGED = 1
    ON_MINISECTOR_CHANGED = 2
    ON_KM_CHANGED = 3
    ON_POSITION_CHANGED = 4
    ON_POSITION_GAINED = 5
    ON_POSITION_LOST = 6
    ON_FLAG_CHANGED = 7
    ON_PIT_ENTERED = 8
    ON_PIT_LEFT = 9
    ON_COMPOUND_CHANGED = 10
    ON_LAP_INVALIDATED = 11
    ON_PENALTY_RECEIVED = 12


class Car:
    def __init__(self, number):
        self.priority = 10  # more means a higher effort to compute but more precise results
        self.timer = 0
        self.loops = 0
        self.initialized = False
        self.max_delta = 0.2  # 0.02
        self.last_interval = 0
        self.events = {}

        self.number = number
        self.player_name = ''
        self.player_nick = ''
        self.car_skin = ''
        self.car_id = ''
        self.car_name = ''
        self.car_brand = ''
        self.car_badge = ''
        self.car_class = ''
        self.car_type = ''
        self.drs = False
        self.ers = False
        self.kers = False

        self.gear = 0  # gear
        self.rpm = 0  # rpm
        self.max_rpm = 0  # max rpm
        self.speed = 0.0  # standings
        self.position = 0  # standings
        self.class_position = 0  # relative standings
        self.benefit = 0  # position gain/loss per lap
        self.location = 0.0  # track position from 0 to 1
        self.traveled_distance = 0.0  # in m
        self.fuel = 0.0  # in l
        self.max_fuel = 0.0  # in l
        self.flag = 0
        self.in_pit = False
        self.penalty = False
        self.penalty_time = 0.0
        self.abs = 0.0
        self.tc = 0.0

        self.next = 0
        self.next_dist = 0
        self.next_time = 0
        self.rel_next = 0
        self.rel_next_dist = 0
        self.rel_next_time = 0
        self.prev = 0
        self.prev_dist = 0
        self.prev_time = 0
        self.rel_prev = 0
        self.rel_prev_dist = 0
        self.rel_prev_time = 0

        self.performance_location = 0
        self.performance = 0  # time at specific location compared to last / best
        self.lap_performance = {}
        self.last_performance = {}
        self.best_performance = {}
        self.lap = 0  # current lap
        self.lap_invalid = False  # 4 tyres out of track
        self.lap_diff = 0.0  # performance meter
        self.lap_time = 0.0  # current lap time
        self.last_time = 0.0  # last lap time
        self.last_invalid = False
        self.best_time = 0.0  # best lap time
        self.fuel_session = 0.0  # fuel needed to end session
        self.lap_fuel = 0.0  # fuel consumption in l
        self.lap_fuel_range = 0.0  # number of laps with current fuel
        self.lap_fuel_level = 0.0  # fuel level from last lap

        self.sector = 0
        self.sector_index = 0
        self.sector_time = [0.0] * 3
        self.last_sector_time = [0.0] * 3
        self.best_sector_time = [float('inf')] * 3
        self.sector_fuel = 0.0
        self.sector_fuel_range = 0.0
        self.sector_fuel_level = 0.0

        self.mini_sector = 0
        self.mini_sector_index = 0
        self.mini_sector_time = [0.0] * 12
        self.last_mini_sector_time = [0.0] * 12
        self.best_mini_sector_time = [float('inf')] * 12
        self.mini_sector_fuel = 0.0
        self.mini_sector_fuel_range = 0.0
        self.mini_sector_fuel_level = 0.0

        self.km = 0
        self.km_index = 0
        self.km_time = [0.0] * (int(ACLIB.getTrackLength() / 1000) + 2)
        self.last_km_time = [0.0] * (int(ACLIB.getTrackLength() / 1000) + 2)
        self.best_km_time = [float('inf')] * (int(ACLIB.getTrackLength() / 1000) + 2)
        self.km_fuel = 0.0
        self.km_fuel_range = 0.0
        self.km_fuel_level = 0.0

        self.damage_body = [0.0] * 4  # 0: front, 1: rear, 2: left, 3: right
        self.damage_suspension = [0.0] * 4  # 0: FL, 1: FR, 2: RL, 3: RR

        self.is_init = False

    def setEvent(self, event, callback):
        if event in self.events:
            self.events[event].append(callback)
        else:
            self.events[event] = []
            self.events[event].append(callback)

    def dispatchEvent(self, event):
        if event in self.events:
            for callback in self.events[event]:
                callback(self.number)

    def update(self, delta):
        self.loops += 1
        if not self.is_init and self.loops > 100:
            self.is_init = True
            self.init()

        # performance
        self.performance_location = round(self.location * ACLIB.getTrackLength() * 5)
        loc = self.performance_location

        if loc not in self.last_performance:
            self.last_performance[loc] = self.speed

        if loc not in self.best_performance:
            self.best_performance[loc] = self.speed

        if loc not in self.lap_performance:
            self.lap_performance[loc] = self.speed

        self.performance = self.best_performance[loc] - self.lap_performance[loc]

        # init components that require shared memory to be loaded
        # init fuel
        if self.lap_fuel_level <= 0:
            self.lap_fuel_level = self.fuel
        if self.sector_fuel_level <= 0:
            self.sector_fuel_level = self.fuel
        if self.mini_sector_fuel_level <= 0:
            self.mini_sector_fuel_level = self.fuel
        if self.km_fuel_level <= 0:
            self.km_fuel_level = self.fuel

        # check penalty
        if self.penalty_time > 0:
            self.penalty = True

            self.dispatchEvent(LIB_EVENT.ON_PENALTY_RECEIVED)
        else:
            self.penalty = False

        # flag
        flag = ACLIB.getFlagId()
        if flag != self.flag:
            self.flag = flag
            self.dispatchEvent(LIB_EVENT.ON_FLAG_CHANGED)

        # pit
        is_in_pit = ACLIB.isInPit(self.number)
        # TODO
        was_in_pit = True
        if is_in_pit and not was_in_pit:
            if self.tyre_compound != ACLIB.getTyreCompund(symbol=False):
                self.tyre_compound = ACLIB.getTyreCompund(symbol=False)
                self.tyre_compound_symbol = ACLIB.getTyreCompund()

                self.dispatchEvent(LIB_EVENT.ON_COMPOUND_CHANGED)

        if is_in_pit and not self.in_pit:
            self.in_pit = is_in_pit

            self.dispatchEvent(LIB_EVENT.ON_PIT_ENTERED)

        else:
            self.in_pit = is_in_pit

            self.dispatchEvent(LIB_EVENT.ON_PIT_LEFT)

        # Position changed
        position = ACLIB.getPosition(self.number)
        if position != self.position:
            self.benefit += self.position - position
            temp = self.position
            self.position = position

            if temp - position > 0:
                self.dispatchEvent(LIB_EVENT.ON_POSITION_GAINED)
            else:
                self.dispatchEvent(LIB_EVENT.ON_POSITION_LOST)

            self.dispatchEvent(LIB_EVENT.ON_POSITION_CHANGED)

        # # Time and Distance to next and previous cars (relative and absolute)
        min_prev = float('-inf')
        min_next = float('inf')
        for c in range(0, ACLIB.getCarsCount()):
            if c != self.number:
                lap = self.lap
                pos = self.location
                track_len = ACLIB.getTrackLength()
                c_pos = ACLIB.getLocation(c)
                c_lap = ACLIB.getLap(c)

                if min_next > c_pos - self.location > 0:
                    min_next = c_pos - self.location
                    self.rel_next = c
                    self.rel_next_dist = max(0, ((c_pos + c_lap) * track_len) - ((pos + lap) * track_len))
                    self.rel_next_time = max(0.0, self.rel_next_dist / max(10.0, ACLIB.getSpeed(self.number, 'ms')))

                if min_prev < c_pos - self.location < 0:
                    min_prev = c_pos - self.location
                    self.rel_prev = c
                    self.rel_prev_dist = max(0, ((pos + lap) * track_len) - ((c_pos + c_lap) * track_len))
                    self.rel_prev_time = max(0.0, self.rel_prev_dist / max(10.0, ACLIB.getSpeed(self.number, 'ms')))

                if ACLIB.getPosition(c) == self.position - 1:
                    self.next = c
                    self.next_dist = max(0, ((c_pos + c_lap) * track_len) - ((pos + lap) * track_len))
                    self.next_time = max(0.0, self.next_dist / max(10.0, ACLIB.getSpeed(self.number, 'ms')))

                elif ACLIB.getPosition(c) == self.position + 1:
                    self.prev = c
                    self.prev_dist = max(0, ((pos + lap) * track_len) - ((c_pos + c_lap) * track_len))
                    self.prev_time = max(0.0, self.prev_dist / max(10.0, ACLIB.getSpeed(self.number, 'ms')))

        # invalid Lap
        invalid = ACLIB.isLapInvalidated(self.number)
        if invalid != self.lap_invalid and not self.lap_invalid:
            self.lap_invalid = invalid

            self.dispatchEvent(LIB_EVENT.ON_LAP_INVALIDATED)

        # Next lap
        lap = ACLIB.getLap(self.number)
        if lap != self.lap:

            self.benefit = 0

            if self.lap_time == self.best_time:
                self.best_performance = self.last_performance

            self.last_performance = self.lap_performance
            self.lap_performance = {}
            self.last_invalid = self.lap_invalid
            self.lap_invalid = False
            self.lap = ACLIB.getLap(self.number)
            self.last_time = ACLIB.getLastLapTime(self.number)
            self.best_time = ACLIB.getBestLapTime(self.number)

            if not self.last_invalid and 0 < self.last_time < SESSION.best_lap_time and lap > 1:
                SESSION.best_lap_time = self.last_time

            self.last_sector_time = self.sector_time
            self.last_sector_time[2] = self.last_time - sum(self.sector_time[:2])
            self.last_mini_sector_time = self.mini_sector_time
            self.last_mini_sector_time[11] = self.last_time - sum(self.mini_sector_time[:11])
            self.last_km_time = self.km_time
            self.last_km_time[int(ACLIB.getTrackLength() / 1000)] = self.last_time - sum(
                self.km_time[:int(ACLIB.getTrackLength() / 1000)])

            if self.lap_fuel_level - self.fuel > 0:
                self.lap_fuel = self.lap_fuel_level - self.fuel
                self.lap_fuel_range = self.fuel / self.lap_fuel
                self.lap_fuel_level = self.fuel

            self.dispatchEvent(LIB_EVENT.ON_LAP_CHANGED)

        # Next sector
        sector = min(int(self.location * 3.33), 2)
        if sector != self.sector_index:
            sector_time = 0

            if sector == 0:
                self.last_sector_time[2] = self.last_time - sum(self.last_sector_time[:2])
            else:
                sector_time = self.lap_time - sum(self.sector_time[:self.sector_index])
                self.sector_time[self.sector_index] = sector_time

            if 0 < sector_time < self.best_sector_time[self.sector_index] and self.lap > 1:
                self.best_sector_time[self.sector_index] = sector_time

                # if sector_time < SESSION.best_sector_time[self.sector_index]:
                #     SESSION.best_sector_time[self.sector_index] = sector_time

            if self.sector_fuel_level - self.fuel > 0:
                self.sector_fuel = self.sector_fuel_level - self.fuel
                self.sector_fuel_range = self.fuel / self.sector_fuel
                self.sector_fuel_level = self.fuel

            self.sector_index = sector
            self.sector = sector + 1
            self.dispatchEvent(LIB_EVENT.ON_SECTOR_CHANGED)

        mini_sector = min(int(self.location * 12), 11)
        if mini_sector != self.mini_sector_index:

            mini_sector_time = 0

            if mini_sector == 0:
                self.last_mini_sector_time[11] = self.last_time - sum(self.last_mini_sector_time[:11])
            else:
                mini_sector_time = self.lap_time - sum(self.mini_sector_time[:self.mini_sector_index])
                self.mini_sector_time[self.mini_sector_index] = mini_sector_time

            if 0 < mini_sector_time < self.best_mini_sector_time[self.mini_sector_index] and self.lap > 1:
                self.best_mini_sector_time[self.mini_sector_index] = mini_sector_time

                # if mini_sector_time < SESSION.best_mini_sector_time[self.mini_sector_index]:
                #     SESSION.best_mini_sector_time[self.mini_sector_index] = mini_sector_time

            if self.mini_sector_fuel_level - self.fuel > 0:
                self.mini_sector_fuel = self.mini_sector_fuel_level - self.fuel
                self.mini_sector_fuel_range = self.fuel / self.mini_sector_fuel
                self.mini_sector_fuel_level = self.fuel

            self.mini_sector_index = mini_sector
            self.mini_sector = mini_sector + 1
            self.dispatchEvent(LIB_EVENT.ON_MINISECTOR_CHANGED)

        # Next km
        km = int(self.location * ACLIB.getTrackLength() / 1000)
        if km != self.km_index:

            km_time = 0

            if km == 0:
                index = int(ACLIB.getTrackLength() / 1000) - 1
                self.last_km_time[index] = self.last_time - sum(self.last_km_time[:index])
            else:
                km_time = self.lap_time - sum(self.km_time[:self.km_index])
                self.km_time[self.km_index] = km_time

            self.km_time[self.km_index] = km_time
            self.last_km_time[self.km_index] = km_time
            if 0 < km_time < self.best_km_time[self.km_index] and self.lap > 1:
                self.best_km_time[self.km_index] = km_time

                # if km_time < SESSION.best_km_time[self.km_index]:
                #     SESSION.best_km_time[self.km_index] = km_time

            if self.km_fuel_level - self.fuel > 0:
                self.km_fuel = self.km_fuel_level - self.fuel
                self.km_fuel_range = self.fuel / self.km_fuel
                self.km_fuel_level = self.fuel
                self.fuel_session = max(ACLIB.getLaps() - self.lap, 1) * ACLIB.getTrackLength() / 1000 * self.km_fuel

            self.km_index = km
            self.km = km + 1
            self.dispatchEvent(LIB_EVENT.ON_KM_CHANGED)


class ACLIB:
    @staticmethod
    def getRaceTimeLeftFormated():
        time = ACLIB.getRaceTimeLeft()

        if not isinf(time):
            if ACLIB.isTimedRace():
                return 'time left: ' + Format.time(time)
            elif time > 0:
                return 'next session in: ' + Format.time(time)
        return ''



    @staticmethod
    def getSector(car=0, form=None):
        return int(ACLIB.getLocation(car) * 3.33)

    @staticmethod
    def getMiniSector(car=0, form=None):
        return int(ACLIB.getLocation(car) * 12)

    @staticmethod
    def getKm(car=0, form=None):
        return int(ACLIB.getLocation(car) * ACLIB.getTrackLength() / 1000)

    @staticmethod
    def getLapDeltaTime(car=0, form=None):
        return ac.getCarState(car, AC_PROP.PerformanceMeter)

    @staticmethod
    def getLapDelta(car=0):
        if car == ACLIB.getFocusedCar():
            time = ACLIB.getLapDeltaTime(car) * 1000
            if time != 0:
                if time < 0:
                    return '-' + Format.time(abs(time))
                elif time > 0:
                    return '+' + Format.time(abs(time))
            else:
                return '-00:00.000'
        else:
            return -1

    @staticmethod
    def isLapInvalidated(car=0):
        return ac.getCarState(car, AC_PROP.LapInvalidated) or ACLIB.getTyresOut(car) > 2 or ACLIB.isInPit(car)

    @staticmethod
    def getCarSuspensionDamage(car=0, tyre=0, form=None):
        if car == ACLIB.getFocusedCar():
            travel = ACLIB.getSuspensionTravel(car, tyre=tyre)
            travel_max = ACLIB.getMaxSuspensionTravel(car, tyre=tyre)
            if form:
                return form.format(travel / max(1, travel_max))
            return travel / max(1, travel_max)
        else:
            return -1
    # other cars

    @staticmethod
    def getPrevCarDiffTimeDist(car=0, form=None):
        if car == ACLIB.getFocusedCar():
            time = 0
            dist = 0
            track_len = ACLIB.getTrackLength()
            lap = ACLIB.getLap(0)
            pos = ACLIB.getLocation(0)

            for car in range(ACLIB.getCarsCount()):
                if ACLIB.getPosition(car) == ACLIB.getPosition(0) - 1:
                    lap_next = ACLIB.getLap(car)
                    pos_next = ACLIB.getLocation(car)

                    dist = max(0, (pos_next * track_len + lap_next * track_len) - (pos * track_len + lap * track_len))
                    time = max(0.0, dist / max(10.0, ACLIB.getSpeed(0, 'ms')))
                    break
            if form:
                if dist > track_len:
                    laps = dist / max(track_len, 1)
                    if laps > 1:
                        return '+{:3.1f}'.format(laps) + ' Laps'
                    else:
                        return '+{:3.1f}'.format(laps) + '   Lap'
                else:
                    if time > 60:
                        minute = time / 60
                        if minute > 1.05:
                            return '+{:3.1f}'.format(minute) + ' Mins'
                        elif minute < 1.05:
                            return '+{:3.0f}'.format(minute) + '   Min'
                    else:
                        return '+' + Format.time(int(time * 1000))
            return time, dist
        else:
            return -1

    @staticmethod
    def getNextCarDiffTimeDist(car=0, form=None):
        if car == ACLIB.getFocusedCar():
            time = 0
            dist = 0
            track_len = ACLIB.getTrackLength()
            lap = ACLIB.getLap(0)
            pos = ACLIB.getLocation(0)

            for car in range(ACLIB.getCarsCount()):
                if ACLIB.getPosition(car) == ACLIB.getPosition(0) + 1:
                    lap_next = ACLIB.getLap(car)
                    pos_next = ACLIB.getLocation(car)

                    dist = max(0.0, (pos * track_len + lap * track_len) - (pos_next * track_len + lap_next * track_len))
                    time = max(0.0, dist / max(10.0, ACLIB.getSpeed(car, 'ms')))
                    break
            if form:
                if dist > track_len:
                    laps = dist / max(track_len, 1)
                    if laps > 1:
                        return '-{:3.1f}'.format(laps) + ' Laps'
                    else:
                        return '-{:3.1f}'.format(laps) + '   Lap'
                else:
                    if time > 60:
                        minute = time / 60
                        if minute > 1.05:
                            return '-{:3.1f}'.format(minute) + ' Mins'
                        elif minute < 1.05:
                            return '-{:3.0f}'.format(minute) + '   Min'
                    else:
                        return '-' + Format.time(int(time * 1000))
            return time, dist
        else:
            return -1
