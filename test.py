import sqlite3

con = sqlite3.connect('data.db')
cur = con.cursor()

create_users_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
cur.execute(create_users_table)

create_user = 'INSERT INTO users VALUES (?, ?, ?)'
user = (None, 'elya_cherry', '1234')
cur.execute(create_user, user)

users = [
        ('dima', 'slave'),
        ('timofey', 'rab')
    ]
cur.executemany(create_user, users)

create_items_table = 'CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price integer)'
cur.execute(create_items_table)

create_item = 'INSERT INTO items(id, name, price) VALUES (?, ?, ?)'
item = (None, 'chair', '1221')
cur.execute(create_item, item)

items = [
        ('bread', 50),
        ('cheese', 200)
    ]
cur.executemany(create_item, items)

con.commit()
con.close()
