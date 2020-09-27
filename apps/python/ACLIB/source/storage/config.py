import os
import sys
import re
import importlib
from collections import OrderedDict

from storage.storage import Storage

# Parameters:
# only_string:  Some config files might define string values without ' or ".
#               This option should be used to read these values as strings.
class Config(Storage):
    def __init__(self,
                 file: str = '',
                 comments: list = None,
                 only_strings = False):
        super().__init__(file)

        self._dict = OrderedDict()
        self._comments = comments if comments is not None else [';', '#', '//']
        self._only_strings = only_strings

        self.topic = 'DEFAULT'
        self._dict['DEFAULT'] = {}

        if file.endswith('.ini'):
            self._file = file

            if os.path.isfile(file):
                f = open(file, mode='r', encoding='utf-8')
                self.read_lines(f.readlines())
                f.close()
        else:
            self.read_lines(file.split('\n'))

    def __iter__(self):
        return iter(self._dict)

    def __getitem__(self, item: str):
        for sec in self._dict:
            if item == sec:
                return self._dict[sec]
            for key in self._dict[sec]:
                if item == key:
                    return self._dict[sec][key]
        return None

    @property
    def dict(self):
        return self._dict

    # Use this function to get a value when you don't know where its stored.
    # Search a section: statement = '[#].? = ?' or more specific '[Settings].resolution = ?'
    # Search a key:     statement = '[?].# = ?'
    # Search a value:   statement = '[?].? = #'
    def query(self, statement: str):
        for section in self._dict:
            pass

    def create(self, topic: str, extra: str = None):
        if topic not in self._dict:
            self._dict[topic] = {}

    def drop(self, topic: str):
        del self._dict[topic]

    def select(self, topic: str):
        if topic:
            if topic not in self._dict:
                self.create(topic)

            self.topic = topic

    def insert(self, key: str, value: str):
        self._dict[self.topic][key] = value

    def get(self, key: str, value: str = None):
        if key in self._dict[self.topic]:
            return self._dict[self.topic][key]
        return None

    def get_all(self):
        return self._dict[self.topic]

    def update(self, key: str, value: str, new: str):
        self.insert(key, new)

    def delete(self, key: str, value: str):
        del self._dict[self.topic][key]

    def write(self, file: str = None):
        if file is not None:
            self._file = file

        path = self._file[:self._file.rfind('/')]

        if not os.path.exists(path):
            os.makedirs(path)

        h = open(self.file, 'w+')

        for section, values in self._dict.items():
            h.write('[{}]\n'.format(section))
            for key, val in values.items():
                h.write(str(key) + ' = ' + str(val) + '\n')
            h.write('\n')

        h.close()

    def set(self, key: str, value, topic: str = ''):
        if topic:
            self.select(topic)
        self.insert(key, value)

    def read_lines(self, lines: list):
        comments_pipe = '|'.join(self._comments)
        comments_plain = ''.join(self._comments)

        for line in lines:
            line = line.strip()

            # Commented
            if re.match(r'^({})'.format(comments_pipe), line):
                continue

            line = re.sub(r'\s*[{}].*$'.format(comments_plain), '', line).strip()

            # Empty
            if not line:
                continue

            # Section
            if re.match('^\[.*\]$', line):
                new_topic = line.replace('[', '').replace(']', '').strip()
                self.select(new_topic)

            # Key-value pair
            else:
                pair = line.split('=')
                if len(pair) == 2:
                    self.read_entry(pair[0].strip(), pair[1].strip())
                elif len(pair) == 1:
                    self.set(pair[0].strip(), None, self.topic)

    def read_entry(self, key: str, value):
        if self._only_strings:
            value = str(value)
        else:
            value = Config.parse_value(value)

        self.set(key, value, self.topic)

    @staticmethod
    def parse_value(arg: str):
        first = arg[0]
        last = arg[-1]

        if first == '[' and last == ']':
            return eval(arg)
        elif first == '(' and last == ')':
            return eval(arg)
        elif re.match(r'\d*\.\d+', arg):
            return float(arg)
        elif re.match(r'\d+', arg):
            return int(arg)
        elif re.match(r'\'.*\'', arg):
            return arg.split('\'')[1]
        elif re.match(r'\".*\"', arg):
            return arg.split('\"')[1]
        elif arg.lower() in ['t', 'true', 'y', 'yes']:
            return True
        elif arg.lower() in ['f', 'false', 'n', 'no']:
            return False
        elif re.match(r'[\w\.]+\(.*\)', arg):
            for match in re.findall(r'([\w\.]+\().*\)', arg):
                class_path = match[:-1].split('.')
                module_name = '.'.join(class_path[:-1])

                arg = arg.replace(module_name + '.', '')

                if module_name not in sys.modules.keys():
                    importlib.import_module(module_name)
            print(eval(arg))

            return eval(arg)
        return None
