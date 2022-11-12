import sys

from functions import paste_web, search_text
from variables import headers, web_idealista
from bs4 import BeautifulSoup
import requests
import re
import time
import pandas as pd


def get_web(ciudad: str = "", sub="", inmueble=False):

    if inmueble:
        website = web_idealista + f'/inmueble/{sub}/'
    else:
        website = paste_web(web_idealista, ciudad)
        if sub != "":
            website = website + sub
    try:
        page = requests.get(website, headers=headers)

    except requests.exceptions.RequestException:
        sys.exit("Connection error")

    soup = BeautifulSoup(page.content, "html.parser")

    if check_unknown(soup):
        sys.exit("Error: Wrong city")

    return soup


def check_unknown(soup):
    results = soup.find("div", id="main").find("div", class_="zero-results")
    return results is not None

def check_busted():
    pass

def get_number_pages(soup, n=30):
    texto = soup.find("div", {"class": "listing-top"}).find("h1").text
    total_n = int(re.findall("\d+", texto.replace(".", ""))[0])

    return round(total_n / n)


def parse_header(text, dix: dict):
    for k in text:
        item = k.text
        dix = search_text(item, r'hab.$', dix, "rooms")
        if re.search(r'm²$', item):
            dix["surface"] = item
        elif re.search(r"(^Planta|Bajo)", item):
            dix["floor"] = item

    return dix

def solve_captcha():
    pass

def get_info_main(sub_part, dix):
    dix["id"] = sub_part.parent["data-adid"]
    dix["title"] = sub_part.find("a", {"class": "item-link"}).text
    dix["price"] = sub_part.find("span", {"class": "item-price"}).text
    texto = sub_part.find_all("span", {"class": "item-detail"})
    dix = parse_header(texto, dix)

    return dix


city = "murcia"

soup = get_web(city)
pages = get_number_pages(soup)

# print(soup.find_all("section", class_="items-container"))

anuncios = soup.find_all("div", {"class": "item-info-container"})

lista = list()

for anuncio in anuncios:
    d = dict()
    d = get_info_main(anuncio, d)
    soup2 = get_web(sub=d['id'], inmueble=True)
    d["description"] = soup2.find("div", {"class": "comment"}).find("p").text

    t0 = time.time()

    details = soup2.find("div", {"class": "details-property_features"}).find_all("li")
    for item in details:
        v = item.text
        if re.search("bañ", v):
            d["bathroom"] = v
        elif re.search("[cC]alefac", v):
            d["heating"] = v
        elif re.search("garaje", v):
            d["garage"] = v
        elif re.search("muebl", v):
            d["furniture"] = v
    d["location"] = ";".join([item.text for item in soup2.find_all("li", class_="header-map-list")])
    d["seller"] = soup2.find("div", class_="professional-name").find("div", class_="name").text

    time.sleep(10*(time.time()-t0))



    #except AttributeError:
    #    d["location"] = None


    lista.append(d)

pd.DataFrame(lista).to_csv(f"../dataset/{city}.csv")
# for i in range(1, pages+1):
#    get_web(city, f"pagina-{i}.htm")


