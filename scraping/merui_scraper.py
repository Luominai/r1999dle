from threading import Thread
from bs4 import BeautifulSoup
import requests
import json
import chompjs

res = requests.get("https://uttu.merui.net/profiles/")
text = res.text

# the data is stored in a big object written into the index.html file. this method of isolating the object is specific to the file (6/26/26)
start = text.find("=[{")
end = len(text) - 1 - text[::-1].find(",]}")
profiles_str = text[start + 1:end]

# parse the JS object into JSON
profiles_list: list[dict] = chompjs.parse_js_object(profiles_str)

# convert the keys to camelcase
data = {}
for profile in profiles_list:
    char_data = {}
    for key, value in profile.items():
        parts = [part.lower() for part in key.split(" ")]
        for i in range(1, len(parts)):
            part = parts[i]
            parts[i] = part[0].upper() + part[1:]

        lower_key = "".join(parts)

        # the two characters named 6 and 37 get parsed as ints instead of strings. so we fix that here
        # lady by the lake has her name wrapped in <i> tags which we also fix here
        if lower_key == "name":
            char_data[lower_key] = BeautifulSoup(str(value), features="html.parser").get_text()
        else:
            char_data[lower_key] = value
        
    # Keys in snake case
    data["_".join(part.lower() for part in char_data["name"].split(" "))] = char_data

# setup work pool
pool = [key for key in data.keys()]
num_threads = 4
threads = []

# define a work function for multithreading
def parse_voicelines():
    if len(pool) == 0:
        return

    name = pool.pop()
    url = f"https://uttu.merui.net/profiles/{name}"
    print(url)
    text = requests.get(url).text
    html = BeautifulSoup(text, features="html.parser")

    # first figure out which index is the default garment
    idx_of_default = html.find(attrs={"data-voice-garment-name" : "default_"})["data-garment-index"] # type: ignore

    # then find the voicelines corresponding to the default garment
    voicelines = html.find(attrs={"data-garment-index": idx_of_default, "class": lambda classes: "voice-garment-panel" in classes}) # type: ignore
    voicelines = voicelines.find_all(name="div", attrs={"data-voice-line-index": True}) # type: ignore
    data[name]["voicelines"] = {}
    for row in voicelines:
        voiceline_name = row.find(name="span").get_text() # type: ignore
        transcription = row.find(attrs={"data-en" : True}).get_text("\n") # type: ignore
        path = f'https://voice.merui.net/en/{row.find(attrs={"data-audio-path" : True})["data-audio-path"]}.ogg' # type: ignore

        data[name]["voicelines"][voiceline_name] = {
            "transcription": transcription,
            "path": path
        }

    parse_voicelines()    

# setup and start multithreading
for i in range(num_threads):
    t = Thread(target=parse_voicelines)
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

# write to file
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)