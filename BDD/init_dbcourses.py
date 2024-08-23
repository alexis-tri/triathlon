import sqlite3
connection = sqlite3.connect('database.db')


with open('./BDD/schemacourses.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
'''
cur.execute("DROP TABLE courses")


cur.execute("INSERT INTO courses (name, place, date, distance) VALUES (?, ?, ?, ?)",
            ('Urban Trail de Crespin', 'Crespin', '2024, 9, 21, 0, 0', '10')
            )

cur.execute("INSERT INTO courses (name, place, date, distance) VALUES (?, ?, ?, ?)",
            ('Belle Dys Trail', 'Bailleul', '2024, 9, 22, 0, 0', 'S, M, L')
            )
'''
connection.commit()
connection.close()
