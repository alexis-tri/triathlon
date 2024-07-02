import requests

from bs4 import BeautifulSoup

url = "https://nord-pas-de-calais.1000pattes.guide/events/s"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# Extraction du texte de la balise a
h1_text = soup.h1.string

# Extraction des noms et des prix des produits dans la liste
events = soup.find_all("div", class_="tribe-events-calendar-month__day-cell tribe-events-calendar-month__day-cell--desktop tribe-common-a11y-hidden")
timetest = soup.find_all("time")
timetestbis = soup.find_all("time", class_="tribe-events-calendar-month__day-date-daynum")
events_list = []
for event in events:
    time = events.time.string
    race = events.h3.string
    events_list.append ((time,race))

# Étape 2 : Affichage des informations extraites
print("Texte de la balise h1 :", timetestbis)