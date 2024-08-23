import requests
import urllib3
import datetime
import locale
import concurrent.futures

from bs4 import BeautifulSoup

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.opentri.fr/calendrier/?_region=hauts-de-france"
response = requests.get(url, verify=False)

soup = BeautifulSoup(response.content, "html.parser")
links = soup.find_all(class_="elementor-element-dfb4d3c")

def get_data(page):
    title = page.find(class_="elementor-heading-title").text.strip()
    place = page.find(class_="elementor-element-d249d7b").text.strip()[2:].strip()
    date = page.find(class_="elementor-element-0a018fa").text.strip()[2:].strip()
    date = datetime.datetime.strptime(date, "%d %B %Y")
    url = page.find(class_="elementor-widget-container").find_all("a", href=True)[0]["href"]
    distance = check_page(url)
    return [title, place, date, distance]

def check_page(url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    distance = soup.find(class_="elementor-element-f758f4b").text.strip().split(", ")
    return distance

#res = []
#with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #futures = []
    #for link in links:
        #futures.append(executor.submit(get_data, link))
    #for future in concurrent.futures.as_completed(futures):
        #res.append(future.result())

#print(res)
