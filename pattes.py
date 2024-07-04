import requests
import urllib3
import datetime
import locale
import re
import unicodedata
import concurrent.futures
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#url = "https://nord-pas-de-calais.1000pattes.guide/events/liste/"
#response = requests.get(url, verify=False)
#soup = BeautifulSoup(response.content, "html.parser")
#events = soup.find_all(class_="tribe-events-calendar-list__event-details")

def scraping(url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    events = soup.find_all(class_="tribe-events-calendar-list__event-details")
    return events

def parse_place(text):
    city = text.split(",")[0].split("(")[0].strip()
    tmp = list(city)
    tmp[0] = tmp[0].upper()
    city = "".join(tmp)
    return city

def get_distance(text):
    pattern = r"\d+(?:\.\d+)?\s*km"
    regex = re.compile(pattern)
    distance = "".join([regex.findall(text)][0]).split(" ")
    distance = [elem.replace("km", "") for elem in distance]
    distance = [elem for elem in distance if elem]
    distance = [str(int(elem)) for elem in distance]
    distance = ";".join(distance)
    return distance

def get_data(page):
    res = []
    title = page.find(class_="tribe-events-calendar-list__event-title-link").text.strip().split("–")[0]
    tmp = page.find(class_="tribe-events-calendar-list__event-title-link").text.strip().split("–")[1].strip()
    try:
        place = page.find(class_="tribe-events-calendar-list__event-venue-address").text.strip()
    except AttributeError:
        place = tmp
    place = parse_place(place)
    date = page.select_one("time")["datetime"]
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    distance = get_distance(page.find(class_="tribe-events-calendar-list__event-description").text)
    return title, place, date, distance

#res = []
#with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #futures = []
    #for event in events:
        #futures.append(executor.submit(get_data, event))
    #for future in concurrent.futures.as_completed(futures):
        #res.append(future.result())

#for item in res:
    #print(item)