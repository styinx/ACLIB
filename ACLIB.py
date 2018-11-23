#from source.db import DB
from source.aclib import ACLIB, SESSION
from apps.ACLIB_Driver import Driver
from apps.ACLIB_Tower import Tower
from apps.ACLIB_Test import Test


def acMain(version):
    global driver, tower, test
    global init

    init = False
    loop = -100

    ACLIB.setup()
    driver = Driver()
    tower = Tower()
    test = Test()


def acUpdate(delta):
    global driver, tower, test
    global init

    SESSION.update()
    ACLIB.update(delta)

    driver.update(delta)
    tower.update(delta)
    test.update(delta)

    if ACLIB.getSessionStatusId() != 2 and not init:
        SESSION.init()
        ACLIB.reset()
        ACLIB.init()
        driver.init()
        init = True

    # s = ""
    # for time in SESSION.best_mini_sector_time:
    #     if time != float("inf"):
    #         s += formatTime(time) + " | "
    # ACLIB.CONSOLE(s)
    #
    # s = ""
    # for time in SESSION.best_sector_time:
    #     if time != float("inf"):
    #         s += formatTime(time) + " | "
    # ACLIB.CONSOLE(s)


def acShutdown():
    i = 0
