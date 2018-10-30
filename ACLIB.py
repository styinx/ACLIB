#from source.db import DB
from source.gui import ACApp, ACLabel, ACVBox
from source.aclib import ACLIB, Car
from apps.ACLIB_Driver import Driver
from apps.ACLIB_Tower import Tower
from source.gl import rect


def acMain(version):
    global app, driver, tower
    global vbox, text1, text2, loops, init

    loops = 0
    init = False

    for i in range(0, ACLIB.getCarsCount()):
        ACLIB.CARS[i] = Car(i)

    app = ACApp("ACLIB", 200, 200, 200, 250).hideDecoration()
    driver = Driver()
    tower = Tower()

    text1 = ACLabel("", app)
    text2 = ACLabel("", app)

    vbox = ACVBox(app)
    vbox.addWidget(text1)
    vbox.addWidget(text2)

    app.setRenderCallback(acRender)

    return app.run()


def acUpdate(delta):
    global app, driver, tower
    global text1, text2, loops

    if not app.isSuspended():

        # car = ACLIB.CARS[0]

        if delta < 0.05:
            for car in ACLIB.CARS:
                car.update(delta)

        app.update(delta)
        driver.update(delta)
        tower.update(delta)

        loops += 1
        if loops == 1000:
            loops = 0

    if ACLIB.getSessionStatusId() == 0:
        for car in ACLIB.CARS:
            car.reset()

    # ACLIB.CONSOLE("Delta: " + str(delta))


def acRender(delta):
    global app, init

    if not init:
        for car in ACLIB.CARS:
            car.init()
            init = True

    app.render(delta)


def acShutdown():
    i = 0
