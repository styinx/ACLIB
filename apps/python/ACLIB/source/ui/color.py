class Color:
    def __init__(self, r: float, g: float, b: float, a: float = 1.0):
        self.r = max(min(r, 1.0), 0.0)
        self.g = max(min(g, 1.0), 0.0)
        self.b = max(min(b, 1.0), 0.0)
        self.a = max(min(a, 1.0), 0.0)

    def __iadd__(self, other):
        self.r = max(min(self.r + other.r, 1.0), 0.0)
        self.g = max(min(self.g + other.g, 1.0), 0.0)
        self.b = max(min(self.b + other.b, 1.0), 0.0)
        self.a = max(min(self.a + other.a, 1.0), 0.0)
        return self

    def __add__(self, other):
        return Color(max(min(self.r + other.r, 1.0), 0.0),
                     max(min(self.g + other.g, 1.0), 0.0),
                     max(min(self.b + other.b, 1.0), 0.0),
                     max(min(self.a + other.a, 1.0), 0.0))

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a

    def __ne__(self, other):
        return not (self == other)

    def __imul__(self, other: float):
        if -1 <= other <= 1:
            self.r *= other
            self.g *= other
            self.b *= other
            self.a *= other
        return self


class AnimationColor:
    def __init__(self, r: float, g: float, b: float, a: float = 1.0):
        self.r = max(min(r, 1.0), -1.0)
        self.g = max(min(g, 1.0), -1.0)
        self.b = max(min(b, 1.0), -1.0)
        self.a = max(min(a, 1.0), -1.0)

    def __iadd__(self, other):
        self.r = max(min(self.r + other.r, 1.0), -1.0)
        self.g = max(min(self.g + other.g, 1.0), -1.0)
        self.b = max(min(self.b + other.b, 1.0), -1.0)
        self.a = max(min(self.a + other.a, 1.0), -1.0)
        return self

    def __add__(self, other):
        return AnimationColor(max(min(self.r + other.r, 1.0), -1.0),
                     max(min(self.g + other.g, 1.0), -1.0),
                     max(min(self.b + other.b, 1.0), -1.0),
                     max(min(self.a + other.a, 1.0), -1.0))

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a

    def __ne__(self, other):
        return not (self == other)

    def __mul__(self, other: float):
        c = AnimationColor(self.r, self.g, self.b, self.a)
        if -1 <= other <= 1:
            c.r *= other
            c.g *= other
            c.b *= other
            c.a *= other
        return c

    def __imul__(self, other: float):
        if -1 <= other <= 1:
            self.r *= other
            self.g *= other
            self.b *= other
            self.a *= other
        return self


def interpolate(value: float, min_val: float, max_val: float, min_color: Color, max_color: Color):
    max_val, min_val = max(max_val, min_val), min(max_val, min_val)
    value_range = max_val - min_val
    if value_range > 0:
        min_weight = (max_val - value) / value_range
        max_weight = 1 - min_weight
        r = min_color.r * min_weight + max_color.r * max_weight
        g = min_color.g * min_weight + max_color.g * max_weight
        b = min_color.b * min_weight + max_color.b * max_weight
        a = min_color.a * min_weight + max_color.a * max_weight

        return Color(round(r, 2), round(g, 2), round(b, 2), round(a, 2))
    return min_color


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
