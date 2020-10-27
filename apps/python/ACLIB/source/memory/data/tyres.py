class Tyres:
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
        return self._info.physics.wheelsPressure

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
    def brake_bias(self):
        return self._info.physics.brakeBias

    @property
    def suspension_travel(self):
        return self._info.physics.suspensionTravel

    @property
    def max_suspension_travel(self):
        return self._info.physics.suspensionMaxTravel

    @property
    def camber(self):
        return self._info.physics.camberRAD

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
