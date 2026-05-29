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

print("opening driver")
driver = webdriver.Firefox(options=options)
character_pages: list[str] = []
data = []

print("fetching website")
driver.get(r1999_wiki)
table_body = driver.find_element(By.TAG_NAME, "tbody")
rows = table_body.find_elements(By.TAG_NAME, "tr")

def parse_row(row: WebElement):
    cells = row.find_elements(By.TAG_NAME, "td")
    try:
        [_, image_cell, name_cell, rarity_cell, afflatus_cell, damage_cell, tags_cell, birthday_cell, age_cell] = cells
    except ValueError:
        return

    href = name_cell.find_element(By.TAG_NAME, "a").get_attribute("href")
    character_pages.append(str(href))

print("parsing rows")
for row in rows:
    parse_row(row)

driver.quit()

print("writing data")
with open("pages.json", "w") as file:
    json.dump(character_pages, file, indent=3)
