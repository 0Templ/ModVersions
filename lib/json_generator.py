import json
import os


def write_data(loader, mod, mod_version, links):
    loader = loader.lower()
    os.makedirs(loader, exist_ok=True)
    if os.path.exists(f"{loader}/{mod}.json"):
        with open(f"{loader}/{mod}.json", "r") as file:
            data = json.load(file)
    else:
        data = {}
    data["homepage"] = f"https://www.curseforge.com/minecraft/mc-mods/{mod}"
    if "promos" not in data:
        data["promos"] = mod_version
    else:
        data["promos"].update(mod_version)
    for link in links:
        data[link] = {links[link][0] : str("Download and view changelog: " + links[link][1])}
    with open(f"{loader}/{mod}.json", "w") as file:
        json.dump(data, file, indent=4)
