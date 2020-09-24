class Color:
    def __init__(self, r, g, b, a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __iadd__(self, other):
        self.r = max(min(self.r + other.r, 1), 0)
        self.g = max(min(self.g + other.g, 1), 0)
        self.b = max(min(self.b + other.b, 1), 0)
        self.a = max(min(self.a + other.a, 1), 0)
        return self

    def __add__(self, other):
        return Color(max(min(self.r + other.r, 1), 0),
                     max(min(self.g + other.g, 1), 0),
                     max(min(self.b + other.b, 1), 0),
                     max(min(self.a + other.a, 1), 0))

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a

    def __ne__(self, other):
        return not (self == other)

    def __imul__(self, other):
        self.r *= other
        self.g *= other
        self.b *= other
        self.a *= other
        return self

    def hsv(self, h, s, v):
        i = 0

    def hex(self, hex_val):
        self.r = int(hex_val[1:3], 16)
        self.g = int(hex_val[3:5], 16)
        self.b = int(hex_val[5:7], 16)
        self.a = 1.0

    def tohex(self):
        return '#' + hex(self.r)[-2:] + hex(self.g)[-2:] + hex(self.b)[-2:]


# def rgb2hsv(color):
#     if not isinstance(color, Color):
#         return None
#
#     r = color.r
#     g = color.g
#     b = color.b
#     max_val = max(r, g, b)
#     min_val = min(r, g, b)
#     c = max_val - min_val
#     hue = 0
#     segment = 0
#     shift = 0
#
#     if c != 0:
#         if max_val == r:
#             segment = (g - b) / c
#             shift = 0 / 60
#             if segment < 0:
#                 shift = 360 / 60
#
#         elif max_val == g:
#             segment = (b - r) / c
#             shift = 120 / 60
#
#         elif max_val == b:
#             segment = (r - g) / c
#             shift = 240 / 60
#
#         hue = segment + shift
#
#     return hue * 60
#
#
# def hsv2rgb(color):
#     if not isinstance(color, Color):
#         return None
#
#     r = color.r
#     g = color.g
#     b = color.b
#     max_val = max(r, g, b)
#     min_val = min(r, g, b)
#     c = max_val - min_val
#     hue = 0
#     segment = 0
#     shift = 0
#
#     if c != 0:
#         if max_val == r:
#             segment = (g - b) / c
#             shift = 0 / 60
#             if segment < 0:
#                 shift = 360 / 60
#
#         elif max_val == g:
#             segment = (b - r) / c
#             shift = 120 / 60
#
#         elif max_val == b:
#             segment = (r - g) / c
#             shift = 240 / 60
#
#         hue = segment + shift
#
#     return hue * 60


def interpolateRGB(start: Color, stop: Color, steps: int):
    colors = []

    for i in range(0, steps):
        step = i / steps
        r = (stop.r - start.r) * step + start.r
        g = (stop.g - start.g) * step + start.g
        b = (stop.b - start.b) * step + start.b
        a = (stop.a - start.a) * step + start.a

        colors.append(Color(round(r, 2), round(g, 2), round(b, 2), round(a, 2)))

    return colors


def interpolateHSV(start: Color, stop: Color, steps: int):
    colors = []

    for i in range(0, steps):
        step = i / steps
        r = (stop.r - start.r) * step + start.r
        g = (stop.g - start.g) * step + start.g
        b = (stop.b - start.b) * step + start.b
        a = (stop.a - start.a) * step + start.a

        colors.append(Color(round(r, 2), round(g, 2), round(b, 2), round(a, 2)))

    return colors


# todo check range for negative value
#
# Example:
# - Start color = Color(0, 0, 1, 1)
# - Stop color = Color(1, 0, 0, 1)
# - Start value = 0
# - Stop value = 100
# - Value = 50
# -> Resulting color = Color(0.5, 0, 0.5, 1)
def interpolate(value: float, min_val: float, max_val: int, min_color: Color, max_color: Color):
    value_range = max_val - min_val
    min_weight = (max_val - value) / value_range
    max_weight = 1 - min_weight
    r = min_color.r * min_weight + max_color.r * max_weight
    g = min_color.g * min_weight + max_color.g * max_weight
    b = min_color.b * min_weight + max_color.b * max_weight
    a = min_color.a * min_weight + max_color.a * max_weight

    return Color(round(r, 2), round(g, 2), round(b, 2), round(a, 2))


TRANSPARENT = Color(0.0, 0.0, 0.0, 0.0)
BLACK = Color(0.0, 0.0, 0.0, 1.0)
BLACK90 = Color(0.0, 0.0, 0.0, 0.9)
BLACK80 = Color(0.0, 0.0, 0.0, 0.8)
BLACK70 = Color(0.0, 0.0, 0.0, 0.7)
BLACK60 = Color(0.0, 0.0, 0.0, 0.6)
BLACK50 = Color(0.0, 0.0, 0.0, 0.5)
BLUE = Color(0.0, 0.0, 1.0, 1.0)
BLUE90 = Color(0.0, 0.0, 1.0, 0.9)
BLUE80 = Color(0.0, 0.0, 1.0, 0.8)
BLUE70 = Color(0.0, 0.0, 1.0, 0.7)
BLUE60 = Color(0.0, 0.0, 1.0, 0.6)
BLUE50 = Color(0.0, 0.0, 1.0, 0.5)
GREEN = Color(0.0, 1.0, 0.0, 1.0)
GREEN90 = Color(0.0, 1.0, 0.0, 0.9)
GREEN80 = Color(0.0, 1.0, 0.0, 0.8)
GREEN70 = Color(0.0, 1.0, 0.0, 0.7)
GREEN60 = Color(0.0, 1.0, 0.0, 0.6)
GREEN50 = Color(0.0, 1.0, 0.0, 0.5)
CYAN = Color(0.0, 1.0, 1.0, 1.0)
LIGHTGRAY = Color(0.25, 0.25, 0.25, 1.0)
PURPLE = Color(0.5, 0.0, 0.5, 1.0)
GRAY = Color(0.5, 0.5, 0.5, 1.0)
DARKGRAY = Color(0.75, 0.75, 0.75, 1.0)
RED = Color(1.0, 0.0, 0.0, 1.0)
RED90 = Color(1.0, 0.0, 0.0, 0.9)
RED80 = Color(1.0, 0.0, 0.0, 0.8)
RED70 = Color(1.0, 0.0, 0.0, 0.7)
RED60 = Color(1.0, 0.0, 0.0, 0.6)
RED50 = Color(1.0, 0.0, 0.0, 0.5)
MAGENTA = Color(1.0, 0.0, 1.0, 1.0)
ORANGE = Color(1.0, 0.5, 0.0, 1.0)
YELLOW = Color(1.0, 1.0, 0.0, 1.0)
WHITE = Color(1.0, 1.0, 1.0, 1.0)
