import sqlite3
connection = sqlite3.connect('database.db')


with open('./BDD/schemausers.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

#cur.execute("DROP TABLE users")

cur.execute("INSERT INTO users (email, password, name, prenom, club) VALUES (?, ?, ?, ?, ?)",
            ('test@test.fr', 'test123', 'test', 'pretest','marcqtriathlon')
            )


connection.commit()
connection.close()
