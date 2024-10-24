import sqlite3
connection = sqlite3.connect('database.db')


with open('./BDD/schemausers.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0;")

connection.commit()
connection.close()
