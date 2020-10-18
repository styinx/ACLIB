import sys
import traceback

import ac
from settings import ACLIB_DOC_DIR, path
from util.format import Format


class Log:
    LOG_2_AC = False
    HANDLE = None
    FILE = path(ACLIB_DOC_DIR, 'log.txt')
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


def log(*what, flush: bool = False):
    if Log.LOGS <= Log.MAX_LOGS:
        Log.LOGS += 1
        if Log.LOG_2_AC:
            return ac.log(Log.stringify(Format.time(), *what))
        else:
            Log.HANDLE.write(Log.stringify(Format.time(), *what))
            if flush:
                Log.HANDLE.flush()


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
