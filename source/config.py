import os
import sys
import re
import importlib


class Config:
    def __init__(self, path):
        self.path = ""
        self.section = "DEFAULT"
        self.dictionary = {}

        self.read(path)

    def read(self, path):
        self.path = path
        if os.path.exists(path):
            f = open(path, mode="r", encoding="utf-8")
            for line in f.readlines():
                if re.match("\[.*\]", line):
                    self.section = line.replace("[", "").replace("]", "").strip()
                    self.dictionary[self.section] = {}
                else:
                    pair = line.split("=")
                    if len(pair) == 2:
                        self.readEntry(pair[0].strip(), pair[1].strip())
                    elif len(pair) == 1:
                        self.dictionary[self.section][pair[0].strip()] = 0

    def readEntry(self, key, value):
        if re.match("\d*\.\d+", value):
            self.dictionary[self.section][key] = float(value)
        elif re.match("\d+", value):
            self.dictionary[self.section][key] = int(value)
        elif re.match("\".*\"", value):
            self.dictionary[self.section][key] = value.split('"')[1]
        else:
            class_path = value[0:value.find("(")].split(".")
            class_name = class_path[-1]
            module_name = '.'.join(class_path[:-1])
            arguments = value[value.find("(") + 1:value.find(")")].split(',')

            # import module from string if not yet imported
            if module_name not in sys.modules.keys():
                importlib.import_module(module_name)

            class_init = getattr(sys.modules[module_name], class_name)
            self.dictionary[self.section][key] = class_init(*Config.parseArguments(arguments))

    @staticmethod
    def parseArguments(args):
        new_args = []
        for i, arg in enumerate(args):
            val = 0
            if re.match("\d*\.\d+", arg):
                val = float(arg)
            elif re.match("\d+", arg):
                val = int(arg)
            elif re.match("\".*\"", arg):
                val = arg.split('"')[1]
            new_args.append(val)
        return new_args


def loadAppConfig(app, section, path):
    config = Config(path)

    for option in config.dictionary[section]:
        if hasattr(app, option):
            setattr(app, option, config.dictionary[section][option])
