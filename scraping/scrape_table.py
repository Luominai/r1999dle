import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from scraping.utils import get_lazy_loaded_img, scroll_to

r1999_wiki = "https://reverse1999.fandom.com/wiki/Crew_Members"
options = Options()
options.page_load_strategy = "eager"

print("opening driver")
driver = webdriver.Firefox(options=options)
data = []

print("fetching website")
driver.get(r1999_wiki)
table_body = driver.find_element(By.TAG_NAME, "tbody")
rows = table_body.find_elements(By.TAG_NAME, "tr")

def parse_row(row: WebElement):
    scroll_to(driver, row)
    cells = row.find_elements(By.TAG_NAME, "td")
    try:
        [_, image_cell, name_cell, rarity_cell, afflatus_cell, damage_cell, tags_cell, birthday_cell, age_cell] = cells
    except ValueError:
        return

    image = get_lazy_loaded_img(image_cell.find_element(By.TAG_NAME, "img"), "src")
    name = name_cell.find_element(By.TAG_NAME, "a").text
    rarity = rarity_cell.text
    afflatus = afflatus_cell.find_element(By.TAG_NAME, "a").text
    damage = damage_cell.text
    tags = tags_cell.text.split("\n")
    birthday = birthday_cell.text
    age = age_cell.text
    data.append({
        "image": image,
        "name": name,
        "rarity": rarity,
        "afflatus": afflatus,
        "damage": damage,
        "tags": tags,
        "birthday": birthday,
        "age": age
    })

print("parsing rows")
for row in rows:
    parse_row(row)

print("writing data")
with open("data/data.json", "w") as file:
    json.dump(data, file, indent=3)

print("closing driver")
driver.quit()