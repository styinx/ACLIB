import os
from os.path import join, realpath, normpath
from storage.config import Config

USER_DIR = os.path.expanduser('~')
AC_DOC_DIR = join(USER_DIR, 'Documents', 'Assetto Corsa')
ACLIB_DOC_DIR = join(AC_DOC_DIR, 'ACLIB')
ACLIB_INSTALL_DIR = normpath(join(realpath(__file__), '..', '..'))
AC_INSTALL_DIR = normpath(join(ACLIB_INSTALL_DIR, '..', '..', '..'))
AC_CONTENT_DIR = normpath(join(AC_INSTALL_DIR, 'content'))
AC_CAR_DIR = normpath(join(AC_CONTENT_DIR, 'cars'))
AC_TRACK_DIR = normpath(join(AC_CONTENT_DIR, 'tracks'))

APP_DIR = join(ACLIB_INSTALL_DIR, 'apps')
RESOURCE_DIR = join(ACLIB_INSTALL_DIR, 'resources')
TEXTURE_DIR = join(RESOURCE_DIR, 'textures')
CONFIG_DIR = join(ACLIB_DOC_DIR, 'config')
METADATA_DIR = join(ACLIB_DOC_DIR, 'metadata')
STYLE_DIR = join(ACLIB_DOC_DIR, 'style')

CONFIG = Config(join(CONFIG_DIR, 'ACLIB.ini'))

def config(key: str):
    return CONFIG.get(key) or False
