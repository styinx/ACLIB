import sys
import os
import platform
from math import isinf
import ac
from source.event import LIB_EVENT
from source.gl import Texture

if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__) + '/../stdlib64'
else:
    sysdir = os.path.dirname(__file__) + '/../stdlib'

sys.path.insert(0, sysdir)
sys.path.insert(0, os.path.dirname(__file__) + '/../third_party')
os.environ['PATH'] = os.environ['PATH'] + ";."

from third_party.sim_info import info, AC_PROP


def pad(number, pos=2):
    return ("{:0" + str(pos) + "}").format(number)


def s(value, term):
    if abs(value) == 1:
        return str(value) + term
    else:
        return str(value) + term + "s"


def formatTime(millis, form="{:02d}:{:02d}.{:03d}"):
    millis = abs(int(millis))
    m = int(millis / 60000)
    s = int((millis % 60000) / 1000)
    ms = millis % 1000

    return form.format(m, s, ms)


def formatTimeCar(time, dist, track_len):
    if dist > track_len:
        laps = dist / track_len
        if laps > 1.05:
            return "{:3.1f}".format(laps) + " Laps"
        elif laps < 1.05:
            return "{:3.0f}".format(laps) + "   Lap"
    else:
        if time > 60:
            minute = time / 60
            if minute > 1.05:
                return "{:3.1f}".format(minute) + " Mins"
            elif minute < 1.05:
                return "{:3.0f}".format(minute) + "   Min"
        else:
            return formatTime(int(time * 1000))


def formatDistance(meters, form="{:02d}.{:02.0f} km"):
    km = int(meters / 1000)
    m = (meters % 1000) / 10

    return form.format(km, m)


def formatGear(gear):
    if gear == 0:
        return "R"
    elif gear == 1:
        return "N"
    else:
        return str(gear - 1)


class SESSION:
    air_temp = 0
    track_temp = 0
    track_length = 0
    wind_direction = 0
    wind_speed = 0

    time_left = 0

    best_lap_time = float("inf")
    best_sector_time = [float("inf")] * 3
    best_mini_sector_time = [float("inf")] * 12
    best_km_time = [float("inf")] * 1

    @staticmethod
    def init():
        SESSION.air_temp = ACLIB.getAirTemp()
        SESSION.track_temp = ACLIB.getRoadTemp()
        SESSION.track_length = ACLIB.getTrackLength()
        SESSION.wind_direction = ACLIB.getWindDirection()
        SESSION.wind_speed = ACLIB.getWindSpeed()

        SESSION.time_left = ACLIB.getRaceTimeLeft()
        SESSION.best_km_time = [float("inf")] * (int(SESSION.track_length / 1000) + 1)

    @staticmethod
    def update():
        SESSION.time_left = ACLIB.getRaceTimeLeft()


