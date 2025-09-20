import os.path
import sqlite3

class Database:
    def __init__(self, name):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.fullpath = os.path.join(self.path, name)
        self._conn = sqlite3.connect(self.fullpath)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()       

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql):
        self.cursor.execute(sql)

    def delete(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def insert(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def update(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        names = [description[0] for description in self.cursor.description]
        return [names,self.cursor.fetchall()]

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()