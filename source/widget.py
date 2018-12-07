from source.aclib import ACLIB
from source.gui import ACWidget, ACGrid, ACProgressBar, ACLabel
from source.gl import rect, quad, line
from source.color import Color
from math import log10

from source.math import Rect


# Mirrored single bar elements
class ACTwinShiftLightWidget(ACWidget):
    def __init__(self, number_of_lights=10, texture=None):
        super().__init__(None)

        self.lights = max(number_of_lights, 1)
        self.middle_gap = 100
        self.texture = texture
        self.rpm = 0
        self.max_rpm = 0

    def update(self, delta):
        car = ACLIB.getFocusedCar()
        self.rpm = ACLIB.CARS[car].rpm
        self.max_rpm = ACLIB.CARS[car].max_rpm
        return self

    def render(self, delta):
        x, y = self.getPos()
        w, h = self.getSize()
        light_w, light_h = (w - self.middle_gap) / 4 / self.lights, h
        pos = x
        progress = min(self.rpm / self.max_rpm, 1)

        for i in range(0, min(self.lights, int(progress * self.lights))):
            col = Color(2 * (i * progress / self.lights), 2 * (1 - (i * progress / self.lights)), 0)
            rect(pos, y, light_w, light_h, col)
            rect(pos, y, light_w, light_h, Color(0.25, 0.25, 0.25), False)
            pos += light_w * 2

        pos = x + w - light_w

        for i in range(0, min(self.lights, int(progress * self.lights))):
            col = Color(2 * (i * progress / self.lights), 2 * (1 - (i * progress / self.lights)), 0)
            rect(pos, y, light_w, light_h, col)
            rect(pos, y, light_w, light_h, Color(0.25, 0.25, 0.25), False)
            pos -= light_w * 2
        return self


# Single bar elements
class ACShiftLightWidget(ACWidget):
    def __init__(self, number_of_lights=15, texture=None):
        super().__init__(None)

        self.lights = max(number_of_lights, 1)
        self.texture = texture
        self.rpm = 0
        self.max_rpm = 0

    def update(self, delta):
        car = ACLIB.getFocusedCar()
        self.rpm = ACLIB.CARS[car].rpm
        self.max_rpm = ACLIB.CARS[car].max_rpm
        return self

    def render(self, delta):
        x, y = self.getPos()
        w, h = self.getSize()
        light_w, light_h = w / 2 / self.lights, h
        pos = x
        progress = min(self.rpm / self.max_rpm, 1)

        for i in range(0, min(self.lights, int(progress * self.lights))):
            col = Color(2 * (i * progress / self.lights), 2 * (1 - (i * progress / self.lights)), 0)
            rect(pos, y, light_w, light_h, col)
            rect(pos, y, light_w, light_h, Color(0.25, 0.25, 0.25), False)
            pos += light_w * 2 + light_w / self.lights
        return self


# Continuous bar
class ACShiftLightBarWidget(ACWidget):
    def __init__(self, texture=None):
        super().__init__(None)

        self.texture = texture
        self.rpm = 0
        self.max_rpm = 0

    def update(self, delta):
        car = ACLIB.getFocusedCar()
        self.rpm = ACLIB.CARS[car].rpm
        self.max_rpm = ACLIB.CARS[car].max_rpm
        return self

    def render(self, delta):
        x, y = self.getPos()
        w, h = self.getSize()

        progress = min(self.rpm / self.max_rpm, 1)
        progress_color = Color(2 * progress, 2 * (1 - progress), 0)
        quad(x, y, w * progress, h, [Color(0, 1, 0), Color(0, 1, 0), progress_color, progress_color])
        rect(x, y, w * progress, h, Color(0.25, 0.25, 0.25), False)
        return self


class ACDeltaBarWidget(ACWidget):
    def __init__(self):
        super().__init__(None)

        self.delta = 0
        self.delta_val = 0

    def update(self, delta):
        self.delta = ACLIB.CARS[ACLIB.getFocusedCar()].performance
        self.delta_val = max(0.0, log10(abs(self.delta) + 1) / 2) * self.geometry.w / 2
        return self

    def render(self, delta):
        x, y = self.getPos()
        w, h = self.getSize()

        if self.delta > 0:
            rect(x + (w / 2 - min(w / 2, self.delta_val)), y, min(w / 2, self.delta_val), h, Color(0.9, 0, 0, 1))
        elif self.delta < 0:
            rect(x + w / 2, y, min(w / 2, self.delta_val), h, Color(0, 0.9, 0, 1))
        else:
            pass

        rect(x, y, w, h, Color(1, 1, 1, 1), False)
        line(x + w / 2, y, x + w / 2, y + h, Color(1, 1, 1, 1))
        return self


