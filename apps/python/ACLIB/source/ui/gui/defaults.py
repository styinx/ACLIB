import os

from settings import STYLE_DIR, CONFIG_DIR, path
from storage.config import Config


class WidgetConfig:
    @staticmethod
    def load_app_config(app: object, app_name: str):
        app_config_file = path(CONFIG_DIR, app_name + '.ini')
        if os.path.isfile(app_config_file):
            config = Config(app_config_file)

            if config:
                section = 'DEFAULT'
                if app_name in config:
                    section = app_name
                for prop, val in config.dict[section].items():
                    if hasattr(app, prop):
                        setattr(app, prop, val)

            return config
        return Config(app_config_file)


class WidgetStyle:
    STYLE = {}

    @staticmethod
    def load_style_from_config(obj: object, class_name: str, app_name: str = None):
        # If style was not already loaded
        if class_name not in WidgetStyle.STYLE:
            config = None

            # Try to load from app style config
            if app_name:
                app_style_file = path(STYLE_DIR, app_name + '.ini')
                if os.path.isfile(app_style_file):
                    config = Config(app_style_file)

            # Try to load from widget style config
            if not config:
                class_style_file = path(STYLE_DIR, class_name + '.ini')
                if os.path.isfile(class_style_file):
                    config = Config(class_style_file)

            # Store the style
            if config:
                if class_name in config.dict:
                    WidgetStyle.STYLE[class_name] = config.dict[class_name]
                else:
                    WidgetStyle.STYLE[class_name] = config.dict['DEFAULT']

        if class_name in WidgetStyle.STYLE:
            for prop, val in WidgetStyle.STYLE[class_name].items():
                if hasattr(obj, prop):
                    setattr(obj, prop, val)
