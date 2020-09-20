import os
import sqlite3
from sqlite3 import Error

from storage.storage import Storage
from util.util import log
from util.text import *


class History:
    def __init__(self, max_len: int = 10):
        self._statements = []
        self._max_len = max_len

    def __iadd__(self, other):
        self._statements.append(other)
        if len(self._statements) > self._max_len:
            self._statements = self._statements[1:self._max_len]
        return self

class SQLite3DB(Storage):
    def __init__(self, file: str):
        super().__init__(os.path.join(os.path.abspath(os.getcwd()), file))
        self._connection = None
        self._cursor = None
        self._statement = None
        self._history = History()

        try:
            log(text(LOG_DB_CREATE).format(self._file))
            self._connection = sqlite3.connect(self._file)
            self._cursor = self._connection.cursor()
        except Error as e:
            self._connection.close()
            self._connection = None
            self._cursor = None
            raise BaseException(text(EXCEPTION_DB_CREATE).format(self._file, e))

    def _commit(self, fetch: bool = False):
        try:
            self._history += self._statement
            log(text(LOG_DB_EXECUTE).format(self._statement))
            if fetch:
                return self._cursor.execute(self._statement).fetchall()
            else:
                self._cursor.execute(self._statement)
                self._connection.commit()
        except Exception as e:
            raise BaseException(text(EXCEPTION_DB_COMMIT).format(self._statement, e))

    def query(self, statement: str):
        pass

    def create(self, table: str, extra: str = None):
        self._statement = 'CREATE TABLE IF NOT EXISTS {0} ({1});'.format(
            table,
            extra)

        self._commit(False)

    def drop(self, table):
        self._statement = 'DROP TABLE {0};'.format(table)

        self._commit(False)

    def select(self, topic: str):
        self._topic = topic

    def insert(self, key: str, value: str):
        self._statement = 'INSERT INTO {0} ({1}) VALUES {2};'.format(
            self._topic,
            ','.join(key),
            value)

        self._commit(False)

    def get(self, key: str, value: str):
        self._statement = 'SELECT {0} FROM {1} WHERE {2} = "{3}";'.format(
            '*',
            self._topic,
            key,
            value)

        return self._commit(True)

    def get_all(self):
        self._statement = 'SELECT {0} FROM {1};'.format(
            '*',
            self._topic)

        return self._commit(True)

    def update(self, key: str, value: str, new: str):
        self._statement = 'UPDATE {0} SET {2} = "{1}" WHERE {2} = "{3}";'.format(
            self._topic,
            new,
            key,
            value)

        self._commit(False)

    def delete(self, key: str, value: str):
        self._statement = 'DELETE FROM {0} WHERE {1} = "{2}";'.format(
            self._topic,
            key,
            value)

        self._commit(False)
