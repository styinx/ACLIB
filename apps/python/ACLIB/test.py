from source.storage.sqlite3 import SQLite3DB

try:
    db = SQLite3DB('asd.db')
    db.create('test', 'id INT PRIMARY KEY, name CHAR NOT NULL, pace INT NOT NULL')
    db.select('test')
    db.insert(['name', 'pace'], ('jens', 50))

    for i in db.get_all():
        print(i)

    db.update('name', 'jens', 'detlef')

    for i in db.get_all():
        print(i)

    db.drop('test')
except Exception as e:
    print(e)