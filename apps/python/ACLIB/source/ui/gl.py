import ac
from math import sin, cos
from ui.color import Color


class Texture:
    def __init__(self, file: str):
        self._path = ''
        self.texture = None

        self.path = file

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: str):
        if self._path != path:
            self._path = path

            self.texture = ac.newTexture(self._path)


class Vec2i:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

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


def line(x1: int , y1: int, x2: int, y2: int, color: Color = Color(1, 1, 1, 1)):
    ac.glColor4f(color.r, color.g, color.b, color.a)
    ac.glBegin(1)
    ac.glVertex2f(x1, y1)
    ac.glVertex2f(x2, y2)
    ac.glEnd()


def rect(x: int, y: int, w: int, h: int, color: Color = Color(1, 1, 1, 1), filled: bool = True):

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
        

def quad(x: int, y: int, w: int, h: int, colors=None, r=None):
    if type(colors) == list:
        ac.glBegin(3)
        if len(colors) >= 1:
            c = colors[0]
            ac.glColor4f(c.r, c.g, c.b, c.a)
        if r is not None:
            ac.glVertex2f(r.x, r.y)
        else:
            ac.glVertex2f(x, y)

        if len(colors) >= 2:
            c = colors[1]
            ac.glColor4f(c.r, c.g, c.b, c.a)
        if r is not None:
            ac.glVertex2f(r.x, r.y + r.h)
        else:
            ac.glVertex2f(x, y + h)

        if len(colors) >= 3:
            c = colors[2]
            ac.glColor4f(c.r, c.g, c.b, c.a)
        if r is not None:
            ac.glVertex2f(r.x + r.w, r.y + r.h)
        else:
            ac.glVertex2f(x + w, y + h)

        if len(colors) >= 4:
            c = colors[3]
            ac.glColor4f(c.r, c.g, c.b, c.a)
        if r is not None:
            ac.glVertex2f(r.x + r.w, r.y)
        else:
            ac.glVertex2f(x + w, y)
        ac.glEnd()


def circle(x: int, y: int, radius: int, color: Color = Color(1, 1, 1, 1), filled: bool = True):
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


def arc(x: int, y: int, r: int, start: int = 0, stop: int = 360, color: Color = Color(1, 1, 1, 1), filled: bool = True):
    ac.glColor4f(color.r, color.g, color.b, color.a)
    if filled:
        ac.glBegin(2)
    else:
        ac.glBegin(1)

    sample = (stop - start) / (36 * r)
    while start <= stop:
        rad1 = start
        rad2 = min(start + 1, stop)
        ac.glVertex2f(x + cos(rad1) * r, y - sin(rad1) * r)
        ac.glVertex2f(x + cos(rad2) * r, y - sin(rad2) * r)
        if filled:
            ac.glVertex2f(x, y)

        start += sample

    ac.glEnd()


def donut(x: int, y: int, r: int, w: int, start: int = 0, stop: int = 360, color: Color = Color(1, 1, 1, 1), filled: bool = True):
    ac.glColor4f(color.r, color.g, color.b, color.a)
    if filled:
        ac.glBegin(2)
    else:
        ac.glBegin(1)

    sample = (stop - start) / (36 * r)
    while start <= stop:
        rad1 = start
        rad2 = min(start + 1, stop)
        ac.glVertex2f(x + cos(rad1) * r, y - sin(rad1) * r)
        ac.glVertex2f(x + cos(rad2) * r, y - sin(rad2) * r)
        ac.glVertex2f(x + cos(rad1) * (r - w), y - sin(rad1) * (r - w))
        ac.glVertex2f(x + cos(rad2) * (r - w), y - sin(rad2) * (r - w))
        if filled:
            ac.glVertex2f(x + cos(rad2) * r, y - sin(rad2) * r)
            ac.glVertex2f(x + cos(rad1) * (r - w), y - sin(rad1) * (r - w))

        start += sample

    ac.glEnd()


def polygon(points, color: Color = Color(1, 1, 1, 1), filled: bool = True):
    ac.glColor4f(color.r, color.g, color.b, color.a)
    if filled:
        ac.glBegin(2)
    else:
        ac.glBegin(1)

    for i in points:
        if isinstance(i, Vec2i):
            ac.glVertex2f(i.x, i.y)

    ac.glEnd()


def texture_rect(x: int, y: int, w: int, h: int, color: Color, tex_path: str = '', tex: Texture = None):
    ac.glColor4f(color.r, color.g, color.b, color.a)
    if tex_path:
        ac.glQuadTextured(x, y, w, h, tex_path)
    else:
        ac.glQuadTextured(x, y, w, h, tex.texture)
