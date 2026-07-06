from threading import Thread
from bs4 import BeautifulSoup
import requests
import json
import chompjs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import os
from PIL import Image

options = Options()
options.page_load_strategy = "eager"
options.add_argument("--headless=new")
driver = webdriver.Firefox(options=options)

# get this json from huijiwiki which provides mappings between cn_name and char_id, plus a list of all char_ids
driver.get("https://res1999.huijiwiki.com/index.php?title=Data:Char/map.json&action=edit")
text = BeautifulSoup(driver.find_element(By.ID, "wpTextbox1").get_attribute("innerHTML"), features="html.parser").get_text() # type: ignore
id_map = json.loads(text)
cn_name_to_id = id_map["name"]

# get a list of released characters
driver.get("https://res1999.huijiwiki.com/wiki/%E8%A7%92%E8%89%B2%E5%88%97%E8%A1%A8")
released_chars = driver.find_elements(By.CLASS_NAME, "character-list-block")    
released_chars = [char for char in released_chars if char.get_attribute("data-isonline") == "1"]            # filter out unreleased characters
released_chars = [char.find_element(By.TAG_NAME, "a").get_attribute("title") for char in released_chars]    # map elements to names of characters
released_chars = [cn_name_to_id[char] for char in released_chars]                                           # map names to ids
driver.quit()

# get the html of uttu merui
res = requests.get("https://uttu.merui.net/profiles/")
text = res.text

# the data is stored in a big object written into the index.html file. this method of isolating the object is specific to the file (7/4/26)
start = text.find("const profiles")
text = text[start:]
start = text.find("[")
text = text[start:]

stack = 0
for idx, char in enumerate(text):
    if char == "]" and stack <= 0:
        text = text[:idx + 1]
        break 
    elif char == "[":
        stack += 1
    elif char == "]":
        stack -= 1

# parse the JS object into JSON
profiles_list: list[dict] = chompjs.parse_js_object(text)

data = {}
for profile in profiles_list:
    # skip if this character is unreleased
    if profile["ID"] not in released_chars:
        continue

    # parse the name field to get a url-ready string
    profile["Name"] = str(profile["Name"])
    name = profile["Name"]
    name = "_".join(part.lower() for part in name.split(" "))
    name = BeautifulSoup(name, features="html.parser").get_text()

    # the "Other Name" field can be either a string or an array of strings. If it's an array, pick the first
    if type(profile["Other Name"]) is list:
        profile["Other Name"] = profile["Other Name"][0] # type: ignore

    # merge euphoria tags into the main tags field
    if "euphoria" in profile:
        for e in profile["euphoria"]:
            for tag in e["tags"]:
                if tag not in profile["Tags"]:
                    profile["Tags"].append(tag)
        del profile["euphoria"]

    # copy the profile data over but change the name of the keys for convenience
    data[name] = {}
    for key in profile:
        data[name][key.replace(" ", "_")] = profile[key]

# load manually-entered location data and merge with the other data
manual_json_path = "manual.json"
with open(manual_json_path, "r") as f:
    manual = json.load(f)
    for char in manual:
        data[char] = manual[char] | data[char]

# setup work pool
pool = [key for key in data.keys()]
num_threads = 4
threads = []

# define a work function for multithreading
def get_assets():
    if len(pool) == 0:
        return

    name = pool.pop()

    # get character images based on id
    assets_path = "frontend/src/assets/charicons"
    headicon_small = f"{assets_path}/{data[name]["ID"]}01_headicon_small.webp"
    with open(f"{assets_path}/{data[name]["ID"]}_temp.png", 'wb') as f:
        f.write(requests.get(f"https://raw.githubusercontent.com/myssal/Reverse-1999-CN-Asset/refs/heads/master/singlebg/headicon_small/{data[name]["ID"]}01.png").content)
    
    # convert the image to webp and save
    im = Image.open(f"{assets_path}/{data[name]["ID"]}_temp.png")
    im.save(headicon_small, "WEBP")
    data[name]["Icon_Small"] = f"https://raw.githubusercontent.com/Luominai/r1999dle/refs/heads/main/frontend/src/assets/{data[name]["ID"]}01_headicon_small.webp"
    os.remove(f"{assets_path}/{data[name]["ID"]}_temp.png")

    # get the merui profile page of the character
    url = f"https://uttu.merui.net/profiles/{name}"
    print(url)
    text = requests.get(url).text
    html = BeautifulSoup(text, features="html.parser")

    # first figure out which index is the default garment
    idx_of_default = html.find(attrs={"data-voice-garment-name" : "default_"})["data-garment-index"] # type: ignore

    # then find the voicelines corresponding to the default garment
    voicelines = html.find(attrs={"data-garment-index": idx_of_default, "class": lambda classes: "voice-garment-panel" in classes}) # type: ignore
    voicelines = voicelines.find_all(name="div", attrs={"data-voice-line-index": True}) # type: ignore
    data[name]["Voicelines"] = {}
    for row in voicelines:
        voiceline_name = row.find(name="span").get_text() # type: ignore
        transcription = row.find(attrs={"data-en" : True}).get_text("\n") # type: ignore
        path = f'https://voice.merui.net/en/{row.find(attrs={"data-audio-path" : True})["data-audio-path"]}.ogg' # type: ignore

        # replace whitespace with underscores for convenience
        voiceline_name = voiceline_name.replace(" ", "_")
        voiceline_name = voiceline_name.replace(":", "")
        voiceline_name = voiceline_name.replace("-", "")
        data[name]["Voicelines"][voiceline_name] = {
            "Transcription": transcription,
            "Path": path
        }

    get_assets()    

# setup and start multithreading
for i in range(num_threads):
    t = Thread(target=get_assets)
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

# # write to file
# with open("data.json", "w") as f:
#     json.dump(data, f, indent=4)

# write to file
with open("frontend/src/assets/data.json", "w") as f:
    json.dump(data, f, indent=4)