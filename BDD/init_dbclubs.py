import sqlite3
connection = sqlite3.connect('database.db')


with open('./BDD/schemaclubs.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO clubs (clubname, adresse) VALUES (?, ?)",
            ('marcqtri', 'Marcq-En-Baroeul')
            )

cur.execute("INSERT INTO clubs (clubname, adresse) VALUES (?, ?)",
            ('senzu', 'saint-crépin-ibouvillers')
            )

connection.commit()
connection.close()

