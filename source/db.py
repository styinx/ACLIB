import sqlite3
from sqlite3 import Error


class DB:
    def __init__(self, path):
        self.conn = None
        self.cursor = None
        self.path = path

        try:
            self.conn = sqlite3.connect(path)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(e)
        finally:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def create_table(self, table):
        statement = "CREATE TABLE " + table.name + "("

        for field in table.fields:
            statement += field["name"] + " " + field["type"] + " " + field["extra"]

        self.cursor.execute(statement[:-1] + ")")
        self.conn.commit()

    def drop_table(self, table):
        self.cursor.execute("DROP TABLE " + table.name)
        self.conn.commit()

    def insert_entry(self, table, field_names, field_values):
        if not isinstance(field_names, str) and len(field_names) != len(field_values):
            raise Exception("Unequal argument value lengths")

        ph = '?'
        if not isinstance(field_names, str):
            ph = ','.join('?' * len(field_names))
        self.cursor.execute("INSERT INTO " + table.name + " (" + ','.join(field_names) + ") VALUES (" + ph + ")", field_values)


class Table:
    def __init__(self, name):
        self.name = name
        self.fields = []

    def field(self, field_name, field_type, field_extra=""):
        self.fields.append({"name": field_name, "type": field_type, "extra": field_extra})
        return self

    def fields(self):
        return [item["name"] for item in self.fields]
