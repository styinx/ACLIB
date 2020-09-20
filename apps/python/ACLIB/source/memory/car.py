import json
import os

from settings import METADATA_DIR, AC_CAR_DIR, AC_TRACK_DIR
from storage.config import Config
from util.util import log


class CarData:
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
        return 0 # todo

    @property
    def location(self):
        return 0 # todo

    @property
    def speed(self):
        return self._info.physics.speedKmh

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


class CarMeta:
    def __init__(self, car_model: str):
        file = open('content/cars/' + car_model + '/ui/ui_car.json', 'r', encoding='utf-8')
        self._car_config = json.loads(file.read(), strict=False)
        file.close()
        self._car_meta = Config(os.path.join(METADATA_DIR, car_model, 'ACLIB_car.ini'))

        self._car_meta.set('name', self._car_config['name'])
        self._car_meta.set('class', self._car_config['tags'][0][1:])
        self._car_meta.set('type', self._car_config['class'])
        self._car_meta.set('brand', self._car_config['brand'])
        self._car_meta.set('brand_badge', 'content/cars/' + car_model + '/ui/badge.png')
        pass

    @property
    def name(self):
        return self._car_meta['name']

    @property
    def class_name(self):
        return self._car_meta['class']

    @property
    def type(self):
        return self._car_meta['type']

    @property
    def brand(self):
        return self._car_meta['brand']

    @property
    def badge(self):
        return self._car_meta['badge']


class TyresData:
    FRONT_LEFT = 0
    FRONT_RIGHT = 1
    REAR_LEFT = 2
    REAR_RIGHT = 3

    def __init__(self, info):
        self._info = info

    @property
    def dirt_level(self):
        return self._info.physics.tyreDirtyLevel

    @property
    def pressure(self):
        return self._info.physics.wheelPressure

    @property
    def wear(self):
        return self._info.physics.tyreWear

    @property
    def inner_temperature(self):
        return self._info.physics.tyreTempI

    @property
    def center_temperature(self):
        return self._info.physics.tyreTempM

    @property
    def outer_temperature(self):
        return self._info.physics.tyreTempO

    @property
    def core_temperature(self):
        return self._info.physics.tyreCoreTemperature

    @property
    def brake_temperature(self):
        return self._info.physics.brakeTemp

    @property
    def suspension_travel(self):
        return self._info.physics.suspensionTravel

    @property
    def max_suspension_travel(self):
        return self._info.physics.suspensionMaxTravel

    @property
    def camber(self):
        return self._info.physics.camberRad

    @property
    def contact_point(self):
        return self._info.physics.tyreContactPoint

    @property
    def contact_normal(self):
        return self._info.physics.tyreContactNormal

    @property
    def contact_heading(self):
        return self._info.physics.tyreContactHeading

    @property
    def slip(self):
        return self._info.physics.wheelSlip

    @property
    def load(self):
        return self._info.physics.wheelLoad

    @property
    def angular_speed(self):
        return self._info.physics.wheelAngularSpeed

    @property
    def compound(self):
        return self._info.graphics.tyreCompound

    @property
    def compound_name(self):
        compound = self.compound
        return compound[:compound.find('(')].strip()

    @property
    def compound_symbol(self):
        compound = self.compound
        return compound[compound.find('(') + 1:compound.find(')')].strip()


class TyresMeta:
    def __init__(self, car_model: str, acd: dict):
        self._acd = acd
        self._tyre_config = Config(self._acd['tyres.ini'], only_strings=True)
        self._tyre_meta = Config(os.path.join(METADATA_DIR, car_model, 'ACLIB_tyres.ini'))

        compound = ''
        for sec_name, section in self._tyre_config.dict.items():
            if 'NAME' in section:
                compound = section['NAME']

            if compound and section:
                self._tyre_meta.select(compound)

                if sec_name.find('THERMAL_FRONT') > -1 or sec_name.find('THERMAL_REAR') > -1:
                    position = 'front' if sec_name.find('THERMAL_FRONT') > -1 else 'rear'
                    self._tyre_meta.set(position + '_tcurve', self._lut_dict(section['PERFORMANCE_CURVE']))

                elif sec_name.find('FRONT') > -1 or sec_name.find('REAR') > -1:
                    position = 'front' if sec_name.find('FRONT') > -1 else 'rear'
                    self._tyre_meta.set(position + '_ideal_pressure', section['PRESSURE_IDEAL'])
                    self._tyre_meta.set(position + '_wear', self._lut_dict(section['WEAR_CURVE']))

    def _lut_dict(self, file: str):
        content = self._acd[file]
        d = {}
        for line in content.split('\n'):
            if line.find('|') > -1:
                k, v = line.split('|')
                d[k] = v
        return d

    def ideal_pressure(self, compound: str, front: bool):
        key = 'front' if front else 'rear'
        return self._tyre_meta.dict[compound][key + '_ideal_pressure']

    def ideal_temperature(self, compound: str, front: bool):
        key = 'front' if front else 'rear'
        min_max = [float(k) for k, v in self._tyre_meta.dict[compound][key + '_tcurve'].items() if v == '1.0']
        return min(min_max), max(min_max)
