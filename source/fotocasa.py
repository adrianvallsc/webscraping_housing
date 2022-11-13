import sys
from functions import paste_web, parse_list
from variables import headers, web_idealista, cookie
from bs4 import BeautifulSoup
import requests
import re
import time
import pandas as pd
from tqdm import tqdm
from datetime import datetime




def gen_website(
