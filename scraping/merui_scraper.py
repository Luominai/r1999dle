import requests
import json
import chompjs

res = requests.get("https://uttu.merui.net/profiles/")
text = res.text
start = text.find("=[{")
end = len(text) - 1 - text[::-1].find(",]}")
profiles_str = text[start + 1:end]
profiles_list: list[dict] = chompjs.parse_js_object(profiles_str)

data = []
for profile in profiles_list:
    char_data = {}
    for key, value in profile.items():
        parts = [part.lower() for part in key.split(" ")]
        for i in range(1, len(parts)):
            part = parts[i]
            parts[i] = part[0].upper() + part[1:]
            
        lower_key = "".join(parts)
        char_data[lower_key] = value
    data.append(char_data)
        
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)