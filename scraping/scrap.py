import datetime
import concurrent.futures

from scraping.pattes import scrap_pattes_page, PattesEvent

# Extract and parse data from the extracted event
def get_data(page):
    event = PattesEvent(page)
    title = event.get_title()
    place = event.get_place()
    date = event.get_date()
    distance = event.get_distance()
    return title, place, date, distance

# Extract events data from the scraped HTML
def parse_events(events):
    res = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for event in events:
            futures.append(executor.submit(get_data, event))      
        for future in concurrent.futures.as_completed(futures):
            title, place, date, distance = future.result()
            res.append([title, place, date, distance])
    res.sort(key=lambda x: x[2])
    return res

# Extract each event separately from the website
def scrap_events():
    res = []
    actual_date = datetime.datetime.today()
    wanted_date = datetime.datetime.today() + datetime.timedelta(weeks=8)
    counter = 1
    while wanted_date > actual_date:
        url = f"https://nord-pas-de-calais.1000pattes.guide/events/liste/page/{counter}"
        events = scrap_pattes_page(url)
        res += parse_events(events)
        actual_date = res[-1][2]
        counter += 1
    return res

courses = scrap_events()
for course in courses:
    print(course)