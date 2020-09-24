import os
import sys
import platform
import importlib

arch = platform.architecture()[0][0:2]
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib', arch))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps'))
os.environ['PATH'] = os.environ['PATH'] + ";."

from settings import *
from util.log import log, tb, Log
from memory.ac_data import ACData
from memory.ac_meta import ACMeta


class ACLIB:
    APPS = {}
    DATA = None
    META = None

    @staticmethod
    def init():
        for aclib_path in [ACLIB_DOC_DIR, CONFIG_DIR, METADATA_DIR, STYLE_DIR]:
            if not os.path.exists(aclib_path):
                os.makedirs(aclib_path)

        Log.init()

        Log.LOG_2_AC = get('log_to_AC')

        ACLIB.DATA = ACData()
        ACLIB.META = ACMeta(ACLIB.DATA)

    @staticmethod
    def shutdown():
        Log.shutdown()


def acMain(version: int = 0):
    try:
        ACLIB.init()

        # Search for all 'ACLIB_<appname>.py' files in the apps directory.
        files_list = [str(m) for m in os.listdir(APP_DIR) if os.path.isfile(path(APP_DIR, m))]
        for file_name in files_list:
            try:
                # Filename without .py extension
                module = file_name[:file_name.rfind(".")]

                if module.find('ACLIB_') > -1:
                    # Import the app to the current program if not yet done.
                    if module not in sys.modules.keys():
                        importlib.import_module(module)

                    # Initialize the class with the constructor and store it in the app list.
                    class_ctor = getattr(sys.modules[module], module[module.find('ACLIB_') + 6:])
                    class_obj = class_ctor(ACLIB.DATA, ACLIB.META)
                    ACLIB.APPS[class_ctor] = class_obj
                    log('Init {0:s}'.format(module))

            except Exception as e:
                log('Problems while initializing {0:s}'.format(file_name))
                tb(e)

    except Exception as e:
        tb(e)

    return 'ACLIB'


def acUpdate(delta: int = 0):
    try:
        ACLIB.DATA.update(delta)

        # Call the update function for every app stored in the app list.
        for _, app in ACLIB.APPS.items():
            try:
                app.update(delta)
            except Exception as e:
                log('Problems while updating app "{0:s}"'.format(app.title))
                tb(e)
    except Exception as e:
        tb(e)


def acShutdown():
    try:
        ACLIB.DATA.shutdown()

        # Call the update function for every app stored in the app list.
        for _, app in ACLIB.APPS.items():
            try:
                log('Shutdown {0:s}'.format(app.title))
                app.shutdown()
            except Exception as e:
                log('Problems while shutting down app "{0:s}"'.format(app.title))
                tb(e)

        CONFIG.write()
        ACLIB.shutdown()
    except Exception as e:
        tb(e)
