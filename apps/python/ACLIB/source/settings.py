import os
from os.path import join, realpath, normpath
from storage.config import Config

def path(first: str, *other):
    return normpath(join(first, *other))

USER_DIR = os.path.expanduser('~')
AC_DOC_DIR = path(USER_DIR, 'Documents', 'Assetto Corsa')
ACLIB_DOC_DIR = path(AC_DOC_DIR, 'ACLIB')
ACLIB_INSTALL_DIR = path(realpath(__file__), '..', '..')
AC_INSTALL_DIR = path(ACLIB_INSTALL_DIR, '..', '..', '..')
AC_CONTENT_DIR = path(AC_INSTALL_DIR, 'content')
AC_CAR_DIR = path(AC_CONTENT_DIR, 'cars')
AC_TRACK_DIR = path(AC_CONTENT_DIR, 'tracks')

APP_DIR = path(ACLIB_INSTALL_DIR, 'apps')
RESOURCE_DIR = path(ACLIB_INSTALL_DIR, 'resources')
TEXTURE_DIR = path(RESOURCE_DIR, 'textures')
CONFIG_DIR = path(ACLIB_DOC_DIR, 'config')
METADATA_DIR = path(ACLIB_DOC_DIR, 'metadata')
STYLE_DIR = path(ACLIB_DOC_DIR, 'style')

CONFIG = Config(path(CONFIG_DIR, 'ACLIB.ini'))


def get(key: str):
    return CONFIG.get(key)


def get_or_set(key: str, value):
    result = get(key)

    if not result:
        CONFIG.set(key, value)
        return value

    return result


get_or_set('write_acd', True)
get_or_set('write_meta', False)
get_or_set('log_to_AC', False)
