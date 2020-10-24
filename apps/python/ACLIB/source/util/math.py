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

    def set(self, x=0, y=0):
        self.x = x
        self.y = y
        return self

    def add(self, x=0, y=0):
        self.x += x
        self.y += y
        return self

    def tuple(self) -> tuple:
        return self.x, self.y


class Rect:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

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

    def mid(self) -> Point:
        return Point(self.x + int(self.w / 2), self.y + int(self.h / 2))

    def topLeft(self) -> Point:
        return Point(self.x, self.y)

    def bottomRight(self) -> Point:
        return Point(self.x + self.w, self.y + self.h)

    @staticmethod
    def rectOverlapping(l, r) -> bool:
        tl1, br1 = l.topLeft(), l.bottomRight()
        tl2, br2 = r.topLeft(), r.bottomRight()

        if tl1.x > br2.x or br1.x < tl2.x:
            return False

        if tl1.y > br2.y or br1.y < tl2.y:
            return False

        return True

    @staticmethod
    def pointInRect(p, r) -> bool:
        tl, br = r.topLeft(), r.bottomRight()

        if p.x < tl.x or p.x > br.x:
            return False

        if p.y < tl.y or p.y > br.y:
            return False

        return True


class Size:
    def __init__(self, w=0, h=0):
        self.w = w
        self.h = h

    def __iadd__(self, other):
        self.w += other.w
        self.h += other.h
        return self

    def __imul__(self, other):
        self.w *= other
        self.h *= other
        return self

    def __add__(self, other):
        return Size(self.w + other.w,
                    self.h + other.h)

    def __eq__(self, other):
        return self.w == other.w and self.h == other.h

    def __ne__(self, other):
        return not (self == other)

    def set(self, w=0, h=0):
        self.w = w
        self.h = h
        return self

    def add(self, w=0, h=0):
        self.w += w
        self.h += h
        return self

    def tuple(self) -> tuple:
        return self.w, self.h
