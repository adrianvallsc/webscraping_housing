from source.idealista import main_idealista
from source.variables import default, chrome_options, web_fotocasa
from source.fotocasa import FotocasaSelenium
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="Select the city in Spain")
    parser.add_argument("pages", help="Select the number of pages to parse")
    args = parser.parse_args()

    main_idealista(args.city, default["speed"], int(args.pages))
    prueba = FotocasaSelenium(n_pages=int(args.pages), url=web_fotocasa,
                              city=args.city,
                              chrome_options=chrome_options)
    prueba.scrap_cities()



