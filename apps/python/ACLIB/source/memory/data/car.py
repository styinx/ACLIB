class Car:
    FRONT = 0
    REAR = 1
    LEFT = 2
    RIGHT = 3
    UNKNOWN = 4

    def __init__(self, info):
        self._info = info

    @property
    def position(self):
        return self._info.graphics.position

    @property
    def skin(self):
        return self._info.static.carSkin

    @property
    def model(self):
        return self._info.static.carModel

    @property
    def class_position(self):
        return 0  # todo

    @property
    def location(self):
        return self._info.graphics.normalizedCarPosition

    @property
    def speed(self):
        return self._info.physics.speedKmh

    @property
    def distance_traveled(self):
        return self._info.graphics.distanceTraveled

    @property
    def velocity(self):
        return self._info.physics.velocity

    @property
    def gear(self):
        return self._info.physics.gear

    @property
    def rpm(self):
        return self._info.physics.rpms

    @property
    def max_rpm(self):
        return self._info.static.maxRpm

    @property
    def fuel(self):
        return self._info.physics.fuel

    @property
    def max_fuel(self):
        return self._info.static.maxFuel

    @property
    def damage(self):
        return self._info.physics.carDamage

    @property
    def abs(self):
        return self._info.physics.abs

    @property
    def tc(self):
        return self._info.physics.tc

    @property
    def drs(self):
        return self._info.physics.drs

    @property
    def has_drs(self):
        return self._info.physics.gear

    @property
    def drs_available(self):
        return self._info.physics.drsAvailable

    @property
    def drs_enabled(self):
        return self._info.physics.drsEnabled

    @property
    def has_ers(self):
        return self._info.static.hasERS

    @property
    def ers_power_level(self):
        return self._info.physics.ersPowerLevel

    @property
    def ers_recovery_level(self):
        return self._info.physics.ersRecoveryLevel

    @property
    def is_ers_charging(self):
        return self._info.physics.ersIsCharging

    @property
    def ers_heat_charging(self):
        return self._info.physics.ersHeatCharging

    @property
    def ers_max_J(self):
        return self._info.static.ersMaxJ

    @property
    def ers_power_count(self):
        return self._info.static.ersPowerControllerCount

    @property
    def has_kers(self):
        return self._info.static.hasERS

    @property
    def kers_current(self):
        return self._info.physics.kersCurrentKJ

    @property
    def kers_input(self):
        return self._info.physics.kersInput

    @property
    def kers_charging(self):
        return self._info.physics.kersCharge

    @property
    def kers_max_J(self):
        return self._info.static.kersMaxJ

    @property
    def has_penalty(self):
        return 0

    @property
    def penalty_time(self):
        return self._info.graphics.penaltyTime

    @property
    def has_mandatory_pit_stop(self):
        return 0

    @property
    def has_mandatory_pit_stop_done(self):
        return self._info.graphics.mandatoryPitDone

    @property
    def is_in_pit(self):
        return self._info.graphics.isInPit

    @property
    def is_in_pit_line(self):
        return self._info.graphics.isInPitLine

    @property
    def is_pit_limiter_on(self):
        return self._info.physics.pitLimiterOn

    @property
    def is_ai_controlled(self):
        return self._info.physics.isAIControlled

    @property
    def has_ideal_line(self):
        return self._info.graphics.idealLineOn
