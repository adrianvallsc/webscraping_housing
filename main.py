from source.idealista import main_idealista
from source.variables import default
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="Select the city in Spain")
    args = parser.parse_args()
    main_idealista(args.city, default["speed"], default["limit"])



