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
from pattestest import scraping, get_data
from secrets import pwalexis
from DatabaseMgmt import create_db_connection, execute_list_query, db


today = datetime.datetime.today()
print (today)
wanted_date = datetime.datetime.today() + datetime.timedelta(weeks=2)
print(wanted_date)
actual_date = datetime.datetime.strptime(datetime.date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
print(actual_date)
'''
res = []
counter = 1
while wanted_date > actual_date:
    url_imp = f"https://nord-pas-de-calais.1000pattes.guide/events/liste/page/{counter}"
    events = scraping(url_imp)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for event in events:
            futures.append(executor.submit(get_data, event))
            print(events)
        for future in concurrent.futures.as_completed(futures):
            title, place, date, distance = future.result()
            res.append([title, place, date, distance])
    counter += 1
    actual_date = res[-1][2]'''