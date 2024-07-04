import mysql.connector
from mysql.connector import Error
import requests
import sqlite3
import urllib3
import datetime
import locale
import re
import unicodedata
import random
import concurrent.futures
from pattes import scraping, get_data
from DatabaseMgmt import *

insertDB = '''
    INSERT INTO `courses3` (name, place, date, distance) 
    VALUES (%s, %s, %s, %s)
    '''
    
if __name__ == "__main__":
    #url_imp = input("Enter the name of the input file (e.g., input.txt): ")
    url_imp="https://nord-pas-de-calais.1000pattes.guide/events/liste/"
    events = scraping(url_imp)
    res = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for event in events:
            futures.append(executor.submit(get_data, event))
        for future in concurrent.futures.as_completed(futures):
            title, place, date, distance = future.result()
            res.append([title, place, date, distance])


    connection = create_db_connection("localhost", "alexistri", pwalexis, db) # Connect to the Database

    execute_list_query(connection, insertDB, res)
    '''
    today = datetime.date.today()
    wanted_date = datetime.date.today() + datetime.timedelta(weeks=8)
    actual_date = datetime.datetime.strptime(datetime.date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
    res = []
    counter = 1
    while wanted_date > actual_date:
        url_imp = f"https://nord-pas-de-calais.1000pattes.guide/events/liste/page/{counter}"
        events = scraping(url_imp)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for event in events:
                futures.append(executor.submit(get_data, event))
            for future in concurrent.futures.as_completed(futures):
                title, place, date, distance = future.result()
                res.append([title, place, date, distance])
        counter += 1
        actual_date = res[-1][2]



'''