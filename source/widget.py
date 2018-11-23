from source.gui import ACWidget
from source.gl import rect, quad, line
from source.color import Color
from math import log10


class ACDeltaBarWidget(ACWidget):
    def __init__(self):
        super().__init__(None)

        self.delta = 0
        self.delta_val = 0

    def setDelta(self, delta):
        self.delta = delta
        self.delta_val = max(0.0, log10(abs(delta) + 1)) * self._geometry.w / 2
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


class ACFuelWidget(ACWidget):
    def __init__(self):
        super().__init__(None)


class ACTwinShiftLightWidget(ACWidget):
    def __init__(self, number_of_lights=5, texture=None):
        super().__init__(None)

        self.lights = number_of_lights
        self.texture = texture
        self.rpm = 0
        self.max_rpm = 0

    def setRpm(self, rpm):
        self.rpm = rpm

    def render(self, delta):
        light_w, light_h = 32, 32
        middle_gap = 100
        x, y = self.getPos()
        w, h = self.getSize()

        for i in range(0, self.lights * 2):
            rect(x, y, light_w, light_h)
            rect(x, y, light_w, light_h, Color(0, 0, 0), False)
            if i == self.lights:
                x += middle_gap
            else:
                x += w / self.lights


class ACTyreWidget(ACWidget):
    def __init__(self):
        super().__init__(None)

        self.temp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.press = [0, 0, 0, 0]
        self.wear = [0, 0, 0, 0]
        self.dirt = [0, 0, 0, 0]

    def setTemperature(self, values):
        self.temp = values
        return self

    def setPressure(self, values):
        self.press = values
        return self

    def setWear(self, values):
        self.wear = values
        return self

    def setDirt(self, values):
        self.dirt = values
        return self

    def render(self, delta):
        super().render(delta)

        t_w, t_h = 24, 34
        h_space, v_space = 10, 10
        dirt_space = 2
        x, y = self.getPos()

        # tyre 1

        dfl_col = tyreDirtColor(self.dirt[0])
        rect(x, y, t_w, t_h, dfl_col)

        tfl = self.temp[0]
        tfl_i_col = tyreTempColor(tfl[2])
        tfl_m_col = tyreTempColor(tfl[1])
        tfl_o_col = tyreTempColor(tfl[0])
        tfl_c_col = tyreTempColor(tfl[3])
        quad(x + dirt_space, y + dirt_space, t_w / 2 - dirt_space, t_h - dirt_space * 2,
             colors=[tfl_o_col, tfl_o_col, tfl_m_col, tfl_m_col])
        quad(x + t_w / 2, y + dirt_space, t_w / 2 - dirt_space, t_h - dirt_space * 2,
             colors=[tfl_m_col, tfl_m_col, tfl_i_col, tfl_i_col])
        rect(x + dirt_space + t_w * 0.3, y + dirt_space + t_h * 0.2,
             (t_w - 2 * dirt_space) * 0.3, (t_h - 2 * dirt_space) * 0.3, tfl_c_col)
        rect(x + dirt_space + t_w * 0.3, y + dirt_space + t_h * 0.2,
             (t_w - 2 * dirt_space) * 0.3, (t_h - 2 * dirt_space) * 0.3, Color(0, 0, 0), False)

        pfl_col = tyrePressureColor(self.press[0])
        rect(x + dirt_space + t_w * 0.2, y + dirt_space + t_h * 0.6,
             (t_w - 2 * dirt_space) * 0.6, (t_h - 2 * dirt_space) * 0.2, pfl_col)
        rect(x + dirt_space + t_w * 0.2, y + dirt_space + t_h * 0.6,
             (t_w - 2 * dirt_space) * 0.6, (t_h - 2 * dirt_space) * 0.2, Color(0, 0, 0), False)

        wfl_col = tyreWearColor(self.wear[0])
        wfl_offset = self.wear[0] / 100 * t_h
        rect(x + dirt_space * 2 + t_w, y + t_h - wfl_offset, h_space * 0.5, wfl_offset, wfl_col)
        rect(x + dirt_space * 2 + t_w, y, h_space * 0.5, t_h, Color(0, 0, 0), False)

        # tyre 2

        dfr_col = tyreDirtColor(self.dirt[1])
        rect(x + t_w + h_space, y, t_w, t_h, dfr_col)

        tfr = self.temp[1]
        tfr_i_col = tyreTempColor(tfr[0])
        tfr_m_col = tyreTempColor(tfr[1])
        tfr_o_col = tyreTempColor(tfr[2])
        tfr_c_col = tyreTempColor(tfr[3])
        quad(x + t_w + h_space + dirt_space, y + dirt_space, t_w / 2 - dirt_space, t_h - dirt_space * 2,
             colors=[tfr_i_col, tfr_i_col, tfr_m_col, tfr_m_col])
        quad(x + t_w + h_space + t_w / 2, y + dirt_space, t_w / 2 - dirt_space, t_h - dirt_space * 2,
             colors=[tfr_m_col, tfr_m_col, tfr_o_col, tfr_o_col])
        rect(x + t_w + h_space + dirt_space + t_w * 0.3, y + dirt_space + t_h * 0.2,
             (t_w - 2 * dirt_space) * 0.3, (t_h - 2 * dirt_space) * 0.3, tfr_c_col)
        rect(x + t_w + h_space + dirt_space + t_w * 0.3, y + dirt_space + t_h * 0.2,
             (t_w - 2 * dirt_space) * 0.3, (t_h - 2 * dirt_space) * 0.3, Color(0, 0, 0), False)

        pfr_col = tyrePressureColor(self.press[1])
        rect(x + t_w + h_space + dirt_space + t_w * 0.2, y + dirt_space + t_h * 0.6,
             (t_w - 2 * dirt_space) * 0.6, (t_h - 2 * dirt_space) * 0.2, pfr_col)
        rect(x + t_w + h_space + dirt_space + t_w * 0.2, y + dirt_space + t_h * 0.6,
             (t_w - 2 * dirt_space) * 0.6, (t_h - 2 * dirt_space) * 0.2, Color(0, 0, 0), False)

        # tyre 3

        drl_col = tyreDirtColor(self.dirt[2])
        rect(x, y + t_h + v_space, t_w, t_h, dfr_col)

        trl = self.temp[2]
        trl_i_col = tyreTempColor(trl[2])
        trl_m_col = tyreTempColor(trl[1])
        trl_o_col = tyreTempColor(trl[0])
        trl_c_col = tyreTempColor(trl[3])
        quad(x + dirt_space, y + t_h + v_space + dirt_space, t_w / 2 - dirt_space, t_h - dirt_space * 2,
             colors=[trl_o_col, trl_o_col, trl_m_col, trl_m_col])
        quad(x + t_w / 2, y + t_h + v_space + dirt_space, t_w / 2 - dirt_space, t_h - dirt_space * 2,
             colors=[trl_m_col, trl_m_col, trl_i_col, trl_i_col])
        rect(x + dirt_space + t_w * 0.3, y + t_h + v_space + dirt_space + t_h * 0.2,
             (t_w - 2 * dirt_space) * 0.3, (t_h - 2 * dirt_space) * 0.3, trl_c_col)
        rect(x + dirt_space + t_w * 0.3, y + t_h + v_space + dirt_space + t_h * 0.2,
             (t_w - 2 * dirt_space) * 0.3, (t_h - 2 * dirt_space) * 0.3, Color(0, 0, 0), False)

        prl_col = tyrePressureColor(self.press[2])
        rect(x + dirt_space + t_w * 0.2, y + t_h + v_space + dirt_space + t_h * 0.6,
             (t_w - 2 * dirt_space) * 0.6, (t_h - 2 * dirt_space) * 0.2, trl_c_col)
        rect(x + dirt_space + t_w * 0.2, y + t_h + v_space + dirt_space + t_h * 0.6,
             (t_w - 2 * dirt_space) * 0.6, (t_h - 2 * dirt_space) * 0.2, Color(0, 0, 0), False)

        wrl_col = tyreWearColor(self.wear[2])
        wrl_offset = self.wear[2] / 100 * t_h
        rect(x + dirt_space * 2 + t_w, y + t_h + v_space + t_h - wrl_offset, h_space * 0.5, wrl_offset, wrl_col)
        rect(x + dirt_space * 2 + t_w, y + t_h + v_space, h_space * 0.5, t_h, Color(0, 0, 0), False)

        # tyre 4

        drr_col = tyreDirtColor(self.dirt[3])
        rect(x + t_w + h_space, y + t_h + v_space, t_w, t_h, dfr_col)

        trr = self.temp[3]
        trr_i_col = tyreTempColor(trr[0])
        trr_m_col = tyreTempColor(trr[1])
        trr_o_col = tyreTempColor(trr[2])
        trr_c_col = tyreTempColor(trr[3])
        quad(x + t_w + h_space + dirt_space, y + t_h + v_space + dirt_space, t_w / 2 - dirt_space, t_h - dirt_space * 2,
             colors=[trr_i_col, trr_i_col, trr_m_col, trr_m_col])
        quad(x + t_w + h_space + t_w / 2, y + t_h + v_space + dirt_space, t_w / 2 - dirt_space, t_h - dirt_space * 2,
             colors=[trr_m_col, trr_m_col, trr_o_col, trr_o_col])
        rect(x + t_w + h_space + dirt_space + t_w * 0.3, y + t_h + v_space + dirt_space + t_h * 0.2,
             (t_w - 2 * dirt_space) * 0.3, (t_h - 2 * dirt_space) * 0.3, trr_c_col)
        rect(x + t_w + h_space + dirt_space + t_w * 0.3, y + t_h + v_space + dirt_space + t_h * 0.2,
             (t_w - 2 * dirt_space) * 0.3, (t_h - 2 * dirt_space) * 0.3, Color(0, 0, 0), False)

        prr_col = tyrePressureColor(self.press[3])
        rect(x + t_w + h_space + dirt_space + t_w * 0.2, y + t_h + v_space + dirt_space + t_h * 0.6,
             (t_w - 2 * dirt_space) * 0.6, (t_h - 2 * dirt_space) * 0.2, trr_c_col)
        rect(x + t_w + h_space + dirt_space + t_w * 0.2, y + t_h + v_space + dirt_space + t_h * 0.6,
             (t_w - 2 * dirt_space) * 0.6, (t_h - 2 * dirt_space) * 0.2, Color(0, 0, 0), False)

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
    r = 0.8 - dirt * 0.75
    g = 0.6 - dirt * 0.75
    b = 0.2 - dirt * 0.5
    return Color(r, g, b, dirt * 2)
