import sqlite3
connection = sqlite3.connect('database.db')


with open('schemaclubfavorites.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

#cur.execute("DROP TABLE users")
'''
cur.execute("INSERT INTO users_courses (, password, name, prenom, club) VALUES (?, ?, ?, ?, ?)",
            ('test@test.fr', 'test123', 'test', 'pretest','marcqtriathlon')
            )
'''

connection.commit()
connection.close()