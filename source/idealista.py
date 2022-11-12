import sys
from functions import paste_web, parse_list
from variables import headers, web_idealista
from bs4 import BeautifulSoup
import requests
import re
import time
import pandas as pd
from tqdm import tqdm


def gen_website(ciudad: str, sub: str, inmueble: bool) -> str:
    """
    This function generates a website for the idealista website

    :param ciudad: city to search
    :param sub: string to append to the website
    :param inmueble: determine if it is a certain advertise
    :return: string containing the website
    """

    # If it is a certain id
    if inmueble:
        # Then paste
        site = web_idealista + f'/inmueble/{sub}/'
    else:

        site = paste_web(web_idealista, ciudad)
        if sub != "":
            site = site + sub

    return site


def get_web(ciudad: str = "", sub="", inmueble=False):

    website = gen_website(ciudad, sub, inmueble)

    try:
        page = requests.get(website, headers=headers)


    except requests.exceptions.RequestException:
        sys.exit("Connection error")

    extract = check_web(page)

    return extract


def check_web(page):

    extract = BeautifulSoup(page.content, "html.parser")

    # Checking if the web obtained is correct
    check_busted(extract)
    check_unknown(extract)


    return extract


def check_unknown(extract):

    if extract.find("div", id="main").find("div", class_="zero-results"):
        sys.exit("Error: Wrong city")



def check_busted(extract):

    if extract.find("script", src="https://ct.captcha-delivery.com/c.js"):
        sys.exit("Error: Too many requests, idealista blocked us")
    else:
        pass


def get_number_pages(extract, n=30):
    texto = extract.find("div", {"class": "listing-top"}).find("h1").text
    total_n = int(re.findall("\d+", texto.replace(".", ""))[0])

    return round(total_n / n)


def get_info_main(sub_part, dix):
    dix["id"] = sub_part.parent["data-adid"]
    dix["title"] = sub_part.find("a", {"class": "item-link"}).text
    dix["price"] = sub_part.find("span", {"class": "item-price"}).text
    texto = sub_part.find_all("span", {"class": "item-detail"})
    dix = parse_list(texto, dix, rooms='hab.$', surface= 'm²$', floor= "(^Planta|Bajo)")

    return dix


def get_details_properties(extract, dix):
    details = extract.find("div", {"class": "details-property_features"})

    if details:
        details = details.find_all("li")
        dix = parse_list(details, dix, bathroom="bañ", heating="[cC]alefac",
                         garage="garaje", furniture="muebl")
    else:
        dix.update({'bathrooom': None, 'heating': None, 'garage': None, 'furniture': None})

    return dix


def get_location(extract):
    location = extract.find_all("li", class_="header-map-list")

    if location:
        value = ";".join([item.text for item in location])
    else:
        value = None

    return value

def get_seller(extract, dix):
    prof = extract.find("div", class_="professional-name")

    if prof:
        dix["seller"] = prof.find("div", class_="name").text
        dix["seller_name"] = prof.find("span").text

    else:
        dix.update({"seller":None, "seller_name":None})


def get_info_link(dix):
    extract = get_web(sub=dix['id'], inmueble=True)
    descrip = extract.find("div", {"class": "comment"})
    dix["description"] = descrip.find("p").text if descrip else None
    dix = get_details_properties(extract, dix)
    dix["location"] = get_location(extract)
    dix = get_seller(extract, dix)

    return dix

city ="madrid"

soup = get_web(city)
pages = get_number_pages(soup)

anuncios = soup.find_all("div", {"class": "item-info-container"})

lista = list()

for anuncio in tqdm(anuncios):
    d = dict()
    d = get_info_main(anuncio, d)
    t0 = time.time()
    d = get_info_link(d)
    time.sleep(2*(time.time()-t0))
    lista.append(d)

pd.DataFrame(lista).to_csv(f"../dataset/{city}.csv")
# for i in range(1, pages+1):
#    get_web(city, f"pagina-{i}.htm")