class Car:
    def __init__(self, number):
        self.priority = 10  # more means a higher effort to compute but more precise results
        self.loops = 0
        self.initialized = False
        self.max_delta = 0.2  # 0.02
        self.last_interval = 0
        self.events = {}

        self.number = number
        self.player_name = ""
        self.player_nick = ""
        self.car_skin = ""
        self.car_id = ""
        self.car_name = ""
        self.car_brand = ""
        self.car_badge = ""
        self.car_class = ""
        self.car_type = ""
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

        self.performance = {}  # time difference for intervals of x
        self.lap = 0  # current lap
        self.lap_diff = 0.0  # performance meter
        self.lap_time = 0.0  # current lap time
        self.last_time = 0.0  # last lap time
        self.best_time = 0.0  # best lap time
        self.lap_fuel = 0.0  # fuel consumption in l
        self.lap_fuel_range = 0.0  # number of laps with current fuel
        self.lap_fuel_level = 0.0  # fuel level from last lap

        self.sector = 0
        self.sector_index = 0
        self.sector_time = [0.0] * 3
        self.last_sector_time = [0.0] * 3
        self.best_sector_time = [float("inf")] * 3
        self.sector_fuel = 0.0
        self.sector_fuel_range = 0.0
        self.sector_fuel_level = 0.0

        self.mini_sector = 0
        self.mini_sector_index = 0
        self.mini_sector_time = [0.0] * 12
        self.last_mini_sector_time = [0.0] * 12
        self.best_mini_sector_time = [float("inf")] * 12
        self.mini_sector_fuel = 0.0
        self.mini_sector_fuel_range = 0.0
        self.mini_sector_fuel_level = 0.0

        self.km = 0
        self.km_index = 0
        self.km_time = [0.0] * (int(ACLIB.getTrackLength() / 1000) + 1)
        self.last_km_time = [0.0] * (int(ACLIB.getTrackLength() / 1000) + 1)
        self.best_km_time = [float("inf")] * (int(ACLIB.getTrackLength() / 1000) + 1)
        self.km_fuel = 0.0
        self.km_fuel_range = 0.0
        self.km_fuel_level = 0.0

        self.damage = [0.0] * 4  # 0: front, 1: rear, 2: left, 3: right
        self.tyre_temp = [0.0] * 4  # 0: FL, 1: FR, 2: RL, 3: RR
        self.tyre_dirt = [0.0] * 4
        self.tyre_wear = [0.0] * 4
        self.tyre_pressure = [0.0] * 4
        self.tyre_compound = ""
        self.tyre_compound_symbol = ""

        self.init()

    def reset(self):
        self.gear = 0
        self.rpm = 0
        self.max_rpm = 0
        self.speed = 0.0
        self.position = 0
        self.class_position = 0
        self.benefit = 0
        self.location = 0.0
        self.traveled_distance = 0.0
        self.fuel = 0.0
        self.flag = 0
        self.in_pit = False
        self.penalty = False
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

        self.performance = {}
        self.lap = 0
        self.lap_diff = 0.0
        self.lap_time = 0.0
        self.last_time = 0.0
        self.best_time = 0.0
        self.lap_fuel = 0.0
        self.lap_fuel_range = 0.0
        self.lap_fuel_level = 0.0

        self.sector = 0
        self.sector_index = 0
        self.sector_time = [0.0] * 3
        self.last_sector_time = [0.0] * 3
        self.best_sector_time = [float("inf")] * 3
        self.sector_fuel = 0.0
        self.sector_fuel_range = 0.0
        self.sector_fuel_level = 0.0

        self.mini_sector = 0
        self.mini_sector_index = 0
        self.mini_sector_time = [0.0] * 12
        self.last_mini_sector_time = [0.0] * 12
        self.best_mini_sector_time = [float("inf")] * 12
        self.mini_sector_fuel = 0.0
        self.mini_sector_fuel_range = 0.0
        self.mini_sector_fuel_level = 0.0

        self.km = 0
        self.km_index = 0
        self.km_time = [0.0] * (int(ACLIB.getTrackLength() / 1000) + 1)
        self.last_km_time = [0.0] * (int(ACLIB.getTrackLength() / 1000) + 1)
        self.best_km_time = [float("inf")] * (int(ACLIB.getTrackLength() / 1000) + 1)
        self.km_fuel = 0.0
        self.km_fuel_range = 0.0
        self.km_fuel_level = 0.0

        self.damage = [0.0] * 4
        self.tyre_temp = [0.0] * 4
        self.tyre_dirt = [0.0] * 4
        self.tyre_wear = [0.0] * 4
        self.tyre_pressure = [0.0] * 4
        self.tyre_compound = ""
        self.tyre_compound_symbol = ""

    def init(self):
        self.player_nick = ACLIB.getPlayerNickname(self.number)
        self.player_name = ACLIB.getPlayerFirstname(self.number) + ACLIB.getPlayerLastname(self.number)
        self.car_skin = ACLIB.getCarSkin(self.number)
        self.car_id = ACLIB.getCarId(self.number)
        self.car_name = ACLIB.getCarName(self.number)
        self.car_badge = ACLIB.getCarBadge(self.number)
        self.car_brand = ACLIB.getCarBrand(self.number)
        self.car_class = ACLIB.getCarClass(self.number)
        self.car_type = ACLIB.getCarType(self.number)
        self.drs = ACLIB.hasDRS(self.number)
        self.ers = ACLIB.hasERS(self.number)
        self.kers = ACLIB.hasKERS(self.number)

        self.gear = ACLIB.getGear(self.number)
        self.rpm = ACLIB.getRPM(self.number)
        self.max_rpm = ACLIB.getRPMMax(self.number)
        self.position = ACLIB.getPosition(self.number)
        self.benefit = 0
        self.in_pit = ACLIB.isInPit(self.number)
        self.location = ACLIB.getLocation(self.number)
        self.fuel = ACLIB.getFuel(self.number)
        self.lap_fuel_level = self.fuel
        self.lap = ACLIB.getLap(self.number)

        self.km_fuel_level = self.fuel
        self.km_index = int(self.location * ACLIB.getTrackLength() / 1000)
        self.km = self.km_index + 1
        self.mini_sector_fuel_level = self.fuel
        self.mini_sector_index = int(self.location * 12)
        self.mini_sector = self.mini_sector_index + 1
        self.sector_fuel_level = self.fuel
        self.sector_index = int(self.location * 3)
        self.sector = self.sector_index + 1

        self.tyre_compound = ACLIB.getTyreCompund(symbol=False)
        self.tyre_compound_symbol = ACLIB.getTyreCompund()

    def setEvent(self, event, callback):
        self.events[event] = callback

    def dispatchEvent(self, event):
        if event in self.events:
            self.events[event](self.number)

    def update(self, delta):
        self.gear = ACLIB.getGear(self.number)
        self.rpm = ACLIB.getRPM(self.number)
        self.location = round(ACLIB.getLocation(self.number), 4)
        self.speed = round(ACLIB.getSpeed(self.number), 2)
        self.traveled_distance = ACLIB.getTraveledDistance(self.number)
        self.fuel = round(ACLIB.getFuel(self.number), 2)
        self.penalty_time = ACLIB.getPenaltyTime(self.number)
        self.lap_time = ACLIB.getCurrentLapTime(self.number)
        self.lap_diff = ACLIB.getLapDeltaTime(self.number)
        self.performance[self.location] = max(self.lap_time - self.last_interval, 0)
        self.last_interval = self.lap_time

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
        else:
            self.penalty = False

        # flag
        flag = ACLIB.getFlagId()
        if flag != self.flag:
            self.flag = flag
            self.dispatchEvent(LIB_EVENT.ON_FLAG_CHANGED)

        # pit
        is_in_pit = ACLIB.isInPit(self.number)
        if is_in_pit and not self.in_pit:
            self.in_pit = is_in_pit

            self.dispatchEvent(LIB_EVENT.ON_PIT_ENTERED)

        else:
            self.tyre_compound = ACLIB.getTyreCompund(symbol=False)
            self.tyre_compound_symbol = ACLIB.getTyreCompund()
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

        # Damage and tyres
        for i in range(0, 4):
            self.damage[i] = ACLIB.getCarDamage(self.number, i)
            self.tyre_wear[i] = ACLIB.getTyreWear(self.number, i)
            self.tyre_temp[i] = ACLIB.getTyreTemp(self.number, i, "all")
            self.tyre_pressure[i] = ACLIB.getTyrePressure(self.number, i)
            self.tyre_dirt[i] = ACLIB.getTyreDirtyLevel(self.number, i)

        # Time and Distance to next and previous car
        min_prev = float("-inf")
        min_next = float("inf")
        for c in range(ACLIB.getCarsCount()):
            if c != self.number:
                track_len = ACLIB.getTrackLength()
                c_pos = ACLIB.getLocation(c)

                if c_pos - self.location < min_next and c_pos > 0:
                    self.rel_next = c
                    self.rel_next_dist = c_pos * track_len
                    self.rel_next_time = self.rel_next_dist / max(10.0, ACLIB.getSpeed(self.number, "ms"))

                if c_pos - self.location > min_prev and c_pos < 0:
                    self.rel_prev = c
                    self.rel_prev_dist = c_pos * track_len
                    self.rel_prev_time = self.rel_prev_dist / max(10.0, ACLIB.getSpeed(self.number, "ms"))

                if ACLIB.getPosition(c) == self.position - 1:
                    c_lap = ACLIB.getLap(c)
                    lap = self.lap
                    pos = self.location

                    self.next = c
                    self.next_dist = max(0, ((c_pos + c_lap) * track_len) - ((pos + lap) * track_len))
                    self.next_time = max(0.0, self.next_dist / max(10.0, ACLIB.getSpeed(self.number, "ms")))

                elif ACLIB.getPosition(c) == self.position + 1:
                    c_lap = ACLIB.getLap(c)
                    lap = self.lap
                    pos = self.location

                    self.prev = c
                    self.prev_dist = max(0, (((pos + lap) * track_len) - (c_pos + c_lap) * track_len))
                    self.prev_time = max(0.0, self.prev_dist / max(10.0, ACLIB.getSpeed(self.number, "ms")))

        # Next lap
        lap = ACLIB.getLap(self.number)
        if lap != self.lap:
            self.benefit = 0

            self.lap = ACLIB.getLap(self.number)
            self.last_time = ACLIB.getLastLapTime(self.number)
            self.best_time = ACLIB.getBestLapTime(self.number)

            if 0 < self.last_time < SESSION.best_lap_time and lap > 1:
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

                if sector_time < SESSION.best_sector_time[self.sector_index]:
                    SESSION.best_sector_time[self.sector_index] = sector_time

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

                if mini_sector_time < SESSION.best_mini_sector_time[self.mini_sector_index]:
                    SESSION.best_mini_sector_time[self.mini_sector_index] = mini_sector_time

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

                if km_time < SESSION.best_km_time[self.km_index]:
                    SESSION.best_km_time[self.km_index] = km_time

            if self.km_fuel_level - self.fuel > 0:
                self.km_fuel = self.km_fuel_level - self.fuel
                self.km_fuel_range = self.fuel / self.km_fuel
                self.km_fuel_level = self.fuel

            self.km_index = km
            self.km = km + 1
            self.dispatchEvent(LIB_EVENT.ON_KM_CHANGED)

        self.loops += 1

        if self.loops > 1000:
            self.loops = 0


