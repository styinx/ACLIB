import os
import sys
import traceback
from time import strftime, localtime

import ac
from settings import ACLIB_DOC_DIR

from util.text import *


class Log:
    LOG_2_AC = False
    HANDLE = None
    FILE = os.path.join(ACLIB_DOC_DIR, 'log.txt')
    LOGS = 0
    CONSOLE = 0
    MAX_LOGS = 1000
    MAX_CONSOLE = 1000

    @staticmethod
    def init():
        Log.HANDLE = open(Log.FILE, 'w+')

    @staticmethod
    def shutdown():
        Log.HANDLE.close()

    @staticmethod
    def stringify(*what, end: str = '\n'):
        return '{0}{1}'.format(' '.join(map(str, what)), end)


def log(*what):
    if Log.LOGS <= Log.MAX_LOGS:
        Log.LOGS += 1
        if Log.LOG_2_AC:
            return ac.log(Log.stringify(Format.time(), *what))
        else:
            Log.HANDLE.write(Log.stringify(Format.time(), *what))


def tb(e: Exception):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    log('Exception: "{}" of type "{}" for object "{} ({})"\n{}'.format(
        e, exc_type, exc_tb, type(exc_tb), traceback.format_exc()))


def warning(*what):
    return Log.stringify(*what)


def error(*what):
    return Log.stringify(*what)


def console(*what):
    if Log.CONSOLE <= Log.MAX_CONSOLE:
        Log.CONSOLE += 1
        ac.console(Log.stringify(*what))


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
    def time():
        return strftime("%H:%M:%S", localtime())

    @staticmethod
    def duration(ms: [float, int] = 0, form="{:02d}:{:02d}.{:03d}"):
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
    def rpm(rpm: int):
        return '{:d}'.format(rpm)

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

        return Format.duration(int(dist_ms * 1000))


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

        return el

    def __iadd__(self, other):
        for i in range(0, other):
            self.next()
        return self

    def __add__(self, other):
        for i in range(0, other):
            self.next()
