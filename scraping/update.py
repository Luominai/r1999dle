import json
from typing import List
from overview_scraper import OverviewScraper
from cover_scraper import CoverScraper
from story_scraper import StoryScraper
from scraper import Scraper

overviews_path = "overviews.json"
covers_path = "covers.json"
stories_path = "stories.json"
output_path = "merged.json"
complete_path = "complete.json"
incomplete_path = "incomplete.json"

overview_scraper = OverviewScraper(overviews_path)
cover_scraper = CoverScraper(covers_path, overviews_path)
story_scraper = StoryScraper(stories_path, overviews_path)

# overview_scraper.scrape(force_update=False)
cover_scraper.scrape(force_update=True)
# story_scraper.scrape(force_update=False)

overviews = {}
with open(overviews_path, "r") as file: overviews = json.load(file)

covers = {}
with open(covers_path, "r") as file: covers = json.load(file)

stories = {}
with open(stories_path, "r") as file: stories = json.load(file)

fields = ["name", "image", "page", "lookup_name", "rarity", "afflatus", "damage", 
          "tags", "birthday", "age", "dimensions", "medium", "fragrance", "inspiration", 
          "signature", "release", "items"
          ]

data = {}
complete = {}
incomplete = {}

for key in overviews:
    data[key] = overviews[key] | covers[key] | stories[key]

    is_incomplete = False

    for field in fields:
        if not field in data[key]:
            data[key][field] = None
            is_incomplete = True

    if is_incomplete:
        incomplete[key] = data[key]
    else:
        complete[key] = data[key]

try:
    with open(output_path, "w") as file:
        json.dump(data, file, indent=4)
except FileNotFoundError:
    with open(output_path, "x") as file:
        json.dump(data, file, indent=4)

try:
    with open(complete_path, "w") as file:
        json.dump(complete, file, indent=4)
except FileNotFoundError:
    with open(complete_path, "x") as file:
        json.dump(complete, file, indent=4)

try:
    with open(incomplete_path, "w") as file:
        json.dump(incomplete, file, indent=4)
except FileNotFoundError:
    with open(incomplete_path, "x") as file:
        json.dump(incomplete, file, indent=4)