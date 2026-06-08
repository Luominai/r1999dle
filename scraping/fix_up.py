import json
from urllib.parse import unquote

data = None
new_data = {}
with open("data/profile.json", "r") as file:
    data = json.load(file)

for key, value in data.items():
    try:
        new_items = []
        for item in value["items"]:
            new_items.append(item.split("/revision")[0])
        value["items"] = new_items
    except KeyError:
        print(f"no items for {key}")

    try:    
        value["signature"] = value["signature"].split(".png")[0] + ".png"
    except KeyError:
        print(f"no signature for {key}")

    new_data[unquote(key)] = value

with open("data/profile.json", "w") as file:
    json.dump(new_data, file, indent=3)

data = None
new_data = []
with open("data/data.json", "r") as file:
    data = json.load(file)

for character in data:
    character["rarity"] = int(character["rarity"])
    character["image"] = character["image"].split("/revision")[0]
    new_data.append(character)

with open("data/data.json", "w") as file:
    json.dump(data, file, indent=3)