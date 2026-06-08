import json
from urllib.parse import unquote

path_to_standard_data = "data/data.json"
path_to_cover_data = "data/profile.json"
path_to_output = "data/merged.json"

standard_data = None
cover_data = None
merged_data = {}

with open(path_to_standard_data, "r") as data:
    standard_data = json.load(data)

with open(path_to_cover_data, "r") as data:
    cover_data = json.load(data)

for character in standard_data:
    name = character["name"]
    name = "_".join(name.split(" "))
    cover = None
    try:
        cover = cover_data[name]
    except KeyError:
        try: 
            name = name.encode("utf-8")
            cover = cover_data[name]
        except KeyError:
            print(f"failed to get cover data using key {name}")
            continue
    merged = character | cover
    merged_data[name] = merged

with open(path_to_output, "w") as file:
    json.dump(merged_data, file, indent=3)