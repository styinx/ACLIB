import os
import sys
import importlib

#from source.db import DB
from source.aclib import ACLIB, SESSION

def acMain(version):
    global init, apps

    init = False
    loop = -100
    apps = []

    ACLIB.setup()

    for module in os.listdir("apps/python/ACLIB/apps/"):
        module = "apps." + module[:module.rfind(".")]
        if module not in sys.modules.keys():
            importlib.import_module(module)
        class_init = getattr(sys.modules[module], module[module.find("_") + 1:])
        apps.append(class_init())


def acUpdate(delta):
    global init, apps

    if ACLIB.getSessionStatusId() != 2 and not init:
        SESSION.init()
        ACLIB.init()
        for app in apps:
            app.init()
        init = True

    SESSION.update()
    ACLIB.update(delta)

    for app in apps:
        app.update(delta)


def acShutdown():
    i = 0
