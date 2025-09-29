import json
import os

from lib import cf_scraper
from lib import json_generator

def main():
    mod_data = cf_scraper.load_all_mod_data()
    if os.path.exists('mods.json'):
        with open('mods.json', 'r') as file:
            loaders = json.load(file)
        for loader in loaders:
            mods = loaders[loader]
            generate_data(loader, mods, mod_data)


    else:
        print("mods.json was not found")

def generate_data(loader, mods, mod_data):
    for mod in mods:
        files = mod_data[mod]['files']
        raws = cf_scraper.get_raws(files)
        stable_raws = cf_scraper.get_latest_raws(raws, "release")
        stable = [i.build() for i in stable_raws]
        if loader == "Fabric":
            alpha_raws = cf_scraper.get_latest_raws(raws, "alpha")
            beta_raws = cf_scraper.get_latest_raws(raws, "beta")
            alpha = [i.build() for i in alpha_raws]
            beta = [i.build() for i in beta_raws]
            json_generator.generate_fabric_format(loader, mod, stable, alpha, beta)
        else:
            latest_raws = cf_scraper.get_latest_raws(raws, "release", "alpha", "beta")
            latest = [i.build() for i in latest_raws]
            json_generator.generate_forge_format(loader, mod, stable, latest)


if __name__ == "__main__":
    main()