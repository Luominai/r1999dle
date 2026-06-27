from selenium.webdriver.firefox.options import Options
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

options = Options()
options.page_load_strategy = "eager"
options.add_argument("--headless=new")
driver = webdriver.Firefox(options=options)

# get this json from huijiwiki which provides mappings between cn_name and char_id, plus a list of all char_ids
driver.get("https://res1999.huijiwiki.com/index.php?title=Data:Char/map.json&action=edit")
text = BeautifulSoup(driver.find_element(By.ID, "wpTextbox1").get_attribute("innerHTML"), features="html.parser").get_text() # type: ignore
id_map = json.loads(text)
cn_name_to_id = id_map["name"]
id_to_cn_name = id_map["id"]
id_list = id_map["list"]

# use the list of char_ids to parse through merui for en_names
driver.get("https://uttu.merui.net/profiles/")
# we'll get a modal asking us if we want to see cn exclusive content. we say yes
driver.find_element(By.ID, "cnModalYes").click()
id_to_en_names = {}
def parse_merui_profile(driver, id):
    card = driver.find_element(By.ID, f"card-{id}")
    [real_name_span, display_name_span] = card.find_elements(By.TAG_NAME, "span")
    id_to_en_names[id] = {
        "name": display_name_span.get_attribute("innerText"),
        "realName": real_name_span.get_attribute("innerText")
    }
for id in id_map["list"]:
    try:
        parse_merui_profile(driver, id)
    except NoSuchElementException:
        print(f"no profile found for char_id: {id}")
    except StaleElementReferenceException:
        parse_merui_profile(driver, id)

# combine mappings to create a mapping from cn_name to en_name
cn_to_en_names = {}
for cn_name, id in cn_name_to_id.items():
    try:
        cn_to_en_names[cn_name] = id_to_en_names[id]
    except KeyError:
        pass

# now parse the huijiwiki character list
driver.get("https://res1999.huijiwiki.com/wiki/%E8%A7%92%E8%89%B2%E5%88%97%E8%A1%A8")
characters = driver.find_elements(By.CLASS_NAME, "character-list-block")
afflatuses = [None, "Mineral", "Star", "Plant", "Beast", "Spirit", "Intellect"]
damageTypes = [None, "Reality", "Mental"]

data = {}
for character in characters:
    is_online = character.get_attribute("data-isonline")

    # skip characters that are not released
    if is_online is not None and is_online == "0":
        continue

    name = cn_to_en_names[character.find_element(By.TAG_NAME, "a").get_attribute("title")]["name"]
    data[name] = {
        "release": character.get_attribute("data-gameversion"),
        "rarity": int(character.get_attribute("data-rare")) + 1, # type: ignore
        "afflatus": afflatuses[int(character.get_attribute("data-career"))], # type: ignore
        "damageType": damageTypes[int(character.get_attribute("data-dmgtype"))], # type: ignore
        "name": cn_to_en_names[character.find_element(By.TAG_NAME, "a").get_attribute("title")]["name"],
        "realName": cn_to_en_names[character.find_element(By.TAG_NAME, "a").get_attribute("title")]["realName"]
    }
    
driver.quit()

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