class ACDamageWidget(ACWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)

    def update(self, delta):
        return self

    def render(self, delta):
        return self


class ACFuelWidget(ACWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)

    def update(self, delta):
        return self

    def render(self, delta):
        x, y = self.getPos()
        w, h = self.getSize()

        car = ACLIB.CARS[0]

        fuel = h * car.fuel / car.max_fuel
        lap = h * car.lap_fuel / car.max_fuel
        km = h * car.km_fuel / car.max_fuel

        rect(x, y + h - fuel, w / 2, fuel, Color(1, 1, 0))
        rect(x + w * 0.25, y + h - fuel, w * 0.25, lap, Color(1, 0, 0))
        rect(x, y + h - fuel, w * 0.125, km, Color(0, 0, 1))
        rect(x, y, w / 2, h, Color(1, 1, 1), False)
        return self


class ACTyreWidget(ACWidget):
    def __init__(self):
        super().__init__(None)

        self.temp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.press = [0, 0, 0, 0]
        self.wear = [0, 0, 0, 0]
        self.dirt = [0, 0, 0, 0]

    def update(self, delta):
        car = ACLIB.getFocusedCar()
        self.temp = ACLIB.CARS[car].tyre_temp
        self.press = ACLIB.CARS[car].tyre_pressure
        self.wear = ACLIB.CARS[car].tyre_wear
        self.dirt = ACLIB.CARS[car].tyre_dirt
        return self

    def render(self, delta):
        t_w, t_h = 24, 34
        h_space, v_space = 10, 10
        x, y = self.getPos()

        # tyre 1

        index = 0
        pfl_col = tyrePressureColor(self.press[index])
        wfl_col = tyreWearColor(self.wear[index])
        tfl_col = [tyreTempColor(self.temp[index][0]),
                   tyreTempColor(self.temp[index][1]),
                   tyreTempColor(self.temp[index][2]),
                   tyreTempColor(self.temp[index][3])]

        if self.dirt[index] > 0:
            colors1 = [tyreDirtColor(self.dirt[index])] * 4
            colors2 = colors1
            colors3 = colors1
            colors4 = colors1
        else:
            colors1 = [tfl_col[0], tfl_col[0], tfl_col[3], tfl_col[1]]
            colors2 = [tfl_col[1], tfl_col[3], tfl_col[2], tfl_col[2]]
            colors3 = [tfl_col[0], tfl_col[0], tfl_col[1], tfl_col[3]]
            colors4 = [tfl_col[3], tfl_col[1], tfl_col[2], tfl_col[2]]

        base = Rect(x, y, t_w / 2, t_h / 2)
        quad(colors=colors1, r=base)
        quad(colors=colors2, r=base + Rect(t_w / 2))
        quad(colors=colors3, r=base + Rect(y=t_h / 2))
        quad(colors=colors4, r=base + Rect(t_w / 2, t_h / 2))

        # tyre 2

        index = 1
        pfl_col = tyrePressureColor(self.press[index])
        wfl_col = tyreWearColor(self.wear[index])
        tfl_col = [tyreTempColor(self.temp[index][0]),
                   tyreTempColor(self.temp[index][1]),
                   tyreTempColor(self.temp[index][2]),
                   tyreTempColor(self.temp[index][3])]

        if self.dirt[index] > 0:
            colors1 = [tyreDirtColor(self.dirt[index])] * 4
            colors2 = colors1
            colors3 = colors1
            colors4 = colors1
        else:
            colors1 = [tfl_col[0], tfl_col[0], tfl_col[3], tfl_col[1]]
            colors2 = [tfl_col[1], tfl_col[3], tfl_col[2], tfl_col[2]]
            colors3 = [tfl_col[0], tfl_col[0], tfl_col[1], tfl_col[3]]
            colors4 = [tfl_col[3], tfl_col[1], tfl_col[2], tfl_col[2]]

        base = Rect(x + t_w + h_space, y, t_w / 2, t_h / 2)
        quad(colors=colors1, r=base)
        quad(colors=colors2, r=base + Rect(t_w / 2))
        quad(colors=colors3, r=base + Rect(y=t_h / 2))
        quad(colors=colors4, r=base + Rect(t_w / 2, t_h / 2))

        # tyre 3

        index = 2
        pfl_col = tyrePressureColor(self.press[index])
        wfl_col = tyreWearColor(self.wear[index])
        tfl_col = [tyreTempColor(self.temp[index][0]),
                   tyreTempColor(self.temp[index][1]),
                   tyreTempColor(self.temp[index][2]),
                   tyreTempColor(self.temp[index][3])]

        if self.dirt[index] > 0:
            colors1 = [tyreDirtColor(self.dirt[index])] * 4
            colors2 = colors1
            colors3 = colors1
            colors4 = colors1
        else:
            colors1 = [tfl_col[0], tfl_col[0], tfl_col[3], tfl_col[1]]
            colors2 = [tfl_col[1], tfl_col[3], tfl_col[2], tfl_col[2]]
            colors3 = [tfl_col[0], tfl_col[0], tfl_col[1], tfl_col[3]]
            colors4 = [tfl_col[3], tfl_col[1], tfl_col[2], tfl_col[2]]

        base = Rect(x, y + t_h + v_space, t_w / 2, t_h / 2)
        quad(colors=colors1, r=base)
        quad(colors=colors2, r=base + Rect(t_w / 2))
        quad(colors=colors3, r=base + Rect(y=t_h / 2))
        quad(colors=colors4, r=base + Rect(t_w / 2, t_h / 2))

        # tyre 4

        index = 3
        pfl_col = tyrePressureColor(self.press[index])
        wfl_col = tyreWearColor(self.wear[index])
        tfl_col = [tyreTempColor(self.temp[index][0]),
                   tyreTempColor(self.temp[index][1]),
                   tyreTempColor(self.temp[index][2]),
                   tyreTempColor(self.temp[index][3])]

        if self.dirt[index] > 0:
            colors1 = [tyreDirtColor(self.dirt[index])] * 4
            colors2 = colors1
            colors3 = colors1
            colors4 = colors1
        else:
            colors1 = [tfl_col[0], tfl_col[0], tfl_col[3], tfl_col[1]]
            colors2 = [tfl_col[1], tfl_col[3], tfl_col[2], tfl_col[2]]
            colors3 = [tfl_col[0], tfl_col[0], tfl_col[1], tfl_col[3]]
            colors4 = [tfl_col[3], tfl_col[1], tfl_col[2], tfl_col[2]]

        base = Rect(x + t_w + h_space, y + t_h + v_space, t_w / 2, t_h / 2)
        quad(colors=colors1, r=base)
        quad(colors=colors2, r=base + Rect(t_w / 2))
        quad(colors=colors3, r=base + Rect(y=t_h / 2))
        quad(colors=colors4, r=base + Rect(t_w / 2, t_h / 2))
        return self


def tyreTempColor(temp):
    c = ACLIB.CARS[ACLIB.getFocusedCar()]
    mid = c.tyre_ideal_temp_min + (c.tyre_ideal_temp_max - c.tyre_ideal_temp_min) / 2

    r = 0.025 * (temp - c.tyre_ideal_temp_max) + 0.3
    g = -0.00125 * ((temp - mid) ** 2) + 1
    b = -0.025 * (temp - c.tyre_ideal_temp_min) + 0.3
    return Color(r, g, b)


def tyrePressureColor(press):
    r = -0.002 * ((press - 50) ** 2) + 1
    g = -0.001 * ((press - 25) ** 2) + 1
    b = -0.002 * (press ** 2) + 1
    return Color(r, g, 0)


def tyreWearColor(wear):
    r = -0.04 * (wear - 40) + 1
    g = -0.0001 * ((wear - 100) ** 2) + 1
    return Color(r, g, 0)


def tyreDirtColor(dirt):
    r = 1 - (dirt / 5) * 0.7
    g = 0.75 - (dirt / 5) * 0.6
    return Color(r, g, 0, dirt * 2)
