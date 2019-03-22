import os
import sys
import re
import importlib


class Config:
    def __init__(self, target, special_string=True):
        self.path = ""
        self.section = "DEFAULT"
        self.dictionary = {"DEFAULT": {}}
        self.special_string = special_string

        if os.path.exists(target):
            self.path = target
            f = open(target, mode="r", encoding="utf-8")
            self.read(f.readlines())
        else:
            self.read(target.split("\n"))

    def __iter__(self):
        return iter(self.dictionary)

    def __getitem__(self, item):
        for sec in self.dictionary:
            if item == sec:
                return self.dictionary[sec]
            for key in self.dictionary[sec]:
                if item == key:
                    return self.dictionary[sec][key]
        return -1

    def get(self, section, key=None):
        if key is None:
            return self.dictionary[section]
        else:
            return self.dictionary[section][key]

    def set(self, key, value, section):
        self.dictionary[section][key] = value

    def read(self, lines):
        for line in lines:
            if re.match(r"((;|#|//).*|^\s*$)", line):
                continue

            line = re.sub("[;#].*", "", line).strip()

            if re.match("\[.*\]", line):
                self.section = line.replace("[", "").replace("]", "").strip()
                self.dictionary[self.section] = {}
            else:
                pair = line.split("=")
                if len(pair) == 2:
                    self.readEntry(pair[0].strip(), pair[1].strip())
                elif len(pair) == 1:
                    self.set(pair[0].strip(), -1, self.section)

    def readEntry(self, key, value):
        if value.find(',') >= 0:
            return
        elif re.match(r"^\d*\.\d+$", value):
            value = float(value)
        elif re.match(r"^\d+$", value):
            value = int(value)
        elif re.match("^\".*\"$", value):
            value = value.split('"')[1]
        elif value.lower() in ["t", "true", "y", "yes"]:
            value = True
        elif value.lower() in ["f", "false", "n", "no"]:
            value = False
        else:
            if self.special_string:
                class_path = value[0:value.find("(")].split(".")
                class_name = class_path[-1]
                module_name = '.'.join(class_path[:-1])
                arguments = value[value.find("(") + 1:value.find(")")].split(',')

                # import module from string if not yet imported
                if module_name not in sys.modules.keys():
                    importlib.import_module(module_name)

                class_init = getattr(sys.modules[module_name], class_name)
                value = class_init(*Config.parseArguments(arguments))

        self.set(key, value, self.section)

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
