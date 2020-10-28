import ac
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
from ui.gui.ac_widget import ACApp


class ACLIB:
    APPS = {}
    TIMER = 0
    DEBUG = False
    AC_DATA = None
    AC_META = None

    @staticmethod
    def init():
        for aclib_path in [ACLIB_DOC_DIR, CONFIG_DIR, METADATA_DIR, STYLE_DIR]:
            if not os.path.exists(aclib_path):
                os.makedirs(aclib_path)

        ACLIB.DEBUG = get_or_set('debug', False)

        Log.init()

        Log.LOG_2_AC = get_or_set('log_to_AC', False)

        ACLIB.AC_DATA = ACData()
        ACLIB.AC_META = ACMeta(ACLIB.AC_DATA)

        # Dummy used to put apps in the same category.
        aclib = ACApp('ACLIB', -10000, -10000, 0, 0, True, True)
        aclib.visible = False
        ACLIB.APPS[aclib.title] = aclib

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

                    class_obj = class_ctor(ACLIB.AC_DATA, ACLIB.AC_META)
                    ACLIB.APPS[class_obj.title] = class_obj
                    log('Init {0:s}'.format(module))

            except Exception as e:
                log('Problems while initializing {0:s}'.format(file_name))
                tb(e)

        ACLIB.AC_DATA.init()

    except Exception as e:
        tb(e)

    return 'ACLIB'


def acUpdate(delta: float):
    ACLIB.TIMER += delta

    # Update every 10 milliseconds.
    if ACLIB.TIMER > 0.01:
        ACLIB.TIMER = 0

        try:
            ac.ext_perfBegin('ACLIB_Standalone')
            ACLIB.AC_DATA.update(delta)
            ac.ext_perfEnd('ACLIB_Standalone')

            # Call the update function for every app stored in the app list.
            for _, app in ACLIB.APPS.items():
                if app.active:
                    try:
                        if not app.no_update:
                            ac.ext_perfBegin(app.title)
                            app.update(delta)
                            ac.ext_perfEnd(app.title)
                    except Exception as e:
                        log('Problems while updating app "{0:s}"'.format(app.title))
                        tb(e)

        except Exception as e:
            tb(e)


def acShutdown():
    try:
        ACLIB.AC_DATA.shutdown()

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
