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
    # parse the name field to get a url-ready string
    name = str(profile["Name"])
    name = "_".join(part.lower() for part in name.split(" "))
    name = BeautifulSoup(name, features="html.parser").get_text()
    data[name] = profile

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
    data[name]["Voicelines"] = {}
    for row in voicelines:
        voiceline_name = row.find(name="span").get_text() # type: ignore
        transcription = row.find(attrs={"data-en" : True}).get_text("\n") # type: ignore
        path = f'https://voice.merui.net/en/{row.find(attrs={"data-audio-path" : True})["data-audio-path"]}.ogg' # type: ignore

        data[name]["Voicelines"][voiceline_name] = {
            "Transcription": transcription,
            "Path": path
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