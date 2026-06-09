import json
from typing import List
from overview_scraper import OverviewScraper
from cover_scraper import CoverScraper
from story_scraper import StoryScraper
from scraper import Scraper

overview_scraper = OverviewScraper("overviews.json")
cover_scraper = CoverScraper("covers.json", "overviews.json")
story_scraper = StoryScraper("stories.json", "overviews.json")

# overview_scraper.scrape(force_update=False)
cover_scraper.scrape()
story_scraper.scrape()

overviews = {}
with open("overviews.json", "r") as file: overviews = json.load(file)

covers = {}
with open("covers.json", "r") as file: covers = json.load(file)

stories = {}
with open("stories.json", "r") as file: stories = json.load(file)

try:
    with open("merged.json", "w") as file:
        data = {}
        for key in overviews:
            data[key] = overviews[key] | covers[key] | stories[key]
        json.dump(data, file, indent=4)
except FileNotFoundError:
    with open("merged.json", "x") as file:
        data = {}
        for key in overviews:
            data[key] = overviews[key] | covers[key] | stories[key]
        json.dump(data, file, indent=4)