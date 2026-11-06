import src.scrapper as sc
import src.visualizer as vs

from os import getenv

api_key = getenv("STEAM_API_KEY")

if __name__ == '__main__':
    sc.start(api_key)
    vs.start()