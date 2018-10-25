class Color:
    def __init__(self, r, g, b, a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __iadd__(self, other):
        self.r = max(min(other.r + self.r, 1), 0)
        self.g = max(min(other.g + self.g, 1), 0)
        self.b = max(min(other.b + self.b, 1), 0)
        self.a = max(min(other.a + self.a, 1), 0)

    def __add__(self, other):
        return Color(max(min(other.r + self.r, 1), 0),
                     max(min(other.g + self.g, 1), 0),
                     max(min(other.b + self.b, 1), 0),
                     max(min(other.a + self.a, 1), 0))

    def __lt__(self, other):
        return self.r < other.r and self.g < other.g and self.b < other.b and self.a < other.a

    def __le__(self, other):
        return self.r <= other.r and self.g <= other.g and self.b <= other.b and self.a <= other.a

    def hsv(self, h, s, v):
        i = 0

    def hex(self, hex_val):
        self.r = int(hex_val[1:3], 16)
        self.g = int(hex_val[3:5], 16)
        self.b = int(hex_val[5:7], 16)
        self.a = 1.0

    def tohex(self):
        return "#" + hex(self.r)[-2:] + hex(self.g)[-2:] + hex(self.b)[-2:]


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


def interpolateRGB(start, stop, steps):
    colors = []

    for i in range(0, steps):
        step = i / steps
        r = (stop.r - start.r) * step + start.r
        g = (stop.g - start.g) * step + start.g
        b = (stop.b - start.b) * step + start.b
        a = (stop.a - start.a) * step + start.a

        colors.append(Color(round(r, 2), round(g, 2), round(b, 2), round(a, 2)))

    return colors


def interpolateHSV(start, stop, steps):
    colors = []

    for i in range(0, steps):
        step = i / steps
        r = (stop.r - start.r) * step + start.r
        g = (stop.g - start.g) * step + start.g
        b = (stop.b - start.b) * step + start.b
        a = (stop.a - start.a) * step + start.a

        colors.append(Color(round(r, 2), round(g, 2), round(b, 2), round(a, 2)))

    return colors
