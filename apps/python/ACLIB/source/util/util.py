import ac

from source.util.text import *


class Log:
    @staticmethod
    def stringify(*what, end: str = '\n'):
        return '{0}{1}'.format(what, end)


def log(what):
    return ac.log(Log.stringify(what))


def warning(what):
    Log.stringify(what)


def error(what):
    Log.stringify(what)


def console(what):
    ac.console(Log.stringify(what))


class Format:
    @staticmethod
    def s(value, term):
        if abs(value) == 1:
            return str(value) + term
        else:
            return str(value) + term + 's'

    @staticmethod
    def pad(number: [float, int], positions: int = 2):
        return ('{:0' + str(positions) + '}').format(number)

    @staticmethod
    def minute(d=None, h=None, s=None, ms=None, us=None, ns=None):
        pass

    @staticmethod
    def second(d=None, h=None, m=None, ms=None, us=None, ns=None):
        pass

    @staticmethod
    def time(ms: [float, int] = 0, form="{:02d}:{:02d}.{:03d}"):
        millis = abs(int(ms))
        m = int(millis / 60000)
        s = int((millis % 60000) / 1000)
        ms = millis % 1000

        return form.format(m, s, ms)

    @staticmethod
    def distance(meters: [float, int] = 0, form='{:02d}.{:02.0f} km'):
        km = int(meters / 1000)
        m = (meters % 1000) / 10

        return form.format(km, m)

    @staticmethod
    def gear(gear: int):
        if gear == 0:
            return 'R'
        elif gear == 1:
            return 'N'

        return str(gear - 1)

    @staticmethod
    def car_distance(dist_ms: [float, int], dist_meters: [float, int], track_len: [float, int]):
        track_len = max(track_len, 1000)

        if dist_meters > track_len:
            laps = dist_meters / track_len
            if laps > 1.05:
                return '{:3.1f} {}'.format(laps, text(LAPS_ACR))
            elif laps < 1.05:
                return '{:3.0f}   {}'.format(laps, LAP_ACR)

        if dist_ms > 60:
            minute = dist_ms / 60
            if minute > 1.05:
                return '{:3.1f} {}'.format(minute, MINUTES_ACR)
            elif minute < 1.05:
                return '{:3.0f}   {}'.format(minute, MINUTE_ACR)

        return Format.time(int(dist_ms * 1000))


# Iterator that starts again from the beginning after the last item has been reached.
class EndlessIterator:
    def __init__(self, collection):
        self.step = 1
        self.index = 0
        self.collection = collection
        self.len = len(self.collection) - 1

    def __getitem__(self, item):
        return self.collection[self.index]

    def __next__(self):
        return self.next()

    def next(self):
        el = self.collection[self.index]

        if 0 <= self.index + self.step <= self.len:
            self.index += self.step
        else:
            self.index = (self.index + self.step) % self.len + 1

        return el

    def prev(self):
        el = self.collection[self.index]

        if 0 <= self.index - self.step <= self.len:
            self.index -= self.step
        else:
            self.index = (self.index - self.step) % self.len + 1

    def __iadd__(self, other):
        for i in range(0, other):
            self.next()
        return self

    def __add__(self, other):
        for i in range(0, other):
            self.next()
