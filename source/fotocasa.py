
# Selenium tiene que ser instalado previamente para que funcione la clase

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd



class FotocasaSelenium:
    # Se definen aquí los parámetros para la búsqueda: Url, ciudades en las que buscar y cantidad de páginas a scrapear
    n_pages = 2
    city = "Madrid"
    url = "https://www.fotocasa.es/es/"
    # Estas preferencias evitan que se cargen imágenes durante el proceso
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    var = chrome_options.experimental_options["prefs"]
    prices_list = []
    rooms_list = []
    bathrooms_list = []
    surfaces_list = []
    floors_list = []
    city_list = []

    def __init__(self, n_pages=n_pages, url=url, chrome_options=chrome_options,
                 city = city):
        self.n_pages = n_pages
        self.url = url
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                       chrome_options=chrome_options)
        self.city = city
        self.open_driver()
        time.sleep(2)

    def __del__(self):
        self.close_driver()

    def open_driver(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        time.sleep(1)

    def close_driver(self):
        self.driver.quit()

    # Aceptamos las cookies para poder acceder a la página
    def accept_cookies(self):
        cookies = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.sui-MoleculeModal-dialog '
                                                                      'button.sui-AtomButton[data-testid=TcfAccept]')
        cookies[0].click()
        time.sleep(2)
        return

    # Accedemos al motor de búsqueda e introducimos la ciudad de interés
    def search_rent(self, city: str):
        self.open_driver()
        time.sleep(2)
        rent = self.driver.find_element("xpath",'/html/body/div[1]/div[1]/main/section/div[2]/div/div/div/div/'
                                                  'div[1]/div/div[2]/label')
        rent.click()
        time.sleep(1)
        search = self.driver.find_element("xpath", '/html/body/div[1]/div[1]/main/section/div[2]/div/div/div/'
                                                    'div/div[2]/div[2]/form/div/div/div/div/div/input')

        search.click()
        search.send_keys(city)
        time.sleep(2)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        self.scrap_pages()
        return

    def scrap_page(self):
        scroll_pause = 1
        screen_height = self.driver.execute_script("return window.screen.height")
        i = 1
        while True:
            # Hay que recorrer la página para poder scrapear los datos
            self.driver.execute_script(
                "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause)
            # Se actualiza el tamaño del scroll cada vez, ya que fuese una página de scroll infinito (reddit), 
            # el tamaño cambia según avanzamos
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")
            if screen_height * i > scroll_height:
                break
        time.sleep(2)

        # Buscamos los parámetros de interés
        prices = self.driver.find_elements(by=By.CSS_SELECTOR, value='span.re-CardPrice')
        for price in range(len(prices)):
            price_euros = prices[price].text.split(" ")
            self.prices_list.append(price_euros[0])
            self.city_list.append(self.city)

        rooms = self.driver.find_elements(by=By.CSS_SELECTOR, value='span.re-CardFeaturesWithIcons-feature-icon--rooms')
        for room in range(len(rooms)):
            room_n = rooms[room].text.split(" ")
            self.rooms_list.append(room_n[0])

        bathrooms = self.driver.find_elements(by=By.CSS_SELECTOR,
                                              value='span.re-CardFeaturesWithIcons-feature-icon--bathrooms')
        for bathroom in range(len(bathrooms)):
            bathroom_n = bathrooms[bathroom].text.split(" ")
            self.bathrooms_list.append(bathroom_n[0])

        surfaces = self.driver.find_elements(by=By.CSS_SELECTOR,
                                             value='span.re-CardFeaturesWithIcons-feature-icon--surface')
        for surface in range(len(surfaces)):
            surface_m2 = surfaces[surface].text.split(" ")
            self.surfaces_list.append(surface_m2[0])

        floors = self.driver.find_elements(by=By.CSS_SELECTOR,
                                           value='span.re-CardFeaturesWithIcons-feature-icon--floor')
        for floor in range(len(floors)):
            floor_n = floors[floor].text.split(" ")
            self.floors_list.append(floor_n[0])
    
    # Si se realiza la búsqueda en más de una página, se va cambiando el url
    def scrap_pages(self):
        self.scrap_page()
        time.sleep(3)
        if self.n_pages > 1:
            current_url = self.driver.current_url
            for page in range(2, self.n_pages + 1):
                new_url = current_url + "/" + str(page)
                self.driver.get(new_url)
                self.scrap_page()

    # Función a utilizar para ejecutar el web scraping completo            
    def scrap_cities(self):
        self.open_driver()
        time.sleep(2)
        self.accept_cookies()
        self.search_rent(self.city)
        self.create_dataset()

    # Generación del csv mediante Pandas      
    def create_dataset(self):
        df = pd.DataFrame(list(zip(self.city_list, self.prices_list, self.surfaces_list, self.rooms_list,
                                   self.bathrooms_list, self.floors_list)),
                          columns=['Ciudad', 'Precio', 'Superficie', 'Habitaciones', 'Lavabos', 'Planta'])
        df.to_csv(f"./dataset/{self.city}_fotocasa.csv")