class ACLIB:
    CARS = [Car] * ac.getCarsCount()

    # Debug functions

    @staticmethod
    def LOG(*msg, sep=""):
        s = ""
        for m in msg:
            s += str(m) + sep
        ac.log(s)

    @staticmethod
    def CONSOLE(*msg, sep=""):
        s = ""
        for m in msg:
            s += str(m) + sep
        ac.console("ACLIB: " + s)

    # Functions for all cars

    @staticmethod
    def setup():
        for i in range(0, ACLIB.getCarsCount()):
            ACLIB.CARS[i] = Car(i)

    @staticmethod
    def init():
        for i in range(0, len(ACLIB.CARS)):
            ACLIB.CARS[i].init()

    @staticmethod
    def update(delta):
        for i in range(0, len(ACLIB.CARS)):
            ACLIB.CARS[i].update(delta)

    @staticmethod
    def reset():
        for i in range(0, len(ACLIB.CARS)):
            ACLIB.CARS[i].reset()

    # Static information

    @staticmethod
    def getPlayerNickname(car=0):
        return ac.getDriverName(car)

    @staticmethod
    def getUniquePlayername(car=0):
        nick = ACLIB.getPlayerNickname(car)
        return (nick[0:3] + " " + nick[-3:]).upper()

    @staticmethod
    def getPlayerFirstname(car=0):
        if car == 0:
            return info.static.playerName
        else:
            return ""

    @staticmethod
    def getPlayerLastname(car=0):
        if car == 0:
            return info.static.playerSurname
        else:
            return ""

    # Player

    @staticmethod
    def getGas(car=0, form=None):
        if form:
            return form.format(ac.getCarState(car, AC_PROP.Gas))
        return ac.getCarState(car, AC_PROP.Gas)

    @staticmethod
    def getBrake(car=0, form=None):
        if form:
            return form.format(ac.getCarState(car, AC_PROP.Brake))
        return ac.getCarState(car, AC_PROP.Brake)

    @staticmethod
    def getClutch(car=0, form=None):
        if form:
            return form.format(ac.getCarState(car, AC_PROP.Clutch))
        return ac.getCarState(car, AC_PROP.Clutch)

    # Session

    @staticmethod
    def getSessionTypeId():
        return info.graphics.session

    @staticmethod
    def getSessionTypeName():
        session = ACLIB.getSessionTypeId()

        if session == -1:
            return "Unknown"
        elif session == 0:
            return "Practice"
        elif session == 1:
            return "Qualifying"
        elif session == 2:
            return "Race"
        elif session == 3:
            return "Hotlap"
        elif session == 4:
            return "Time Attack"
        elif session == 5:
            return "Drift"
        elif session == 6:
            return "Drag"
        return ""

    @staticmethod
    def getSessionCount():
        return info.static.numberOfSessions

    @staticmethod
    def getSessionStatusId():
        return info.graphics.status

    @staticmethod
    def getSessionStatusName():
        session = ACLIB.getSessionStatusId()

        if session == 0:
            return "Off"
        elif session == 1:
            return "Replay"
        elif session == 2:
            return "Live"
        elif session == 3:
            return "Pause"

    @staticmethod
    def pitWindowStart():
        return info.static.pitWindowStart

    @staticmethod
    def pitWindowEnd():
        return info.static.pitWindowEnd

    @staticmethod
    def isTimedRace():
        return info.static.isTimedRace

    @staticmethod
    def getRaceTimeLeft():
        return info.graphics.sessionTimeLeft

    @staticmethod
    def getRaceTimeLeftFormated():
        time = ACLIB.getRaceTimeLeft()

        if not isinf(time):
            if ACLIB.isTimedRace():
                return "time left: " + formatTime(time)
            elif time > 0:
                return "next session in: " + formatTime(time)
        return ""

    @staticmethod
    def getTrackLength(form=None):
        if form:
            return formatDistance(ac.getTrackLength(0))
        return ac.getTrackLength(0)

    @staticmethod
    def getTrackName():
        return info.static.track

    @staticmethod
    def getTrackConfiguration():
        return info.static.trackConfiguration

    @staticmethod
    def getCarsCount():
        return ac.getCarsCount()

    @staticmethod
    def getWindDirection():
        return info.graphics.windDirection

    @staticmethod
    def getWindSpeed():
        return info.graphics.windSpeed

    @staticmethod
    def getSurfaceGrip():
        return info.graphics.surfaceGrip

    @staticmethod
    def getRoadTemp():
        return info.physics.roadTemp

    @staticmethod
    def getAirTemp():
        return info.physics.airTemp

    @staticmethod
    def getAirDensity():
        return info.physics.airDensity

    # aid settings

    @staticmethod
    def isIdealLineOn(car=0):
        if car == 0:
            return info.graphics.idealLineOn
        else:
            return False

    @staticmethod
    def isAutoShifterOn(car=0):
        if car == 0:
            return info.physics.autoShifterOn
        else:
            return False

    @staticmethod
    def tyreBlankets():
        return info.static.aidAllowTyreBlankets

    @staticmethod
    def fuelRate():
        return info.static.aidFuelRate

    @staticmethod
    def tyreRate():
        return info.static.aidTireRate

    @staticmethod
    def damageRate():
        return info.static.aidMechanicalDamage

    @staticmethod
    def stabilityControl():
        return info.static.aidStability

    @staticmethod
    def clutchAid():
        return info.static.aidAutoClutch

    @staticmethod
    def blipAid():
        return info.static.aidAutoBlip

    # Car UI

    @staticmethod
    def getCarId(car=0):
        return ac.getCarName(car)

    @staticmethod
    def getCarClass(car=0):
        name = ACLIB.getCarId(car)
        file = open("content/cars/" + name + "/ui/ui_car.json")
        for line in file.readlines():
            class_line = line.split(":")
            if class_line[0].strip() == "\"tags\"":
                try:
                    class_index = class_line[1].index("#")
                    return class_line[1][class_index + 1:class_line[1].index("\"", class_index)].lower()
                except ValueError:
                    return ""

    @staticmethod
    def getCarBadge(car=0, form=None):
        name = ACLIB.getCarId(car)
        return Texture("content/cars/" + name + "/ui/badge.png")

    @staticmethod
    def getCarBrand(car=0, form=None):
        name = ACLIB.getCarId(car)
        file = open("content/cars/" + name + "/ui/ui_car.json")
        for line in file.readlines():
            class_line = line.split(":")
            if class_line[0].strip() == "\"brand\"":
                return class_line[1].strip().replace("\"", "")

    @staticmethod
    def getCarName(car=0, form=None):
        name = ACLIB.getCarId(car)
        file = open("content/cars/" + name + "/ui/ui_car.json")
        for line in file.readlines():
            class_line = line.split(":")
            if class_line[0].strip() == "\"name\"":
                return class_line[1].strip().replace("\"", "")

    @staticmethod
    def getCarType(car=0, form=None):
        name = ACLIB.getCarId(car)
        file = open("content/cars/" + name + "/ui/ui_car.json")
        for line in file.readlines():
            class_line = line.split(":")
            if class_line[0].strip() == "\"class\"":
                return class_line[1].strip().replace("\"", "")

    @staticmethod
    def getCarSkin(car=0, form=None):
        if car == 0:
            return info.static.carSkin
        else:
            return ""

    @staticmethod
    def hasFinishedRace(car=0, form=None):
        return ac.getCarState(car, AC_PROP.RaceFinished)

    @staticmethod
    def getCurrentLapTime(car=0, form=None):
        return ac.getCarState(car, AC_PROP.LapTime)

    @staticmethod
    def getCurrentLap(car=0, form=None):
        return formatTime(ACLIB.getCurrentLapTime(car))

    @staticmethod
    def getLastLapTime(car=0, form=None):
        return ac.getCarState(car, AC_PROP.LastLap)

    @staticmethod
    def getLastLap(car=0):
        return formatTime(ACLIB.getLastLapTime(car))

    @staticmethod
    def getBestLapTime(car=0, form=None):
        return ac.getCarState(car, AC_PROP.BestLap)

    @staticmethod
    def getBestLap(car=0, form=None):
        return formatTime(ACLIB.getBestLapTime(car))

    @staticmethod
    def getSectorIndex(car=0, form=None):
        if car == 0:
            return info.graphics.currentSectorIndex
        else:
            return -1

    @staticmethod
    def getLastSector(car=0, form=None):
        if car == 0:
            return info.graphics.lastSectorTime
        else:
            return -1

    @staticmethod
    def getSectorCount(car=0, form=None):
        if car == 0:
            return info.static.sectorCount
        else:
            return -1

    @staticmethod
    def getSplit(car=0, form=None):
        if car == 0:
            return info.graphics.split
        else:
            return -1

    @staticmethod
    def getSplits(car=0, form=None):
        return ac.getLastSplits(car)

    @staticmethod
    def getLap(car=0, form=None):
        return ac.getCarState(car, AC_PROP.LapCount) + 1

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
        if car == 0:
            time = ACLIB.getLapDeltaTime(car) * 1000
            if time != 0:
                if time < 0:
                    return "-" + formatTime(abs(time))
                elif time > 0:
                    return "+" + formatTime(abs(time))
            else:
                return "-00:00.000"
        else:
            return -1

    @staticmethod
    def isLapInvalidated(car=0):
        return ac.getCarState(car, AC_PROP.LapInvalidated) or ACLIB.getTyresOut(car) > 2 or ACLIB.isInPit(car)

    @staticmethod
    def getLapCount():
        return info.graphics.completedLaps

    @staticmethod
    def getLaps():
        if info.graphics.numberOfLaps > 0:
            return info.graphics.numberOfLaps
        else:
            return "-"

    @staticmethod
    def lastSectorTime(car=0):
        if car == 0:
            return info.graphics.lastSectorTime
        else:
            return -1

    @staticmethod
    def getSectors(car=0):
        if car == 0:
            return info.static.sectorCount
        else:
            return -1

    @staticmethod
    def getTraveledDistance(car=0, form=None):
        if car == 0:
            if form:
                return form.format(info.graphics.distanceTraveled)
            return info.graphics.distanceTraveled
        else:
            return -1

    @staticmethod
    def getCarDamage(car=0, loc=0, form=None):
        if car == 0:
            if form:
                return form.format(info.physics.carDamage[loc])
            return info.physics.carDamage[loc]  # 0: Front, 1: Rear, 2: Left, 3: Right, 4:?
        else:
            return -1

    @staticmethod
    def hasDRS(car=0, form=None):
        if car == 0:
            return info.static.hasDRS
        else:
            return -1

    @staticmethod
    def DRSAvailable(car=0, form=None):
        return ac.getCarState(car, AC_PROP.DrsAvailable)

    @staticmethod
    def DRSEnabled(car=0, form=None):
        return ac.getCarState(car, AC_PROP.DrsEnabled)

    @staticmethod
    def hasERS(car=0, form=None):
        if car == 0:
            return info.static.hasERS
        else:
            return -1

    @staticmethod
    def ERSRecovery(car=0, form=None):
        if form:
            return form.format(ac.getCarState(car, AC_PROP.ERSRecovery))
        return ac.getCarState(car, AC_PROP.ERSRecovery)

    @staticmethod
    def ERSDelivery(car=0, form=None):
        if form:
            return form.format(ac.getCarState(car, AC_PROP.ERSDelivery))
        return ac.getCarState(car, AC_PROP.ERSDelivery)

    @staticmethod
    def isERSHeatCharging(car=0):
        return ac.getCarState(car, AC_PROP.ERSHeatCharging)

    @staticmethod
    def isERSCharging(car=0):
        if car == 0:
            return info.static.ersIsCharging
        else:
            return -1

    @staticmethod
    def ERSCurrentKJ(car=0, form=None):
        if form:
            return form.format(ac.getCarState(car, AC_PROP.ERSCurrentKJ))
        return ac.getCarState(car, AC_PROP.ERSCurrentKJ)

    @staticmethod
    def ERSMaxJ(car=0, form=None):
        if form:
            return form.format(ac.getCarState(car, AC_PROP.ERSMaxJ))
        return ac.getCarState(car, AC_PROP.ERSMaxJ)

    @staticmethod
    def ERSPowerControllerCount(car=0, form=None):
        if car == 0:
            if form:
                return form.format(info.static.ersPowerControllerCount)
            return info.static.ersPowerControllerCount
        else:
            return -1

    @staticmethod
    def engineBrakeSettingsCount(car=0, form=None):
        if car == 0:
            if form:
                return form.format(info.static.engineBrakeSettingsCount)
            return info.static.engineBrakeSettingsCount
        else:
            return -1

    @staticmethod
    def hasKERS(car=0, form=None):
        if car == 0:
            return info.static.hasKERS
        else:
            return -1

    @staticmethod
    def KERSCharge(car=0, form=None):
        if form:
            return form.format(ac.getCarState(car, AC_PROP.KersCharge))
        return ac.getCarState(car, AC_PROP.KersCharge)

    @staticmethod
    def KERSInput(car=0, form=None):
        if form:
            return form.format(ac.getCarState(car, AC_PROP.KersInput))
        return ac.getCarState(car, AC_PROP.KersInput)

    @staticmethod
    def KERSCurrentKJ(car=0, form=None):
        if form:
            return form.format(ac.getCarState(car, AC_PROP.ERSCurrentKJ))
        return ac.getCarState(car, AC_PROP.ERSCurrentKJ)

    @staticmethod
    def KERSMaxJ(car=0, form=None):
        if car == 0:
            if form:
                return form.format(info.static.kersMaxJ)
            return info.static.kersMaxJ
        else:
            return -1

    @staticmethod
    def ABS(car=0, form=None):
        if car == 0:
            return info.physics.abs
        else:
            return -1

    @staticmethod
    def getSpeed(car=0, unit="kmh", form=None):
        val = 0
        if unit == "kmh":
            val = ac.getCarState(car, AC_PROP.SpeedKMH)
        elif unit == "mph":
            val = ac.getCarState(car, AC_PROP.SpeedMPH)
        elif unit == "ms":
            val = ac.getCarState(car, AC_PROP.SpeedMS)

        if form:
            return form.format(val)
        return val

    @staticmethod
    def getGear(car=0, form=None):
        if form:
            return form.format(ac.getCarState(car, AC_PROP.Gear))
        return ac.getCarState(car, AC_PROP.Gear)

    @staticmethod
    def getRPM(car=0, form=None):
        if form:
            return form.format(ac.getCarState(car, AC_PROP.RPM))
        return ac.getCarState(car, AC_PROP.RPM)

    @staticmethod
    def getRPMMax(car=0, form=None):
        if car == 0:
            val = 8000
            if info.static.maxRpm:
                val = info.static.maxRpm
            if form:
                return form.format(val)
            return val
        else:
            return -1

    @staticmethod
    def getFuel(car=0, form=None):
        if car == 0:
            if form:
                return form.format(info.physics.fuel)
            return info.physics.fuel
        else:
            return -1

    @staticmethod
    def getMaxFuel(car=0, form=None):
        if car == 0:
            if form:
                return form.format(info.static.maxFuel)
            return info.static.maxFuel
        else:
            return -1

    @staticmethod
    def getRealTimePosition(car=0):
        return ac.getCarRealTimeLeaderboardPosition(car) + 1

    @staticmethod
    def getLeaderboardPosition(car=0):
        return ac.getCarLeaderboardPosition(car)

    @staticmethod
    def getPosition(car=0, form=None):
        val = 0
        if ACLIB.getSessionTypeId() == 2:
            val = ACLIB.getRealTimePosition(car)
        else:
            val = ACLIB.getLeaderboardPosition(car)

        if form:
            return form.format(val)
        return val

    @staticmethod
    def getClassPosition(car, form=None):
        if form:
            return form.format(-1)
        return -1  # TODO

    @staticmethod
    def getLocation(car=0, form=None):
        if form:
            form.format(ac.getCarState(car, AC_PROP.NormalizedSplinePosition))
        return ac.getCarState(car, AC_PROP.NormalizedSplinePosition)

    @staticmethod
    def getPenaltyTime(car=0, form=None):
        if car == 0:
            if form:
                return form.format(info.graphics.penaltyTime)
            return info.graphics.penaltyTime
        else:
            return -1

    @staticmethod
    def getFocusedCar():
        return ac.getFocusedCar()

    @staticmethod
    def setFocusedCar(car):
        return ac.focusCar(car)

    @staticmethod
    def isAIDriven(car):
        if car == 0:
            return info.physics.isAIControlled
        else:
            return -1

    # Flag

    @staticmethod
    def getFlagId():
        return info.graphics.flag

    @staticmethod
    def getFlagColor():
        flag = ACLIB.getFlagId()

        if flag == 1:
            return "Blue"
        elif flag == 2:
            return "Yellow"
        elif flag == 3:
            return "Black"
        elif flag == 4:
            return "White"
        elif flag == 5:
            return "Checkered"
        elif flag == 1:
            return "Penalty"

    # Pit

    @staticmethod
    def isPitLimiterOn(car=0):
        if car == 0:
            return info.physics.pitLimiterOn
        else:
            return -1

    @staticmethod
    def mandatoryPitStopDone(car=0):
        if car == 0:
            return info.graphics.mandatoryPitDone
        else:
            return -1

    @staticmethod
    def isInPit(car=0):
        return ACLIB.isInPitLine(car) or ACLIB.isInPitBox(car)

    @staticmethod
    def isInPitLine(car=0):
        return ac.isCarInPitline(car)

    @staticmethod
    def isInPitBox(car=0):
        return ac.isCarInPit(car)

    # Tyres:
    # 0: FL, 1: FR, 2: RL, 3: RR

    @staticmethod
    def getTyreCompund(car=0, symbol=True):
        if car == 0:
            if symbol:
                info.graphics.tyreCompound.split("_")[-1].upper()
            return info.graphics.tyreCompound
        else:
            return -1

    @staticmethod
    def getCamberRad(car, tyre=0, form=None):
        if car == 0:
            if form:
                return form.format(info.physics.camberRAD[tyre])
            return info.physics.camberRAD[tyre]
        else:
            return -1

    @staticmethod
    def getMaxSuspensionTravel(car, tyre=0, form=None):
        if car == 0:
            if form:
                return form.format(info.static.suspensionMaxTravel[tyre])
            return info.static.suspensionMaxTravel[tyre]
        else:
            return -1

    @staticmethod
    def getSuspensionTravel(car, tyre=0, form=None):
        if car == 0:
            if form:
                form.format(info.physics.suspensionTravel[tyre])
            return info.physics.suspensionTravel[tyre]
        else:
            return -1

    @staticmethod
    def getTyresOut(car=0, form=None):
        if car == 0:
            return info.physics.numberOfTyresOut
        else:
            return -1

    @staticmethod
    def getTyreWearValue(car, tyre=0, form=None):
        if car == 0:
            if form:
                return form.format(info.physics.tyreWear[tyre])
            return info.physics.tyreWear[tyre]
        else:
            return -1

    @staticmethod
    def getTyreWear(car, tyre=0, form=None):
        if car == 0:
            if form:
                return form.format((ACLIB.getTyreWearValue(tyre) - 94) * 16.6)
            return (ACLIB.getTyreWearValue(tyre) - 94) * 16.6
        else:
            return -1

    @staticmethod
    def getTyreDirtyLevel(car=0, tyre=0, form=None):
        if car == 0:
            if form:
                form.format(info.physics.tyreDirtyLevel[tyre])
            return info.physics.tyreDirtyLevel[tyre]
        else:
            return -1

    @staticmethod
    def getTyreTemp(car, tyre=0, loc="m", form=None):
        if car == 0:
            if loc == "i":
                if form:
                    form.format(info.physics.tyreTempI[tyre])
                return info.physics.tyreTempI[tyre]
            elif loc == "m":
                if form:
                    form.format(info.physics.tyreTempM[tyre])
                return info.physics.tyreTempM[tyre]
            elif loc == "o":
                if form:
                    form.format(info.physics.tyreTempO[tyre])
                return info.physics.tyreTempO[tyre]
            elif loc == "c":
                if form:
                    form.format(info.physics.tyreCoreTemperature[tyre])
                return info.physics.tyreCoreTemperature[tyre]
            elif loc == "all":
                if form:
                    return [form.format(info.physics.tyreTempI[tyre]),
                            form.format(info.physics.tyreTempM[tyre]),
                            form.format(info.physics.tyreTempO[tyre]),
                            form.format(info.physics.tyreCoreTemperature[tyre])]
                return [info.physics.tyreTempI[tyre],
                        info.physics.tyreTempM[tyre],
                        info.physics.tyreTempO[tyre],
                        info.physics.tyreCoreTemperature[tyre]]
        else:
            return -1

    @staticmethod
    def getTyrePressure(car, tyre=0, form=None):
        if car == 0:
            if form:
                return form.format(info.physics.wheelsPressure[tyre])
            return info.physics.wheelsPressure[tyre]
        else:
            return -1

    # brakes

    @staticmethod
    def getBrakeTemperature(car, tyre=0, form=None):
        if car == 0:
            if form:
                return form.format(info.physics.brakeTemp[tyre])
            return info.physics.brakeTemp[tyre]
        else:
            return -1

    # other cars

    @staticmethod
    def getPrevCarDiffTimeDist(car=0, form=None):
        if car == 0:
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
                    time = max(0.0, dist / max(10.0, ACLIB.getSpeed(0, "ms")))
                    break
            if form:
                if dist > track_len:
                    laps = dist / track_len
                    if laps > 1:
                        return "+{:3.1f}".format(laps) + " Laps"
                    else:
                        return "+{:3.1f}".format(laps) + "   Lap"
                else:
                    if time > 60:
                        minute = time / 60
                        if minute > 1.05:
                            return "+{:3.1f}".format(minute) + " Mins"
                        elif minute < 1.05:
                            return "+{:3.0f}".format(minute) + "   Min"
                    else:
                        return "+" + formatTime(int(time * 1000))
            return time, dist
        else:
            return -1

    @staticmethod
    def getNextCarDiffTimeDist(car=0, form=None):
        if car == 0:
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
                    time = max(0.0, dist / max(10.0, ACLIB.getSpeed(car, "ms")))
                    break
            if form:
                if dist > track_len:
                    laps = dist / track_len
                    if laps > 1:
                        return "-{:3.1f}".format(laps) + " Laps"
                    else:
                        return "-{:3.1f}".format(laps) + "   Lap"
                else:
                    if time > 60:
                        minute = time / 60
                        if minute > 1.05:
                            return "-{:3.1f}".format(minute) + " Mins"
                        elif minute < 1.05:
                            return "-{:3.0f}".format(minute) + "   Min"
                    else:
                        return "-" + formatTime(int(time * 1000))
            return time, dist
        else:
            return -1
