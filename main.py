
import requests
from source.variables import headers
from source.functions import parse_list
from bs4 import BeautifulSoup
from pprint import pprint

ciudad = "murcia"

city = "madrid"

website = "https://www.idealista.com/"

with open("error_data.html") as f:
    file = f.read()

extract = BeautifulSoup(file, "html.parser")

print(extract.find("script", src="https://ct.captcha-delivery.com/c.js"))
print(extract.prettify())




