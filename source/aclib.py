import sys
import os
import platform
from math import isinf
import ac

if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__) + '/../stdlib64'
else:
    sysdir = os.path.dirname(__file__) + '/../stdlib'

sys.path.insert(0, sysdir)
sys.path.insert(0, os.path.dirname(__file__) + '/../third_party')
os.environ['PATH'] = os.environ['PATH'] + ";."

from third_party.sim_info import info, AC_PROP


def formatTime(millis, form="{:02d}:{:02d}.{:03d}"):
    millis = int(millis)
    m = int(millis / 60000)
    s = int((millis % 60000) / 1000)
    ms = millis % 1000

    return form.format(m, s, ms)


def formatDistance(meters, form="{:2d}.{:02.0f} km"):
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


class Car:
    def __init__(self, number):
        self.priority = 10  # more means a higher effort to compute but more precise results
        self.loops = 0
        self.initialized = False
        self.max_delta = 0.1

        self.number = number
        self.player_name = ""
        self.player_nick = ""
        self.drs = False
        self.ers = False
        self.kers = False

        self.speed = 0.0  # standings
        self.position = 0  # standings
        self.benefit = 0  # position gain/loss per lap
        self.location = 0.0  # track position from 0 to 1
        self.traveled_distance = 0.0  # in m
        self.lap_performance = 0.0  # current lap
        self.fuel = 0.0  # in l
        self.flag = 0
        self.penalty = False
        self.penalty_time = 0.0
        self.abs = 0.0
        self.tc = 0.0

        self.next = 0
        self.next_dist = 0
        self.next_time = 0

        self.prev = 0
        self.prev_dist = 0
        self.prev_time = 0

        self.lap = 1  # current lap
        self.lap_diff = 0.0  # performance meter
        self.lap_time = 0.0  # last lap time
        self.lap_fuel = 0.0  # fuel consumption in l
        self.lap_fuel_range = 0.0  # number of laps with current fuel
        self.lap_fuel_level = 0.0  # fuel level from last lap

        self.sector = 0
        self.sector_index = 0
        self.sector_time = [0.0] * 3
        self.last_sector_time = [0.0] * 3
        self.best_sector_time = [0.0] * 3
        self.sector_fuel = 0.0
        self.sector_fuel_range = 0.0
        self.sector_fuel_level = 0.0

        self.mini_sector = 0
        self.mini_sector_index = 0
        self.mini_sector_time = [0.0] * 12
        self.last_mini_sector_time = [0.0] * 12
        self.best_mini_sector_time = [0.0] * 12
        self.mini_sector_fuel = 0.0
        self.mini_sector_fuel_range = 0.0
        self.mini_sector_fuel_level = 0.0

        self.km = 0
        self.km_index = 0
        self.km_time = [0.0] * 1
        self.last_km_time = [0.0] * 1
        self.best_km_time = [0.0] * 1
        self.km_fuel = 0.0
        self.km_fuel_range = 0.0
        self.km_fuel_level = 0.0

        self.damage = [0.0] * 4  # 0: front, 1: rear, 2: left, 3: right
        self.tyre_temp = [0.0] * 4  # 0: FL, 1: FR, 2: RL, 3: RR
        self.tyre_dirt = [0.0] * 4
        self.tyre_wear = [0.0] * 4
        self.tyre_pressure = [0.0] * 4

        self.init()

    def reset(self):
        self.speed = 0.0
        self.position = 0
        self.benefit = 0
        self.location = 0.0
        self.traveled_distance = 0.0
        self.lap_performance = 0.0
        self.fuel = 0.0
        self.flag = 0
        self.penalty = False
        self.abs = 0.0
        self.tc = 0.0

        self.next = 0
        self.next_dist = 0
        self.next_time = 0

        self.prev = 0
        self.prev_dist = 0
        self.prev_time = 0

        self.lap = 1
        self.lap_diff = 0.0
        self.lap_time = 0.0
        self.lap_fuel = 0.0
        self.lap_fuel_range = 0.0
        self.lap_fuel_level = 0.0

        self.sector = 1
        self.sector_index = 0
        self.sector_time = [0.0] * 3
        self.last_sector_time = [0.0] * 3
        self.best_sector_time = [0.0] * 3
        self.sector_fuel = 0.0
        self.sector_fuel_range = 0.0
        self.sector_fuel_level = 0.0

        self.mini_sector = 1
        self.mini_sector_index = 0
        self.mini_sector_time = [0.0] * 12
        self.last_mini_sector_time = [0.0] * 12
        self.best_mini_sector_time = [0.0] * 12
        self.mini_sector_fuel = 0.0
        self.mini_sector_fuel_range = 0.0
        self.mini_sector_fuel_level = 0.0

        self.km = 1
        self.km_index = 0
        self.km_time = [0.0] * 1
        self.last_km_time = [0.0] * 1
        self.best_km_time = [0.0] * 1
        self.km_fuel = 0.0
        self.km_fuel_range = 0.0
        self.km_fuel_level = 0.0

        self.damage = [0.0] * 4
        self.tyre_temp = [0.0] * 4
        self.tyre_dirt = [0.0] * 4
        self.tyre_wear = [0.0] * 4
        self.tyre_pressure = [0.0] * 4

    def init(self):
        self.player_nick = ACLIB.getPlayerNickname(self.number)
        self.player_name = ACLIB.getPlayerFirstname() + ACLIB.getPlayerLastname()
        self.drs = ACLIB.hasDRS(self.number)
        self.ers = ACLIB.hasERS(self.number)
        self.kers = ACLIB.hasKERS(self.number)

        self.km_time = [0.0] * int(ACLIB.getTrackLength() / 1000)
        self.last_km_time = [0.0] * int(ACLIB.getTrackLength() / 1000)
        self.best_km_time = [0.0] * int(ACLIB.getTrackLength() / 1000)

        self.position = ACLIB.getPosition(self.number)
        self.benefit = 0
        self.location = ACLIB.getLocation(self.number)
        self.fuel = ACLIB.getFuel(self.number)
        self.km_fuel_level = self.fuel
        self.km_index = int(self.location * ACLIB.getTrackLength() / 1000) - 1
        self.km = self.km_index - 1
        self.mini_sector_fuel_level = self.fuel
        self.mini_sector_index = max(0, int(self.location * 12) - 1)
        self.mini_sector = self.mini_sector_index + 1
        self.sector_fuel_level = self.fuel
        self.sector_index = max(0, int(self.location * 10 / 3) - 1)
        self.sector = self.sector_index + 1
        self.lap_fuel_level = self.fuel

    def update(self, delta):
        self.location = round(ACLIB.getLocation(self.number), 4)
        self.speed = round(ACLIB.getSpeed(self.number), 2)
        self.traveled_distance = ACLIB.getTraveledDistance(self.number)
        self.lap_performance = ACLIB.getCurrentLapTime(self.number)
        self.fuel = round(ACLIB.getFuel(self.number), 2)
        self.lap_diff = ACLIB.getLapDeltaTime(self.number)
        self.penalty_time = ACLIB.getPenaltyTime(self.number)

        if self.penalty_time > 0:
            self.penalty = True
        else:
            self.penalty = False

        # flag
        self.flag = ACLIB.getFlagId()

        # Position changed
        position = ACLIB.getPosition(self.number)
        if position != self.position:
            self.benefit += self.position - position
            self.position = position

        # Damage and tyres
        for i in range(0, 4):
            dmg = ACLIB.getCarDamage(i)
            if dmg > self.damage[i]:
                self.damage[i] = dmg

            wear = ACLIB.getTyreWear(i)
            temp = ACLIB.getTyreTemp(i)
            pressure = ACLIB.getTyrePressure(i)
            dirt = ACLIB.getTyreDirtyLevel(i)

        # Time and Distance to next and previous car
        both = 0
        for c in range(ACLIB.getCarsCount()):
            if ACLIB.getPosition(c) == self.position - 1:
                track_len = ACLIB.getTrackLength()
                c_lap = ACLIB.getLap(c)
                c_pos = ACLIB.getLocation(c)
                lap = self.lap
                pos = self.location

                self.next_dist = max(0, ((c_pos + c_lap) * track_len) - ((pos + lap) * track_len))
                self.next_time = max(0.0, self.next_dist / max(10.0, ACLIB.getSpeed(0, "ms")))
                both += 1

            elif ACLIB.getPosition(c) == self.position + 1:
                track_len = ACLIB.getTrackLength()
                c_lap = ACLIB.getLap(c)
                c_pos = ACLIB.getLocation(c)
                lap = self.lap
                pos = self.location

                self.prev_dist = max(0, (((pos + lap) * track_len) - (c_pos + c_lap) * track_len))
                self.prev_time = max(0.0, self.prev_dist / max(10.0, ACLIB.getSpeed(0, "ms")))
                both += 1

            if both == 2:
                break

        # Next lap
        lap = ACLIB.getLap(self.number)
        if lap != self.lap:
            self.benefit = 0
            self.lap = lap
            self.lap_time = ACLIB.getLastLapTime(self.number)
            self.lap_fuel = round(self.lap_fuel_level - self.fuel, 1)
            if self.lap_fuel > 0:
                self.lap_fuel_range = round(self.fuel / self.lap_fuel, 1)
                self.lap_fuel_level = self.fuel

        # Update every 5th loop only if delta is < 0.1 sec and priority >= 1
        if self.priority >= 0 and self.loops % 3 == 0 and delta < self.max_delta:
            # Next sector
            sector = max(0, int(self.location * 10 / 3) - 1)
            if sector != self.sector_index:
                sec_time = ACLIB.getCurrentLapTime(self.number)
                if self.sector_index > 0:
                    sec_time -= self.sector_time[self.sector_index]
                self.sector_time[sector] = sec_time
                self.sector_fuel = round(self.sector_fuel_level - self.fuel, 1)
                if self.sector_fuel > 0:
                    self.sector_fuel_range = round(self.fuel / self.sector_fuel, 1)
                    self.sector_fuel_level = self.fuel
                self.sector_index = sector
                self.sector = sector + 1

        # Update every 20th loop only if delta is < 0.1 sec and priority >= 3
        if self.priority >= 2 and self.loops % 5 == 0 and delta < self.max_delta:
            # Next mini sector
            mini_sector = max(0, int(self.location * 12) - 1)
            if mini_sector != self.mini_sector_index:
                mini_sector_time = ACLIB.getCurrentLapTime(self.number)
                if self.mini_sector_index > 0:
                    mini_sector_time -= self.mini_sector_time[self.mini_sector_index]
                self.mini_sector_time[mini_sector] = mini_sector_time
                self.mini_sector_fuel = round(self.mini_sector_fuel_level - self.fuel, 1)
                if self.mini_sector_fuel > 0:
                    self.mini_sector_fuel_range = round(self.fuel / self.mini_sector_fuel, 1)
                    self.mini_sector_fuel_level = self.fuel
                self.mini_sector_index = mini_sector
                self.mini_sector = mini_sector + 1

        # # Update every 50th loop only if delta is < 0.1 sec and priority >= 5
        # if self.priority >= 5 and self.loops % 10 == 0 and delta < self.max_delta:
        #     # Next km
        #     km = int(self.location * ACLIB.getTrackLength() / 1000)
        #     if km != self.km_index:
        #         km_time = ACLIB.getCurrentLapTime(self.number)
        #         if self.km_index > 0:
        #             km_time -= self.km_time[self.km_index]
        #         self.km_time[max(0, km - 1)] = km_time
        #         self.km_fuel = round(self.km_fuel_level - self.fuel, 1)
        #         if self.km_fuel > 0:
        #             self.km_fuel_range = round(self.fuel / self.km_fuel, 1)
        #             self.km_fuel_level = self.fuel
        #         self.km_index = max(0, km - 1)
        #         self.km = km

        self.loops += 1

        if self.loops > 1000:
            self.loops = 0


