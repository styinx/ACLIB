import ac
from math import sin, cos
from source.color import Color


class Texture:
    def __init__(self, path):
        self.path = path
        self.texture = ac.newTexture(path)


class Vec2i:
    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other):
        return Vec2i(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vec2i(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, val):
        return Vec2i(self.x * val, self.y * val)

    def __imul__(self, val):
        self.x *= val
        self.y *= val
        return self


def line(x1, y1, x2, y2, color=Color(1, 1, 1, 1)):
    if not isinstance(color, Color):
        raise Exception("Argument is not a Color")

    ac.glColor4f(color.r, color.g, color.b, color.a)
    ac.glBegin(1)
    ac.glVertex2f(x1, y1)
    ac.glVertex2f(x2, y2)
    ac.glEnd()


def rect(x, y, w, h, color=Color(1, 1, 1, 1), filled=True, r=None):
    if not isinstance(color, Color):
        raise Exception("Argument is not a Color")

    ac.glColor4f(color.r, color.g, color.b, color.a)
    if filled:
        ac.glQuad(x, y, w, h)
    else:
        ac.glBegin(1)
        ac.glVertex2f(x, y)
        ac.glVertex2f(x + w, y)
        ac.glVertex2f(x + w, y)
        ac.glVertex2f(x + w, y + h)
        ac.glVertex2f(x + w, y + h)
        ac.glVertex2f(x, y + h)
        ac.glVertex2f(x, y + h)
        ac.glVertex2f(x, y)
        ac.glEnd()
        

def quad(x, y, w, h, colors):
    if type(colors) == list:
        ac.glBegin(3)
        if len(colors) >= 1:
            c = colors[0]
            ac.glColor4f(c.r, c.g, c.b, c.a)
        ac.glVertex2f(x, y)
        if len(colors) >= 2:
            c = colors[1]
            ac.glColor4f(c.r, c.g, c.b, c.a)
        ac.glVertex2f(x, y + h)
        if len(colors) >= 3:
            c = colors[2]
            ac.glColor4f(c.r, c.g, c.b, c.a)
        ac.glVertex2f(x + w, y + h)
        if len(colors) >= 4:
            c = colors[3]
            ac.glColor4f(c.r, c.g, c.b, c.a)
        ac.glVertex2f(x + w, y)
        ac.glEnd()


def circle(x, y, radius, color=Color(1, 1, 1, 1), filled=True):
    if not isinstance(color, Color):
        raise Exception("Argument is not a Color")

    ac.glColor4f(color.r, color.g, color.b, color.a)
    if filled:
        ac.glBegin(2)
    else:
        ac.glBegin(1)

    start = 0
    stop = 360
    sample = 36 * radius
    while start <= stop:
        rad1 = start
        rad2 = min(start + 1, stop)
        ac.glVertex2f(x + cos(rad1) * radius, y - sin(rad1) * radius)
        ac.glVertex2f(x + cos(rad2) * radius, y - sin(rad2) * radius)
        if filled:
            ac.glVertex2f(x, y)

        start += sample

    ac.glEnd()


def arc(x, y, radius, start=0, stop=360, color=Color(1, 1, 1, 1), filled=True):
    if not isinstance(color, Color):
        raise Exception("Argument is not a Color")

    ac.glColor4f(color.r, color.g, color.b, color.a)
    if filled:
        ac.glBegin(2)
    else:
        ac.glBegin(1)

    sample = (stop - start) / (36 * radius)
    while start <= stop:
        rad1 = start
        rad2 = min(start + 1, stop)
        ac.glVertex2f(x + cos(rad1) * radius, y - sin(rad1) * radius)
        ac.glVertex2f(x + cos(rad2) * radius, y - sin(rad2) * radius)
        if filled:
            ac.glVertex2f(x, y)

        start += sample

    ac.glEnd()


def donut(x, y, radius, width, start=0, stop=360, color=Color(1, 1, 1, 1), filled=True):
    if not isinstance(color, Color):
        raise Exception("Argument is not a Color")

    ac.glColor4f(color.r, color.g, color.b, color.a)
    if filled:
        ac.glBegin(2)
    else:
        ac.glBegin(1)

    sample = (stop - start) / (36 * radius)
    while start <= stop:
        rad1 = start
        rad2 = min(start + 1, stop)
        ac.glVertex2f(x + cos(rad1) * radius, y - sin(rad1) * radius)
        ac.glVertex2f(x + cos(rad2) * radius, y - sin(rad2) * radius)
        ac.glVertex2f(x + cos(rad1) * (radius - width), y - sin(rad1) * (radius - width))
        ac.glVertex2f(x + cos(rad2) * (radius - width), y - sin(rad2) * (radius - width))
        if filled:
            ac.glVertex2f(x + cos(rad2) * radius, y - sin(rad2) * radius)
            ac.glVertex2f(x + cos(rad1) * (radius - width), y - sin(rad1) * (radius - width))

        start += sample

    ac.glEnd()


def polygon(points, color=Color(1, 1, 1, 1), filled=True):
    if not isinstance(color, Color):
        raise Exception("Argument is not a Color")

    ac.glColor4f(color.r, color.g, color.b, color.a)
    if filled:
        ac.glBegin(2)
    else:
        ac.glBegin(1)

    for i in points:
        if isinstance(i, Vec2i):
            ac.glVertex2f(i.x, i.y)

    ac.glEnd()


def texture_rect(x, y, w, h, tex, color):
    if not isinstance(tex, Texture):
        raise Exception("Argument is not a Texture")

    if not isinstance(color, Color):
        raise Exception("Argument is not a Color")

    ac.glColor4f(color.r, color.g, color.b, color.a)
    ac.glQuadTextured(x, y, w, h, tex.texture)
