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

    n_pages = 1
    url = "https://www.fotocasa.es/es/"
    fcpath = "webdriver/chromedriver.exe"

    def __init__(self, n_pages=n_pages, url=url, fcpath=fcpath):
        self.n_pages = n_pages
        self.url = url
        self.browser = webdriver.Chrome(fcpath)
        self.open_browser
        time.sleep(2)

    def __del__(self):
        self.close_browser

    def open_browser(self):
        self.browser.get(self.url)
        self.browser.maximize_window()
        time.sleep(1)

    def close_browser(self):
        self.browser.quit()

    def accept_cookies(self):
        cookies = self.browser.find_elements_by_xpath('.//*[@id="App"]/div[3]/div/div/div/footer/div/button[2]')
        cookies.click()
        time.sleep(2)
        return

    def search_rent(self, ciudad: str):
        rent = self.browser.find_elements_by_xpath('/html/body/div[1]/div[1]/main/section/div[2]/'
                                                   'div/div/div/div/div[1]/div/div[2]/label')
        rent.click()
        time.sleep(1)
        search = self.browser.find_elements_by_xpath('/html/body/div[1]/div[1]/main/section/div[2]/div/div/div/'
                                                     'div/div[2]/div[2]/form/div/div/div/div/div/input')
        search.send_keys(ciudad)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(1)
        return






    '''
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
            
    '''

