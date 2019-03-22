import os
import sys
import importlib
from source.aclib import ACLIB, SESSION
from source.config import Config


def acMain(version):
    global init, apps

    init = False
    apps = []
    aclib_config = Config("apps/python/ACLIB/config/ACLIB.ini")

    ACLIB.setup()

    for module in os.listdir("apps/python/ACLIB/apps/"):
        try:
            module = "apps." + module[:module.rfind(".")]
            if module not in sys.modules.keys():
                importlib.import_module(module)
            class_init = getattr(sys.modules[module], module[module.find("_") + 1:])
            apps.append(class_init())
        except Exception as e:
            ACLIB.CONSOLE("Module '" + module + "' made some problems: " + str(e))


def acUpdate(delta):
    global init, apps, loops

    if ACLIB.getSessionStatusId() != 2:
        SESSION.init()
        ACLIB.init()
        for app in apps:
            app.init()

    SESSION.update()
    ACLIB.update(delta)

    for app in apps:
        if app.update_timer >= app.update_time:
            app.update(delta)
            app.update_timer = 0
        else:
            app.update_timer += delta


def acShutdown():
    i = 0
