import json
import os

from lib import cf_scraper
from lib import json_generator

def main():
    datas = cf_scraper.load_all_mod_data()
    if os.path.exists('mods.json'):
        with open('mods.json', 'r') as file:
            loaders = json.load(file)
        for loader in loaders:
            print(f"Generating {loader} data...")
            for mod in loaders[loader]:
                exact_versions = cf_scraper.get_versions_for(cf_scraper.get_versions_from_data(datas[mod]), loader, ["release"])
                latest_versions = cf_scraper.get_versions_for(cf_scraper.get_versions_from_data(datas[mod]), loader, ["release", "beta", "alpha"])
                recommended = {}
                latest = {}
                urls = {}
                for v in exact_versions:
                    recommended[v.mc_version + "-recommended"] = str(v.mod_version)
                    urls[v.mc_version] = (v.mod_version, v.url)
                for v in latest_versions:
                    latest[v.mc_version + "-latest"] = str(v.mod_version)
                json_generator.write_data(loader, mod, recommended, urls)
                json_generator.write_data(loader, mod, latest, {})
    else:
        print("mods.json was not found")


if __name__ == "__main__":
    main()