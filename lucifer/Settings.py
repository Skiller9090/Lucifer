from yaml import load, dump, Loader, Dumper
from lucifer.Errors import LuciferFileNotFound, LuciferSettingNotFound
from functools import reduce
import operator
import os


def is_settings():
    return os.path.isfile("settings.yml")


def create_settings(font):
    default_settings = {
        "gui": {
            "font": {
                "name": font[0],
                "size": font[1]
            }
        }
    }
    settings = dump(default_settings, default_flow_style=False)
    with open("settings.yml", "w") as f:
        f.write(settings)


def load_settings():
    if is_settings():
        with open("settings.yml", "r") as f:
            file_data = f.read()
        data = load(file_data, Loader=Loader)
    else:
        raise LuciferFileNotFound("settings.yml")
    return data


def get_setting(setting):
    settings = load_settings()
    setting_split = setting.split(".")
    if settings:
        try:
            return reduce(operator.getitem, setting_split, settings)
        except KeyError as e:
            raise LuciferSettingNotFound(setting)
        except TypeError as e:
            raise LuciferSettingNotFound(setting)
    else:
        print("'settings.yml' file empty, ignoring user settings!")


def update_setting(setting, value):
    if setting != "":
        settings = load_settings()
        to_edit = settings
        setting_split = setting.split(".")
        to_update = setting_split.pop(-1)
        for node in setting_split:
            settings = settings[node]
        settings[to_update] = value
        settings = dump(to_edit, default_flow_style=False)
        with open("settings.yml", "w") as f:
            f.write(settings)
