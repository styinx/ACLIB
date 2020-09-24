# Storage interface
class Storage:
    def __init__(self, file: str):
        self._file = file
        self._topic = None

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file: str):
        self._file = file

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, topic: str):
        self._topic = topic

    def query(self, statement: str):
        raise NotImplemented

    def create(self, topic: str, extra: str = None):
        raise NotImplemented

    def drop(self, topic: str):
        raise NotImplemented

    def select(self, topic: str):
        self.topic = topic

    def insert(self, key: str, value: str):
        raise NotImplemented

    def get(self, key: str, value: str):
        raise NotImplemented

    def get_all(self):
        raise NotImplemented

    def update(self, key: str, value: str, new: str):
        raise NotImplemented

    def delete(self, key: str, value: str):
        raise NotImplemented
