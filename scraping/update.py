import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from scraping.utils import get_lazy_loaded_img

r1999_wiki = "https://reverse1999.fandom.com/wiki/Crew_Members"
options = Options()
options.page_load_strategy = "eager"

def update_overview_data(output="data/pages.json"):
    """ 
        Args:
            output: Where to write the data to
        
        Update overview data (Rarity, Afflatus, etc.) and also update the list of character wiki pages (ex: "https://reverse1999.fandom.com/wiki/6")

        This should be run every time a new character is released so the rest of the scraping program knows where to look for data
    """
    print("opening driver")
    driver = webdriver.Firefox(options=options)

    print("fetching website")
    driver.get(r1999_wiki)
    table_body = driver.find_element(By.TAG_NAME, "tbody")
    rows = table_body.find_elements(By.TAG_NAME, "tr")

    print("parsing rows")
    overview_data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        try:
            [_, image_cell, name_cell, rarity_cell, afflatus_cell, damage_cell, tags_cell, birthday_cell, age_cell] = cells
        except ValueError:
            return
        
        # get the character's overview data
        image = get_lazy_loaded_img(image_cell.find_element(By.TAG_NAME, "img"), "src")
        name = name_cell.find_element(By.TAG_NAME, "a").text
        page = str(name_cell.find_element(By.TAG_NAME, "a").get_attribute("href"))
        rarity = int(rarity_cell.text)
        afflatus = afflatus_cell.find_element(By.TAG_NAME, "a").text
        damage = damage_cell.text
        tags = tags_cell.text.split("\n")
        birthday = birthday_cell.text
        age = age_cell.text
        overview_data.append({
            "image": image,
            "name": name,
            "page": page,
            "rarity": rarity,
            "afflatus": afflatus,
            "damage": damage,
            "tags": tags,
            "birthday": birthday,
            "age": age,
        })

    print("writing data")
    with open(output, "w") as file:
        json.dump(output, file, indent=3)

    print("closing driver")
    driver.quit()


def update_cover_data(force_update = False, path_to_overviews = "data/data.json", path_to_cover_data = "data/profile.json"):
    """ 
        Args:
            force_update: Whether to re-fetch data for characters that already have all their cover data fields filled in
        
        Update all cover data (Medium, Fragrance, etc.)

        By default this will not update characters who already have all their fields filled in. If you want to force update all characters,
        change the force_update param
    """
    pages = []
    with open(path_to_overviews, "r") as file:
        overview_data = json.load(file)
        pages = [overview["page"] for overview in overview_data]

    cover_data = {}
    with open(path_to_cover_data, "r") as file:
        cover_data = json.load(file)

    def is_complete(data: dict):
        keys = ["image", "name", "rarity", "afflatus", "damage", "tags", "birthday", "age"]
        for key in keys:
            if not key in data:
                return False
            
    for name, cover in cover_data.items():
        if is_complete(cover) and f"https://reverse1999.fandom.com/wiki/{name}" in pages:
            pages.remove(f"https://reverse1999.fandom.com/wiki/{name}")
    story_pages = [page + "/Story" for page in pages]

    
    