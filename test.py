from selenium import webdriver
from selenium.webdriver.firefox.options import Options

#options = Options()
#options.headless = True

driver = webdriver.Firefox()

driver.get("https://www.idealista.es")