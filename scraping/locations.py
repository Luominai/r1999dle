import json

manual = "scraping/resources/manual.json"
data: dict = {}

with open(manual) as f:
    data: dict = json.load(f)

locations = []
for char, bg in data.items():
    for location in bg["Locations"]:
        if location not in locations:
            locations.append(location)

major_locations = []
assignments = {}

print(len(locations))

for location in locations:
    print(f"Assign {location} to a major location")

    majors = [f"{str(i+1)}.{major_locations[i]}" for i in range(len(major_locations))]
    majors = " ".join(majors)
    print(f"Majors: {majors}")
    val = input()

    try:
        num = int(val)
        if num <= len(major_locations):
            assignments[location] = major_locations[num - 1]
        else:
            print("invalid number")
    except:
        found = False
        for loc in major_locations:
            if "".join(val.lower().split(" ")) == "".join(loc.lower().split(" ")):
                assignments[location] = loc
                found = True
                break
        if not found:
            print(f"Assigning {location} to new major location: {val}")
            major_locations.append(val)
            assignments[location] = val