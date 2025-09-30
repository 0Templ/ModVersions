import json
import os

from lib import cf_scraper
from lib import json_generator

def main():
    if os.path.exists('mods.json'):
        with open('mods.json', 'r') as file:
            loaders = json.load(file)
        mods = list({mod for mods in loaders.values() for mod in mods})
        scrapped = cf_scraper.get_mods_data(mods)
        generate_data(loaders, mods, scrapped)

    else:
        print("mods.json was not found")

def generate_data(loaders, mods, mods_data):
    for mod in mods:
        if mod not in mods_data or mods_data[mod] is None:
            continue
        files = mods_data[mod]['files']
        raws_all = cf_scraper.get_raws(files)
        for loader in loaders:
            if mod not in loaders[loader]: continue
            raws = [raw for raw in raws_all  if raw.loader and raw.loader == loader.lower()]
            print(f"{len(raws)}", loader)
            baked = {}
            for release_type in ["release", "alpha", "beta"]:
                latest = cf_scraper.get_latest_raws(raws, release_type)
                baked[release_type] = [i.build() for i in latest]
            baked["latest"] = [i.build() for i in cf_scraper.get_latest_raws(raws, "release", "alpha", "beta")]
            if loader == "Fabric":
                json_generator.generate_fabric_format(loader, mod, baked["release"], baked["alpha"], baked["beta"])
            else:
                json_generator.generate_forge_legacy_format(loader, mod, baked["latest"], baked["release"])
                json_generator.generate_forge_v1_format(loader, mod, baked)

if __name__ == "__main__":
    main()