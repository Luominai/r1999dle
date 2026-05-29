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

# print("parsing character pages")
# for page in character_pages:
#     driver = webdriver.Firefox(options=options)
#     driver.get(page)
#     cover = driver.find_elements(By.CLASS_NAME, "wds-tab__content")[4]
#     dimensions = cover.find_element(By.CSS_SELECTOR, "[data-source=proportions]").find_element(By.TAG_NAME, "div").text
#     medium = cover.find_element(By.CSS_SELECTOR, "[data-source=medium]").find_element(By.TAG_NAME, "div").text
#     fragrance = cover.find_element(By.CSS_SELECTOR, "[data-source=fragrance]").find_element(By.TAG_NAME, "div").text
#     inspiration = cover.find_element(By.CSS_SELECTOR, "[data-source=inspo]").find_element(By.TAG_NAME, "div").text
#     signature_cell = cover.find_element(By.CSS_SELECTOR, "[data-source=signature]").find_element(By.TAG_NAME, "a")
#     signature = get_lazy_loaded_img(signature_cell, "href")

#     # sleeping
#     print("sleeping")
#     time.sleep(15)
#     driver.get(page + "/Story")
#     character_name = page.split("/")[-1]
#     item_1 = get_lazy_loaded_img(driver.find_element(By.CSS_SELECTOR, f"[data-image-name={character_name}_Item_1.png]"), "src")
#     item_2 = get_lazy_loaded_img(driver.find_element(By.CSS_SELECTOR, f"[data-image-name={character_name}_Item_2.png]"), "src")
#     item_3 = get_lazy_loaded_img(driver.find_element(By.CSS_SELECTOR, f"[data-image-name={character_name}_Item_3.png]"), "src")

#     data.append({
#         "dimensions": dimensions, 
#         "medium": medium, 
#         "fragrance": fragrance, 
#         "inspiration": inspiration, 
#         "signature": signature,
#         "items": [item_1, item_2, item_3]
#     })
#     driver.quit()

# print("writing data")
# with open("profile.json", "w") as file:
#     json.dump(data, file, indent=3)
