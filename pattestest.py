import requests
import urllib3
import datetime
import locale
import re
import unicodedata
import concurrent.futures
from bs4 import BeautifulSoup

month_mapping = {
    "janvier": "01",
    "février": "02",
    "mars": "03",
    "avril": "04",
    "mai": "05",
    "juin": "06",
    "juillet": "07",
    "août": "08",
    "septembre": "09",
    "octobre": "10",
    "novembre": "11",
    "décembre": "12"
}


locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

'''
#url = "https://nord-pas-de-calais.1000pattes.guide/events/liste/"
url = "https://nord-pas-de-calais.1000pattes.guide/events/liste/page/3"
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.content, "html.parser")
events = soup.find_all(class_="tribe-events-calendar-list__event-details")
'''
def scraping(url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    events = soup.find_all(class_="tribe-events-calendar-list__event-details")
    return events
'''
def parse_place(text):
    city = text.split(",")[0].split("(")[0].strip()
    tmp = list(city)
    tmp[0] = tmp[0].upper()
    city = "".join(tmp)
    return city'''

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
    title = page.find(class_="tribe-events-calendar-list__event-title-link").text.strip().split("–")[0]
    tmp = "Inconnu"
    try:
        place = page.find(class_="tribe-events-calendar-list__event-title-link").text.strip().split("–")[1].strip()       
    except IndexError:
        place = tmp
    if place == "Inconnu":
        try:
            place = page.find(class_="tribe-events-calendar-list__event-venue-address").text.strip()
        except AttributeError:
            place = tmp   
    #place = parse_place(place)
    date = page.find(class_="tribe-event-date-start").text.strip().split("@")[0].strip()
    dateparts = date.split()
    month = dateparts[0]
    month = month_mapping[month]
    day = int(dateparts[1])
    year = 2024
    datefinal = (year, month, day)
    date = str(datefinal)
    #print (datefinal)
    #print (date)
    date = datetime.datetime.strptime(date, "(%Y, '%m', %d)")
    #date = datetime.datetime.strptime(datetime.date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
    try:
        distance = get_distance(page.find(class_="tribe-events-calendar-list__event-description").text)
    except ValueError:
        distance = tmp
    return title, place, date, distance

'''
res = []
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = []
    for event in events:
        futures.append(executor.submit(get_data, event))
    for future in concurrent.futures.as_completed(futures):
        title, place, date, distance = future.result()
        res.append([title, place, date, distance])


for item in res:
    print(item)'''