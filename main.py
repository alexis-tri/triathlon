import mysql.connector
from mysql.connector import Error

from scrap import scrap_events
from DatabaseMgmt import create_db_connection, execute_list_query, read_query, db
from secrets import pwalexis

insertDB = '''
    INSERT INTO `courses4` (name, place, date, distance) 
    VALUES (%s, %s, %s, %s)
'''

read_courses_table = """
SELECT id, name
FROM courses4;
"""

connection = create_db_connection("localhost", "alexistri", pwalexis, db) # Connect to the Database

if __name__ == "__main__":
    res = scrap_events()
    execute_list_query(connection, insertDB, res)
    