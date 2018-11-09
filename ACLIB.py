#from source.db import DB
from source.gui import ACApp, ACLabel, ACVBox
from source.aclib import ACLIB, Car
from apps.ACLIB_Driver import Driver
from apps.ACLIB_Tower import Tower


def acMain(version):
    global app, driver, tower
    global loops, init

    loops = 0
    init = False

    ACLIB.setup()

    app = ACApp("ACLIB", 200, 200, 200, 250).hideDecoration()
    driver = Driver()
    tower = Tower()
    app.setRenderCallback(acRender)

    return app.run()


def acUpdate(delta):
    global app, driver, tower
    global loops

    if not app.isSuspended():
        ACLIB.update(delta)

        app.update(delta)
        driver.update(delta)
        tower.update(delta)

        loops += 1
        if loops == 1000:
            loops = 0

    if ACLIB.getSessionStatusId() != 2:
        ACLIB.reset()


def acRender(delta):
    global app, init

    if not init:
        ACLIB.init()
        init = True

    app.render(delta)


def acShutdown():
    i = 0
