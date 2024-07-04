import mysql.connector
from mysql.connector import Error
#import pandas as pd
from secrets import pwalexis

def create_server_connection(host_name, user_name, user_password): #Fonction permettant de se connecter à MySQL Server
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#connection = create_server_connection("localhost", "alexistri", pwalexis)

def create_database(connection, query): #Fonction permettant de créer une DB
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

create_database_query = "CREATE DATABASE courses"
db = "courses"
#create_database(connection, create_database_query)

def create_db_connection(host_name, user_name, user_password, db_name): #Fonction pour se connecter à une DB spécifique
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query): #Fonction pour exécuter les SQL queries
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query): #Fonction permettant de lire dans les tableaux
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def execute_list_query(connection, sql, val): #Fonction permettant d'ajouter une list dans une DB
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

create_courses_table = """
CREATE TABLE courses3 (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  name VARCHAR(40) NOT NULL,
  place VARCHAR(40) NOT NULL,
  date DATE,
  distance VARCHAR(40)
  );
 """


#insertDB = '''
#    INSERT INTO courses (course_id, name, place, date, distance_1, distance_2, distance_3, distance_4) 
#    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#    '''

val = [
    (7, 'Hank', 'Dodson', 'ENG', None, '1991-12-23', 11111, '+491772345678'), 
    (8, 'Sue', 'Perkins', 'MAN', 'ENG', '1976-02-02', 22222, '+491443456432')
]

#connectionS = create_server_connection("localhost", "alexistri", pwalexis) # Connect to the Server
connectionD = create_db_connection("localhost", "alexistri", pwalexis, db) # Connect to the Database

#execute_query(connectionS, create_database_query) #Création d'une DB
execute_query(connectionD, create_courses_table) #Création d'une table
#execute_list_query(connection, sql, val) #Ajout d"une liste dans la DB