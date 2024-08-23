import os
import sqlite3
from scrap import scrap_events

def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

insertDB = '''
    INSERT INTO `courses4` (name, place, date, distance) 
    VALUES (%s, %s, %s, %s)
'''

read_courses_table = """
SELECT id, name
FROM courses4;
"""

if __name__ == "__main__":
    res = scrap_events()
    for re in res:
        title = res[0]
        place = res[1]
        date = res[2]
        distance = res[3]
        conn = get_db_connection()
        conn.execute('INSERT INTO courses (title, place, date, distance) VALUES (?, ?, ?, ?)',
                         (title, place, date, distance))
        conn.commit()
        conn.close()