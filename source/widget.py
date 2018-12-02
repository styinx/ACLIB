from source.aclib import ACLIB
from source.gui import ACWidget, ACGrid, ACProgressBar
from source.gl import rect, quad, line
from source.color import Color
from math import log10

from source.math import Rect


class ACDeltaBarWidget(ACWidget):
    def __init__(self):
        super().__init__(None)

        self.delta = 0
        self.delta_val = 0

    def update(self, delta):
        self.delta = ACLIB.CARS[0].lap_diff
        self.delta_val = max(0.0, log10(abs(delta) + 1)) * self.geometry.w / 2
        return self

    def render(self, delta):
        super().render(delta)

        x, y = self.getPos()
        w, h = self.getSize()

        if self.delta > 0:
            rect(x + (w / 2 - min(w / 2, self.delta_val)), y, min(w / 2, self.delta_val), h, Color(0.9, 0, 0, 1))
        elif self.delta < 0:
            rect(x + w / 2, y, min(w / 2, self.delta_val), h, Color(0, 0.9, 0, 1))

        rect(x, y, w, h, Color(1, 1, 1, 1), False)
        line(x + w / 2, y, x + w / 2, y + h, Color(1, 1, 1, 1))
        return self


class ACFuelWidget(ACGrid):
    def __init__(self, app):
        super().__init__(None, 2, 3)

        self.fuel_level = ACProgressBar(app, 1)

        self.fuel_level.color = Color(1, 1, 0)
        self.fuel_level.background_color = Color(0.75, 0.75, 0.75, 0.5)
        self.fuel_level.max_val = ACLIB.getMaxFuel(0)

        self.addWidget(self.fuel_level, 0, 0, 1, 3)

    def update(self, delta):
        self.fuel_level.value = ACLIB.CARS[0].fuel

    def render(self, delta):
        super().render(delta)

        self.fuel_level.render(delta)


class ACTwinShiftLightWidget(ACWidget):
    def __init__(self, number_of_lights=5, texture=None):
        super().__init__(None)

        self.lights = number_of_lights
        self.texture = texture
        self.rpm = 0
        self.max_rpm = 0

    def update(self, delta):
        self.rpm = ACLIB.CARS[0].rpm
        self.max_rpm = ACLIB.CARS[0].max_rpm
        return self

    def render(self, delta):
        x, y = self.getPos()
        w, h = self.getSize()
        middle_gap = 100
        light_w, light_h = (w - middle_gap) / 4 / self.lights, h
        pos = x

        for i in range(0, self.lights):
            rect(pos, y, light_w, light_h)
            rect(pos, y, light_w, light_h, Color(0, 0, 0), False)
            pos += light_w * 2

        pos = x + w - light_w

        for i in range(0, self.lights):
            rect(pos, y, light_w, light_h)
            rect(pos, y, light_w, light_h, Color(0, 0, 0), False)
            pos -= light_w * 2


class ACTyreWidget(ACWidget):
    def __init__(self):
        super().__init__(None)

        self.temp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.press = [0, 0, 0, 0]
        self.wear = [0, 0, 0, 0]
        self.dirt = [0, 0, 0, 0]

    def update(self, delta):
        self.temp = ACLIB.CARS[0].tyre_temp
        self.press = ACLIB.CARS[0].tyre_pressure
        self.wear = ACLIB.CARS[0].tyre_wear
        self.dirt = ACLIB.CARS[0].tyre_dirt

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
    r = 0.05 * (temp - 120) + 1  # 80
    g = -0.00125 * ((temp - 90) ** 2) + 1  # 70 | 90 | 110
    b = -0.05 * (temp - 60) + 1  # 110
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
