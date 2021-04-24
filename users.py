import sqlite3
from sqlite3 import Error

con = sqlite3.connect('mydatabase.db')

cursorObj = con.cursor()


def sql_connection():
    try:
        con = sqlite3.connect('mydatabase.db')
        return con
    except Error:
        print(Error)


def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE employees(id integer PRIMARY KEY, name text, salary real, department text, position text, hireDate text)")
    con.commit()


con = sql_connection()
sql_table(con)


class User(object):
    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

    @staticmethod
    def find_by_username(username):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = 'SELECT * FROM users WHERE username=?'
        row = cur.execute(query, (username,)).fetchone()

        con.close()

        user = User(*row) if row else None
        return user

    @staticmethod
    def find_by_id(_id):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = 'SELECT * FROM users WHERE id=?'
        row = cur.execute(query, (_id,)).fetchone()

        con.close()

        user = User(*row) if row else None
        return user
