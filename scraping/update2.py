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
import time

options = Options()
options.page_load_strategy = "eager"
options.add_argument("--headless=new")
driver = webdriver.Firefox(options=options)

# the data is stored in a big object written into the index.html file. this method of isolating the object is specific to the file (7/4/26)
def get_object(text, keystring):
    start = text.find(keystring)
    text = text[start:]
    start = min(text.find("["), text.find("{"))
    text = text[start:]

    stack = 0
    for idx, char in enumerate(text):
        if (char == "]" or char == "}") and stack <= 0:
            text = text[:idx + 1]
            break 
        elif char == "[" or char == "{":
            stack += 1
        elif char == "]" or char == "}":
            stack -= 1

    return chompjs.parse_js_object(text)

def get_uttu():
    # get the html of uttu merui
    res = requests.get("https://uttu.merui.net/profiles/")
    text = res.text
    return text

def get_existing_data(path="frontend/src/assets/data.json"):
    # load existing data
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}
    
def convert_key(key):
    key = BeautifulSoup(key, features="html.parser").get_text() # strip html tags
    key = "_".join(part.lower() for part in key.split(" ")) # convert to snakecase

def convert_all_keys(d: dict):
    new_dict = {}
    for key, val in d.items():
        new_key = convert_key(key)
        if type(val) is dict:
            new_dict[new_key] = convert_all_keys(val)
        else:
            new_dict[new_key] = val
    return new_dict

def cleanup_profile(profile):
    profile = convert_all_keys(profile)
    name = convert_key(str(profile["name"]))

    # some characters' names may be read as a number, so perform a typecast to be safe
    profile["name"] = str(profile["name"])

    # the "Other Name" field can be either a string or an array of strings. If it's an array, pick the first
    if type(profile["other_name"]) is list:
        profile["other_name"] = str(profile["other_name"][0]) # type: ignore
        profile["other_name"] = BeautifulSoup(profile["other_name"], features="html.parser").get_text()

    # merge euphoria tags into the main tags field
    if "euphoria" in profile:
        for e in profile["euphoria"]:
            for tag in e["tags"]:
                if tag not in profile["tags"]:
                    profile["tags"].append(tag)
        del profile["euphoria"]

    # remove role tags because they're too common to be interesting hints
    roles: list[str] = get_object(text, "const role")
    for tag in roles:
        if tag in profile["Tags"]:
            profile["Tags"].remove(tag)

    # rename tags
    profile["archetypes"] = profile.pop("tags")
    return name, profile

# find the JS objects in text and parse them into JSON
text = get_uttu()
profiles: list[dict] = get_object(text, "const profiles")
version_order: list[str] = get_object(text, "const categoryOptions")["characteristics"]["Version"]
hidden_characters: list[int] = get_object(text, "const hiddenCharacters")
data = {name : data for [name, data] in [cleanup_profile(profile) for profile in profiles]}

# load manually-entered location data and merge with the other data
manual_json_path = "scraping/resources/manual.json"
with open(manual_json_path, "r") as f:
    manual = json.load(f)
    for char in manual:
        data[char] = manual[char] | data[char]

# setup work pool
pool = [key for key in data.keys()]
num_threads = 4
threads = []    

def get_icon(id, name):
    # get this character's icon if we're missing it
    png_path = f"scraping/resources/charicons/{id}01.png"
    webp_path = f"frontend/src/assets/charicons/{id}01_headicon_small.webp"
    try:
        im = Image.open(png_path)
        im.save(webp_path, "WEBP")
    except:
        png_url = f"https://raw.githubusercontent.com/myssal/Reverse-1999-CN-Asset/refs/heads/master/singlebg/headicon_small/{id}01.png"
        try:
            content = requests.get(png_url).content
            with open(png_path, "wb") as f:
                f.write(content)
            im = Image.open(png_path)
            im.save(webp_path, "WEBP")
            print(png_url)
        except:
            print(f"an error occured while fetching icon for {name}. skipping.")

def get_voicelines(id, name):
    required = ["First_Encounter", "Suitcase_Climate", "To_the_Future", "Idle", "Greetings", "Morning", 
                "Bond_Morning", "Night", "Bond_Night", "Hat_and_Hair", "Sleeves_and_Hands", "Clothing_and_Torso", 
                "Hobby", "Praise", "Intimacy", "Chitchat_I", "Chitchat_II", "Monologue", "Insight"]
    

# define a work function for multithreading
def get_assets():
    if len(pool) == 0:
        return

    name = pool.pop()
    get_icon(data[name]["ID"], name)

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

# write to file
with open("frontend/src/assets/data.json", "w") as f:
    json.dump(data, f, indent=4)

with open("frontend/src/assets/versions.json", "w") as f:
    json.dump(version_order, f, indent=4)

# with open("frontend/src/imports.jsx", "w") as f:
#     for char, charData in data.items():
#         f.write(f"import {char}_icon_small from ./assets/charicons/{charData["ID"]}01_headicon_small.webp\n")