class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __add__(self, other):
        return Point(self.x + other.x,
                     self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)


class Rect:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def set(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        return self

    def add(self, x=0, y=0, w=0, h=0):
        self.x += x
        self.y += y
        self.w += w
        self.h += h
        return self

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.w += other.w
        self.h += other.h
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        self.w *= other
        self.h *= other
        return self

    def __add__(self, other):
        return Rect(self.x + other.x,
                    self.y + other.y,
                    self.w + other.w,
                    self.h + other.h)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.w == other.w and self.h == other.h

    def __ne__(self, other):
        return not (self == other)
