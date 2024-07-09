import requests
import urllib3
import datetime
import locale
import re

from bs4 import BeautifulSoup

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

# Scrap a given URL and return each event found
def scrap_pattes_page(url):
    verify = True
    try:
        requests.get(url)
    except requests.exceptions.SSLError:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        verify = False
    finally:
        response = requests.get(url, verify=verify)
    soup = BeautifulSoup(response.content, "html.parser")
    events = soup.find_all(class_="tribe-events-calendar-list__event-details")
    return events

class PattesEvent:

    # Constructor
    def __init__(self, event):
        self.event = event

    # Get the title of the event
    def get_title(self):
        title = self.event.find(class_="tribe-events-calendar-list__event-title-link").text.strip()
        title = title.split("–")[0].strip()
        title = title.split("(")[0].strip()
        return title
    
    # Correctly get and parse the place of the event
    def get_place(self):
        try:
            place = self.event.find(class_="tribe-events-calendar-list__event-venue-address").text.strip()
        except AttributeError:
            place = None
        if not place:
            place = self.event.find(class_="tribe-events-calendar-list__event-title-link").text.strip()
            try:
                place = place.split("–")[1].strip()
                place = place.split("(")[0].strip()
            except IndexError:
                place = None
        else:
            place = place.split(",")[0].strip()
            place = place.split("(")[0].strip()
        return place
    
    # Get date of the event and convert it to the right format
    def get_date(self):
        date = datetime.datetime.strptime(self.event.select_one("time")["datetime"], "%Y-%m-%d")
        return date
    
    # Get each distance of the event heuristicly from the description
    def get_distance(self):
        regex = re.compile(r"\d+(?:\.\d+)?\s*km")
        distance = self.event.find(class_="tribe-events-calendar-list__event-description").text
        distance = "".join([regex.findall(distance)][0]).split(" ")
        distance = [elem.replace("km", "") for elem in distance]
        distance = [elem for elem in distance if elem]
        distance = [int("".join(char for char in elem if char.isdigit())) for elem in distance]
        distance = sorted(set(distance))
        distance = ";".join([str(elem) for elem in distance])
        return distance