class ACLIB:
    CARS = [Car] * ac.getCarsCount()

    @staticmethod
    def init():
        for i in range(0, ac.getCarsCount()):
            ACLIB.CARS[i] = Car(i)

    @staticmethod
    def LOG(msg):
        ac.log(str(msg))

    @staticmethod
    def CONSOLE(msg):
        ac.console(str(msg))

    @staticmethod
    def getPlayerNickname(car):
        return ac.getDriverName(car)

    @staticmethod
    def getUniquePlayername(car):
        nick = ACLIB.getPlayerNickname(car)
        return nick[0:3] + " " + nick[-3:]

    @staticmethod
    def getPlayerFirstname():
        return info.static.playerName

    @staticmethod
    def getPlayerLastname():
        return info.static.playerSurname

    @staticmethod
    def isIdealLineOn():
        return info.graphics.idealLineOn

    @staticmethod
    def isAutoShifterOn():
        return info.physics.autoShifterOn

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
    def getTrackLength():
        return info.static.trackSPlineLength

    @staticmethod
    def getTrackLengthFormated():
        return formatDistance(ACLIB.getTrackLength())

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

    @staticmethod
    def getLapCount():
        return info.graphics.completedLaps

    @staticmethod
    def getCarName(car):
        return info.static.carModel

    @staticmethod
    def getCarSkin(car):
        return info.static.carSkin

    @staticmethod
    def getCurrentLapTime(car):
        return ac.getCarState(car, AC_PROP.LapTime)

    @staticmethod
    def getCurrentLap(car):
        return formatTime(ACLIB.getCurrentLapTime(car))

    @staticmethod
    def getLastLapTime(car):
        return ac.getCarState(car, AC_PROP.LastLap)

    @staticmethod
    def getLastLap(car):
        return formatTime(ACLIB.getLastLapTime(car))

    @staticmethod
    def getBestLapTime(car):
        return ac.getCarState(car, AC_PROP.BestLap)

    @staticmethod
    def getBestLap(car):
        return formatTime(ACLIB.getBestLapTime(car))

    @staticmethod
    def getSectorIndex(car):
        if car == 0:
            return info.graphics.currentSectorIndex
        else:
            return 0

    @staticmethod
    def getLastSector(car):
        if car == 0:
            return info.graphics.lastSectorTime
        else:
            return 0

    @staticmethod
    def getSectorCount(car):
        if car == 0:
            return info.static.sectorCount
        else:
            return 0

    @staticmethod
    def getSplit(car):
        if car == 0:
            return info.graphics.split
        else:
            return 0

    @staticmethod
    def getSplits(car):
        return ac.getLastSplits(car)

    @staticmethod
    def getLap(car):
        return ac.getCarState(car, AC_PROP.LapCount) + 1

    @staticmethod
    def getLapDeltaTime(car):
        return ac.getCarState(car, AC_PROP.PerformanceMeter)

    @staticmethod
    def getLapDelta(car):
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
            return 0

    @staticmethod
    def isLapInvalidated(car):
        return ac.getCarState(car, AC_PROP.LapInvalidated) or ACLIB.getTyresOut(car) > 2 or ACLIB.isInPit(car)

    @staticmethod
    def getLaps():
        if info.graphics.numberOfLaps > 0:
            return info.graphics.numberOfLaps
        else:
            return "-"

    @staticmethod
    def lastSectorTime(car):
        if car == 0:
            return info.graphics.lastSectorTime
        else:
            return 0

    @staticmethod
    def getSectors(car):
        if car == 0:
            return info.static.sectorCount
        else:
            return 0

    @staticmethod
    def getFocusedCar(car):
        if car == 0:
            return ac.getFocusedCar()
        else:
            return 0

    @staticmethod
    def getTraveledDistance(car):
        if car == 0:
            return info.graphics.distanceTraveled
        else:
            return 0

    @staticmethod
    def getCarDamage(car, loc=0):
        if car == 0:
            return info.physics.carDamage[loc]  # 0: Front, 1: Rear, 2: Left, 3: Right, 4:?
        else:
            return 0

    @staticmethod
    def getPrevCarDiffTimeDist(car):
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
            return time, dist
        else:
            return 0

    @staticmethod
    def getPrevCarDiff(car):
        if car == 0:
            time, dist = ACLIB.getPrevCarDiffTimeDist(car)
            track_len = ACLIB.getTrackLength()

            if dist > track_len:
                laps = dist / track_len
                if laps > 1.05:
                    return "+{:3.1f}".format(laps) + " Laps"
                elif laps < 1.05:
                    return "+{:3.0f}".format(laps) + "   Lap"
            else:
                if time > 60:
                    minute = time / 60
                    if minute > 1.05:
                        return "+{:3.1f}".format(minute) + " Mins"
                    elif minute < 1.05:
                        return "+{:3.0f}".format(minute) + "   Min"
                else:
                    return "+" + formatTime(int(time * 1000))
        else:
            return 0

    @staticmethod
    def getNextCarDiffTimeDist(car):
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
            return time, dist
        else:
            return 0

    @staticmethod
    def getNextCarDiff(car):
        if car == 0:
            time, dist = ACLIB.getNextCarDiffTimeDist(car)
            track_len = ACLIB.getTrackLength()

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
        else:
            return 0

    @staticmethod
    def getGas(car):
        if car == 0:
            return info.physics.gas
        else:
            return 0

    @staticmethod
    def getBrake(car):
        if car == 0:
            return info.physics.brake
        else:
            return 0

    @staticmethod
    def getClutch(car):
        if car == 0:
            return info.physics.clutch
        else:
            return 0

    @staticmethod
    def hasDRS(car):
        if car == 0:
            return info.static.hasDRS
        else:
            return 0

    @staticmethod
    def DRSAvailable(car):
        if car == 0:
            return info.physics.drsAvailable
        else:
            return 0

    @staticmethod
    def DRSEnabled(car):
        if car == 0:
            return info.physics.drsEnabled
        else:
            return 0

    @staticmethod
    def hasERS(car):
        if car == 0:
            return info.static.hasERS
        else:
            return 0

    @staticmethod
    def isERSCharging(car):
        if car == 0:
            return info.static.ersIsCharging
        else:
            return 0

    @staticmethod
    def ERSMaxJ(car):
        if car == 0:
            return info.static.ersMaxJ
        else:
            return 0

    @staticmethod
    def ERSPowerControllerCount(car):
        if car == 0:
            return info.static.ersPowerControllerCount
        else:
            return 0

    @staticmethod
    def engineBrakeSettingsCount(car):
        if car == 0:
            return info.static.engineBrakeSettingsCount
        else:
            return 0

    @staticmethod
    def hasKERS(car):
        if car == 0:
            return info.static.hasKERS
        else:
            return 0

    @staticmethod
    def KERSCharge(car):
        if car == 0:
            return info.physics.kersCharge
        else:
            return 0

    @staticmethod
    def KERSInput(car):
        if car == 0:
            return info.physics.kersInput
        else:
            return 0

    @staticmethod
    def KERSCurrentKJ(car):
        if car == 0:
            return info.static.kersCurrentKJ
        else:
            return 0

    @staticmethod
    def KERSMaxJ(car):
        if car == 0:
            return info.static.kersMaxJ
        else:
            return 0

    @staticmethod
    def ABS(car):
        if car == 0:
            return info.physics.abs
        else:
            return 0

    @staticmethod
    def getSpeed(car, unit="kmh"):
        if unit == "kmh":
            return ac.getCarState(car, AC_PROP.SpeedKMH)
        elif unit == "mph":
            return ac.getCarState(car, AC_PROP.SpeedMPH)
        elif unit == "ms":
            return ac.getCarState(car, AC_PROP.SpeedMS)

    @staticmethod
    def getGear(car):
        return formatGear(ac.getCarState(car, AC_PROP.Gear))

    @staticmethod
    def getRPMValue(car):
        return ac.getCarState(car, AC_PROP.RPM)

    @staticmethod
    def getRPM(car):
        return int(ACLIB.getRPMValue(car))

    @staticmethod
    def getRPMMax(car):
        if car == 0:
            if info.static.maxRpm:
                return info.static.maxRpm
            else:
                return 8000
        else:
            return 0

    @staticmethod
    def getPosition(car):
        return ac.getCarRealTimeLeaderboardPosition(car) + 1

    @staticmethod
    def getLocation(car):
        return ac.getCarState(car, AC_PROP.NormalizedSplinePosition)

    @staticmethod
    def getPenaltyTime(car):
        if car == 0:
            return info.graphics.penaltyTime
        else:
            return 0

    @staticmethod
    def isPitLimiterOn(car):
        if car == 0:
            return info.physics.pitLimiterOn
        else:
            return 0

    @staticmethod
    def mandatoryPitStopDone(car):
        if car == 0:
            return info.graphics.mandatoryPitDone
        else:
            return 0

    @staticmethod
    def isInPit(car):
        return ACLIB.isInPitLine(car) or ACLIB.isInPitBox(car)

    @staticmethod
    def isInPitLine(car):
        return ac.isCarInPitline(car)

    @staticmethod
    def isInPitBox(car):
        return ac.isCarInPit(car)

    @staticmethod
    def isAIDriven(car):
        if car == 0:
            return info.physics.isAIControlled
        else:
            return 0

    @staticmethod
    def getFuel(car):
        if car == 0:
            return info.physics.fuel
        else:
            return 0

    @staticmethod
    def getMaxFuel(car):
        if car == 0:
            return info.static.maxFuel
        else:
            return 0

    @staticmethod
    def getCamberRad(car, tyre=0):
        if car == 0:
            return info.physics.camberRAD[tyre]
        else:
            return 0

    @staticmethod
    def getMaxSuspensionTravel(car, tyre=0):
        if car == 0:
            return info.static.suspensionMaxTravel[tyre]
        else:
            return 0

    @staticmethod
    def getSuspensionTravel(car, tyre=0):
        if car == 0:
            return info.physics.suspensionTravel[tyre]
        else:
            return 0

    @staticmethod
    def getTyresOut(car):
        if car == 0:
            return info.physics.numberOfTyresOut
        else:
            return 0

    @staticmethod
    def getTyreWearValue(car, tyre=0):
        if car == 0:
            return info.physics.tyreWear[tyre]  # 0: FL, 1: FR, 2: RL, 3: RR
        else:
            return 0

    @staticmethod
    def getTyreWear(car, tyre=0):
        if car == 0:
            return (ACLIB.getTyreWearValue(tyre) - 94) * 16.6
        else:
            return 0

    @staticmethod
    def getTyreWearFormated(car, tyre=0):
        if car == 0:
            return "{:2.1f}%".format((ACLIB.getTyreWearValue(car, tyre) - 94) * 16.6)
        else:
            return 0

    @staticmethod
    def getTyreDirtyLevel(tyre=0):
        return info.physics.tyreDirtyLevel[tyre]

    @staticmethod
    def getTyreCompund():
        return info.graphics.tyreCompound

    @staticmethod
    def getTyreTemp(car, tyre=0, loc="m"):
        if car == 0:
            if loc == "i":
                return info.physics.tyreTempI[tyre]
            elif loc == "m":
                return info.physics.tyreTempM[tyre]
            elif loc == "o":
                return info.physics.tyreTempO[tyre]
            elif loc == "c":
                return info.physics.tyreCoreTemperature[tyre]
            elif loc == "all":
                return [info.physics.tyreTempI[tyre],
                        info.physics.tyreTempM[tyre],
                        info.physics.tyreTempO[tyre],
                        info.physics.tyreCoreTemperature[tyre]]
        else:
            return 0

    @staticmethod
    def getTyreTempFormated(car, tyre=0, loc="m"):
        if car == 0:
            return "{:2.1f}°".format(ACLIB.getTyreTemp(car, tyre, loc))
        else:
            return 0

    @staticmethod
    def getTyrePressure(car, tyre=0):
        if car == 0:
            return info.physics.wheelsPressure[tyre]
        else:
            return 0

    @staticmethod
    def getTyrePressureFormated(car, tyre=0):
        if car == 0:
            return "{:2.1f}psi".format(ACLIB.getTyrePressure(car, tyre))
        else:
            return 0

    @staticmethod
    def getBrakeTemperature(car, tyre=0):
        if car == 0:
            return info.physics.brakeTemp[tyre]
        else:
            return 0

    @staticmethod
    def getBrakeTemperatureFormated(car, tyre=0):
        if car == 0:
            return "{:2.1f}°".format(ACLIB.getBrakeTemperature(tyre))
        else:
            return 0
