from selenium import webdriver

web_idealista = "https://www.idealista.com/buscar/alquiler-viviendas/"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
    */*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "no-cache",
    "dnt": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Wildfire U20 5G) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36"
}

cookie = {
    "datadome": "BuCriLq.fGP_8NDSNCAFXR4oBF-0rxDzn6gIxy_wobKtDZ4XgOV_NAA4k~qQbY.KIq6HKUZ11PxMHCBXdXQ1JG7GxA0OdLpniYbvMV8TjKw_74ri3ly9MEx3ETG_tmc"}

default = {"city": "Murcia", "speed": 0, "limit": 2}

web_fotocasa = "https://www.fotocasa.es/es/"

WINDOW_SIZE = "1920,1080"


chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument(headers["User-Agent"])
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
#chrome_options.experimental_options(prefs["profile.managed_default_content_settings.images"])
