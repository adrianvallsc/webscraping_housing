import sys
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from functions import paste_web, parse_list
from variables import headers, web_fotocasa, cookie
from bs4 import BeautifulSoup
import requests
import re
import time
import pandas as pd
from tqdm import tqdm
from datetime import datetime


class FotocasaSelenium:
    def gen_website(self, ciudad: str, sub: str, inmueble: bool) -> str:
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
            site = web_fotocasa + f'/inmueble/{sub}/'
        else:

            site = paste_web(web_fotocasa, ciudad)
            if sub != "":
                site = site + sub

        return site

    def get_web(self, ciudad: str = "", sub="", inmueble=False):

        website = gen_website(ciudad, sub, inmueble)

        try:
            page = requests.get(website, headers=headers, cookies=cookie)

        except requests.exceptions.RequestException:
            sys.exit("Connection error")

        extract = check_web(page)

        return extract

    def check_web(self, page):

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
