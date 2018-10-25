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
    car = 0
    air_temp = 0
    track_temp = 0
    track_length = 0
    wind_direction = 0
    wind_speed = 0

    time_left = 0


class Car:
    position = 0  # standings
    benefit = 0  # position gain/loss per lap
    location = 0.0  # track position from 0 to 1
    traveled_distance = 0.0  # in m
    fuel = 0.0  # in l
    flag = 0
    penalty = False
    abs = 0.0
    tc = 0.0
    drs = False
    ers = False
    kers = False

    next = 0
    next_dist = 0
    next_time = 0

    prev = 0
    prev_dist = 0
    prev_time = 0

    lap = 0  # current lap
    lap_diff = 0.0  # performance meter
    lap_time = 0.0  # last lap time
    lap_fuel = 0.0  # fuel consumption in l
    lap_fuel_range = 0.0  # number of laps with current fuel
    lap_fuel_level = 0.0  # fuel level from last lap

    sector = 0
    sector_time = [0.0] * 3
    sector_fuel = 0.0
    sector_fuel_range = 0.0
    sector_fuel_level = 0.0

    mini_sector = 0
    mini_sector_time = [0.0] * 12
    mini_sector_fuel = 0.0
    mini_sector_fuel_range = 0.0
    mini_sector_fuel_level = 0.0

    km = 0
    km_time = [0.0] * 1
    km_fuel = 0.0
    km_fuel_range = 0.0
    km_fuel_level = 0.0

    damage = [0.0] * 4  # 0: front, 1: rear, 2: left, 3: right
    tyre_temp = [0.0] * 4
    tyre_dirt = [0.0] * 4
    tyre_wear = [0.0] * 4  # 0: FL, 1: FR, 2: RL, 3: RR
    tyre_pressure = [0.0] * 4


