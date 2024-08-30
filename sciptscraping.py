import os
import datetime
import sqlite3
from scraping.scrap import scrap_events

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
        name = str(re[0])
        place = str(re[1])
        date = str(re[2])
        distance = str(re[3])
        conn = get_db_connection()
        conn.execute('INSERT INTO courses (name, place, date, distance) VALUES (?, ?, ?, ?)',
                         (name, place, date, distance))
        conn.commit()
        conn.close()