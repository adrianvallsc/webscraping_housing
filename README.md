# Webscraping Housing

This package performs a webscraping of spanish famous renting houses in major cities of Spain:

- Fotocasa (www.fotocasa.es)
- Idealista (www.idealista.com)

## Contents

- main.py: is the main script to execute, and calls the functions to obtain a dataset from a certain city in Spain
- source: contains the scripts and variables for the program
  - fotocasa.py: contains the script and functions to parse the information from the web www.fotocasa.es
  - idealista.py: contains the script and functions to parse the information from the web www.idealista.com
  - functions.py: contains general functions
  - variables.py: contains general variables
- dataset: it is a folder where every dataset will be stored with name of the city

## Before you use it

This program requires the installation of Google Chrome prior running it: https://www.google.com/intl/es/chrome/

## How to use it

1. Open a terminal and navigate to the folder where you will store your package
2. Download the package with the command `git clone https://github.com/adrianvallsc/webscraping_housing`
3. Open the folder in the terminal
4. If you don't have virtualenv installed execute `pip install virtualenv`
5. Execute the command `virtualenv venv` to create the virtual environment
6. Execute `source venv/bin/activate` to activate the virtual environment
7. Open the folder, and execute `pip install -r requirements.txt` to install the requirements 
8. Execute the following command `python main.py` followed by the city you want to search and the number of pages desired to obtain
   1. For example if you want to obtain the 3 first pages of the city of Santander you will execute `python main.py Santander 3`
   2. If you want to obtain the first 10 pages of the city of Barcelona, you will have to execute `python main.py Barcelona 10`
9. Obtain the dataset in the dataset folder. There you will obtain the datasets in .csv format, one with the name city_fotocasa.csv, which contains the flats obtained in fotocasa, and another named city_idealista.csv which contains the flats obtained in idealista.