class ACLIB:
    def __init__(self):
        self.CARS = [Car] * self.getCarsCount()
        self.car = None  # use focused car
        self.car_index = -1  # use focused car
        self.priority = 10  # more means a higher effort to compute
        self.loops = 0
        self.initialized = False
        self.max_delta = 0.1

    def init(self):
        for car in self.CARS:
            car.drs = self.hasDRS()
            car.ers = self.hasERS()
            car.kers = self.hasKERS()

            car.km_time = [0.0] * int(self.getTrackLength() / 1000)

            car.km_fuel_level = car.fuel
            car.mini_sector_fuel = car.fuel
            car.sector_fuel = car.fuel
            car.lap_fuel = car.fuel
            
    def reset(self):
        car = self.CARS[self.car_index]
        
        car.position = 0
        car.benefit = 0
        car.location = 0.0
        car.traveled_distance = 0.0
        car.fuel = 0.0
        car.flag = 0
        car.penalty = False
        car.abs = 0.0
        car.tc = 0.0
        car.drs = False
        car.ers = False
        car.kers = False
        
        car.next = 0
        car.next_dist = 0
        car.next_time = 0
        
        car.prev = 0
        car.prev_dist = 0
        car.prev_time = 0
        
        car.lap = 0
        car.lap_diff = 0.0
        car.lap_time = 0.0
        car.lap_fuel = 0.0
        car.lap_fuel_range = 0.0
        car.lap_fuel_level = 0.0
        
        car.sector = 0
        car.sector_time = [0.0] * 3
        car.sector_fuel = 0.0
        car.sector_fuel_range = 0.0
        car.sector_fuel_level = 0.0
        
        car.mini_sector = 0
        car.mini_sector_time = [0.0] * 12
        car.mini_sector_fuel = 0.0
        car.mini_sector_fuel_range = 0.0
        car.mini_sector_fuel_level = 0.0
        
        car.km = 0
        car.km_time = [0.0] * 1
        car.km_fuel = 0.0
        car.km_fuel_range = 0.0
        car.km_fuel_level = 0.0
        
        car.damage = [0.0] * 4
        car.tyre_temp = [0.0] * 4
        car.tyre_dirt = [0.0] * 4
        car.tyre_wear = [0.0] * 4
        car.tyre_pressure = [0.0] * 4

    def updateAll(self):
        for i in range(0, len(self.CARS)):
            self.update(0, i)

    def update(self, delta, car=-1):
        if not self.initialized:
            self.init()
            self.initialized = True

        if car != -1:
            self.car_index = car
        else:
            self.car_index = self.getFocusedCar()

        self.car = self.CARS[self.car_index]

        self.car.location = round(self.getLocation(self.car_index), 4)
        self.car.traveled_distance = self.getTraveledDistance()
        self.car.fuel = round(self.getFuel(), 2)
        self.car.diff = self.getLapDeltaTime(self.car_index)

        # Time and Distance to next and previous car
        both = 0
        for c in range(self.getCarsCount()):
            if self.getPosition(c) == self.getPosition(0) - 1:
                track_len = self.getTrackLength()
                c_lap = self.getLap(c)
                c_pos = self.getLocation(c)
                lap = self.car.lap
                pos = self.car.position

                self.car.next_dist = max(0, ((c_pos + c_lap) * track_len) - ((pos + lap) * track_len))
                self.car.next_time = max(0.0, self.car.next_dist / max(10.0, self.getSpeed(0, "ms")))
                both += 1

            elif self.getPosition(c) == self.getPosition(0) + 1:
                track_len = self.getTrackLength()
                c_lap = self.getLap(c)
                c_pos = self.getLocation(c)
                lap = self.car.lap
                pos = self.car.position

                self.car.prev_dist = max(0, (((pos + lap) * track_len) - (c_pos + c_lap) * track_len))
                self.car.prev_time = max(0.0, self.car.prev_dist / max(10.0, self.getSpeed(0, "ms")))
                both += 1

            if both == 2:
                break

        # flag
        self.car.flag = self.getFlagId()

        # Position changed
        position = self.getPosition(self.car_index)
        if position != self.car.position:
            self.car.benefit = self.car.position - position
            self.car.position = position

        # # Next lap
        # lap = self.getLap(self.car_index)
        # if lap != self.car.lap:
        #     self.car.lap = lap
        #     self.car.lap_time = self.getLastLapTime(self.car_index)
        #     self.car.lap_fuel = round(self.car.lap_fuel_level - self.car.fuel, 1)
        #     if self.car.lap_fuel > 0:
        #         self.car.lap_fuel_range = round(self.car.fuel / self.car.lap_fuel, 1)
        #         self.car.lap_fuel_level = self.car.fuel
        #
        # # Update every 50th loop only if delta is < 0.1 sec and priority >= 5
        # if self.priority >= 5 and self.loops % 10 == 0 and delta < self.max_delta:
        #     # Next km
        #     km = int(self.getTraveledDistance() / 1000) % int(self.getTrackLength() / 1000)
        #     if km != self.car.km:
        #         self.car.km_time[km] = self.getCurrentLapTime(self.car_index)
        #         self.car.km = km
        #         self.car.km_fuel = round(self.car.km_fuel_level - self.car.fuel, 1)
        #         if self.car.km_fuel > 0:
        #             self.car.km_fuel_range = round(self.car.fuel / self.car.km_fuel, 1)
        #             self.car.km_fuel_level = self.car.fuel
        #
        # # Update every 20th loop only if delta is < 0.1 sec and priority >= 3
        # if self.priority >= 2 and self.loops % 5 == 0 and delta < self.max_delta:
        #     # Next mini sector
        #     mini_sector = int(self.getLocation(self.car_index) * 12)
        #     if mini_sector != self.car.mini_sector:
        #         self.car.mini_sector_time[mini_sector] = self.getCurrentLapTime(self.car_index)
        #         self.car.mini_sector = mini_sector
        #         self.car.mini_sector_fuel = round(self.car.mini_sector_fuel_level - self.car.fuel, 1)
        #         if self.car.mini_sector_fuel > 0:
        #             self.car.mini_sector_fuel_range = round(self.car.fuel / self.car.mini_sector_fuel,
        #                                                           1)
        #             self.car.mini_sector_fuel_level = self.car.fuel
        #
        # # Update every 5th loop only if delta is < 0.1 sec and priority >= 1
        # if self.priority >= 0 and self.loops % 3 == 0 and delta < self.max_delta:
        #     # Next sector
        #     sector = int(self.getLocation(self.car_index) * 10 / 3)
        #     if sector != self.car.sector:
        #         self.car.sector_time[sector] = self.getCurrentLapTime(self.car_index)
        #         self.car.sector = sector
        #         self.car.sector_fuel = round(self.car.sector_fuel_level - self.car.fuel, 1)
        #         if self.car.sector_fuel > 0:
        #             self.car.sector_fuel_range = round(self.car.fuel / self.car.sector_fuel, 1)
        #             self.car.sector_fuel_level = self.car.fuel

            # # Damage and tyres
            # for i in range(0, 4):
            #     dmg = self.getCarDamage(i)
            #     if dmg > self.car.damage[i]:
            #         self.car.damage[i] = dmg
            #
            #     wear = self.getTyreWear(i)
            #     temp = self.getTyreTemp(i)
            #     pressure = self.getTyrePressure(i)
            #     dirt = self.getTyreDirtyLevel(i)

        self.loops += 1

        if self.loops > 1000:
            self.loops = 0

    @staticmethod
    def LOG(msg):
        ac.log(msg)

    @staticmethod
    def CONSOLE(msg):
        ac.console(msg)

    @staticmethod
    def getPlayerNickname():
        return info.static.playerNick

    @staticmethod
    def getUniquePlayername():
        nick = info.static.playerNick
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
    def getCarName():
        return info.static.carModel

    @staticmethod
    def getCarSkin():
        return info.static.carSkin

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
    def fuelRate():
        return info.static.aidFuelRate

    @staticmethod
    def tyreRate():
        return info.static.aidTireRate

    @staticmethod
    def damageRate():
        return info.static.aidMechanicalDamage

    @staticmethod
    def tyreBlankets():
        return info.static.aidAllowTyreBlankets

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
    def getCurrentLapTime(car=0):
        return ac.getCarState(car, AC_PROP.LapTime)

    @staticmethod
    def getCurrentLap(car=0):
        return formatTime(ACLIB.getCurrentLapTime(car))

    @staticmethod
    def getLastLapTime(car=0):
        return ac.getCarState(car, AC_PROP.LastLap)

    @staticmethod
    def getLastLap(car=0):
        return formatTime(ACLIB.getLastLapTime(car))

    @staticmethod
    def getBestLapTime(car=0):
        return ac.getCarState(car, AC_PROP.BestLap)

    @staticmethod
    def getBestLap(car=0):
        return formatTime(ACLIB.getBestLapTime(car))

    @staticmethod
    def getSectorIndex():
        return info.graphics.currentSectorIndex

    @staticmethod
    def getLastSector():
        return info.graphics.lastSectorTime

    @staticmethod
    def getSectorCount():
        return info.static.sectorCount

    @staticmethod
    def getSplit():
        return info.graphics.split

    @staticmethod
    def getSplits(car=0):
        return ac.getLastSplits(car)

    @staticmethod
    def getLap(car=0):
        return ac.getCarState(car, AC_PROP.LapCount) + 1

    @staticmethod
    def getLapDeltaTime(car=0):
        return ac.getCarState(car, AC_PROP.PerformanceMeter)

    @staticmethod
    def getLapDelta(car=0):
        time = ACLIB.getLapDeltaTime() * 1000
        if time != 0:
            if time < 0:
                return "-" + formatTime(abs(time))
            elif time > 0:
                return "+" + formatTime(abs(time))
        else:
            return "-00:00.000"

    @staticmethod
    def isLapInvalidated(car=0):
        return ac.getCarState(car, AC_PROP.LapInvalidated) or ACLIB.getTyresOut() > 2 or ACLIB.isInPit()

    @staticmethod
    def getLaps():
        if info.graphics.numberOfLaps > 0:
            return info.graphics.numberOfLaps
        else:
            return "-"

    @staticmethod
    def lastSectorTime():
        return info.graphics.lastSectorTime

    @staticmethod
    def getSectors():
        return info.static.sectorCount

    @staticmethod
    def getFocusedCar():
        return ac.getFocusedCar()

    @staticmethod
    def getTraveledDistance():
        return info.graphics.distanceTraveled

    @staticmethod
    def getCarDamage(loc=0):
        # 0: Front, 1: Rear, 2: Left, 3: Right, 4:?
        return info.physics.carDamage[loc]

    @staticmethod
    def getPrevCarDiffTimeDist():
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

    @staticmethod
    def getPrevCarDiff():
        time, dist = ACLIB.getPrevCarDiffTimeDist()
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

    @staticmethod
    def getNextCarDiffTimeDist():
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

    @staticmethod
    def getNextCarDiff():
        time, dist = ACLIB.getNextCarDiffTimeDist()
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

    @staticmethod
    def getGas():
        return info.physics.gas

    @staticmethod
    def getBrake():
        return info.physics.brake

    @staticmethod
    def getClutch():
        return info.physics.clutch

    @staticmethod
    def hasDRS():
        return info.static.hasDRS

    @staticmethod
    def DRSAvailable():
        return info.physics.drsAvailable

    @staticmethod
    def DRSEnabled():
        return info.physics.drsEnabled

    @staticmethod
    def hasERS():
        return info.static.hasERS

    @staticmethod
    def isERSCharging():
        return info.static.ersIsCharging

    @staticmethod
    def ERSMaxJ():
        return info.static.ersMaxJ

    @staticmethod
    def ERSPowerControllerCount():
        return info.static.ersPowerControllerCount

    @staticmethod
    def engineBrakeSettingsCount():
        return info.static.engineBrakeSettingsCount

    @staticmethod
    def hasKERS():
        return info.static.hasKERS

    @staticmethod
    def KERSCharge():
        return info.physics.kersCharge

    @staticmethod
    def KERSInput():
        return info.physics.kersInput

    @staticmethod
    def KERSCurrentKJ():
        return info.static.kersCurrentKJ

    @staticmethod
    def KERSMaxJ():
        return info.static.kersMaxJ

    @staticmethod
    def ABS():
        return info.physics.abs

    @staticmethod
    def getSpeed(car=0, unit="kmh"):
        if unit == "kmh":
            return ac.getCarState(car, AC_PROP.SpeedKMH)
        elif unit == "mph":
            return ac.getCarState(car, AC_PROP.SpeedMPH)
        elif unit == "ms":
            return ac.getCarState(car, AC_PROP.SpeedMS)

    @staticmethod
    def getGear(car=0):
        return formatGear(ac.getCarState(car, AC_PROP.Gear))

    @staticmethod
    def getRPMValue(car=0):
        return ac.getCarState(car, AC_PROP.RPM)

    @staticmethod
    def getRPM(car=0):
        return int(ACLIB.getRPMValue(car))

    @staticmethod
    def getRPMMax():
        if info.static.maxRpm:
            return info.static.maxRpm
        else:
            return 8000

    @staticmethod
    def getPosition(car=0):
        return ac.getCarRealTimeLeaderboardPosition(car) + 1

    @staticmethod
    def getLocation(car=0):
        return ac.getCarState(car, AC_PROP.NormalizedSplinePosition)

    @staticmethod
    def getPenaltyTime():
        return info.graphics.penaltyTime

    @staticmethod
    def isPitLimiterOn():
        return info.physics.pitLimiterOn

    @staticmethod
    def mandatoryPitStopDone():
        return info.graphics.mandatoryPitDone

    @staticmethod
    def isInPit(car=0):
        return ACLIB.isInPitLine(car) or ACLIB.isInPitBox(car)

    @staticmethod
    def isInPitLine(car=0):
        return ac.isCarInPitline(car)

    @staticmethod
    def isInPitBox(car=0):
        return ac.isCarInPit(car)

    @staticmethod
    def isAIDriven():
        return info.physics.isAIControlled

    @staticmethod
    def getFuel():
        return info.physics.fuel

    @staticmethod
    def getMaxFuel():
        return info.static.maxFuel

    @staticmethod
    def getCamberRad(tyre=0):
        return info.physics.camberRAD[tyre]

    @staticmethod
    def getMaxSuspensionTravel(tyre=0):
        return info.static.suspensionMaxTravel[tyre]

    @staticmethod
    def getSuspensionTravel(tyre=0):
        return info.physics.suspensionTravel[tyre]

    @staticmethod
    def getTyresOut():
        return info.physics.numberOfTyresOut

    @staticmethod
    def getTyreWearValue(tyre=0):
        # 0: FL, 1: FR, 2: RL, 3: RR
        return info.physics.tyreWear[tyre]

    @staticmethod
    def getTyreWear(tyre=0):
        return (ACLIB.getTyreWearValue(tyre) - 94) * 16.6

    @staticmethod
    def getTyreWearFormated(tyre=0):
        return "{:2.1f}%".format((ACLIB.getTyreWearValue(tyre) - 94) * 16.6)

    @staticmethod
    def getTyreDirtyLevel(tyre=0):
        return info.physics.tyreDirtyLevel[tyre]

    @staticmethod
    def getTyreCompund():
        return info.graphics.tyreCompound

    @staticmethod
    def getTyreTemp(tyre=0, loc="m"):
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

    @staticmethod
    def getTyreTempFormated(tyre=0, loc="m"):
        return "{:2.1f}°".format(ACLIB.getTyreTemp(tyre, loc))

    @staticmethod
    def getTyrePressure(tyre=0):
        return info.physics.wheelsPressure[tyre]

    @staticmethod
    def getTyrePressureFormated(tyre=0):
        return "{:2.1f}psi".format(ACLIB.getTyrePressure(tyre))

    @staticmethod
    def getBrakeTemperature(tyre=0):
        return info.physics.brakeTemp[tyre]

    @staticmethod
    def getBrakeTemperatureFormated(tyre=0):
        return "{:2.1f}°".format(ACLIB.getBrakeTemperature(tyre))
