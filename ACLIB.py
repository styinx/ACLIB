#from source.db import DB
from source.gui import ACApp
from source.aclib import ACLIB
from apps.ACLIB_Driver import Driver
from apps.ACLIB_Tower import Tower


def acMain(version):
    global app, driver, tower
    global init

    init = False
    loop = -100

    ACLIB.setup()

    app = ACApp("ACLIB", 200, 200, 200, 250).hideDecoration()
    driver = Driver()
    tower = Tower()
    app.setRenderCallback(acRender)

    return app.run()


def acUpdate(delta):
    global app, driver, tower, init

    ACLIB.update(delta)

    app.update(delta)
    driver.update(delta)
    tower.update(delta)

    if ACLIB.getSessionStatusId() != 2 and not init:
        ACLIB.reset()
        ACLIB.init()
        init = True


def acRender(delta):
    global app

    app.render(delta)


def acShutdown():
    i = 0
