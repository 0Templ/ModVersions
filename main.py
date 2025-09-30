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
        all_versions = cf_scraper.get_versions(files)
        for loader in loaders:
            if mod not in loaders[loader]: continue
            versions = [version for version in all_versions if version.loader and loader.lower() in version.loader]
            typed_versions = {}
            for release_type in ["release", "alpha", "beta"]:
                typed_versions[release_type] = [i for i in cf_scraper.get_latest(versions, release_type)]
            typed_versions["latest"] = [i for i in cf_scraper.get_latest(versions, "release", "alpha", "beta")]
            if loader == "Fabric":
                json_generator.generate_fabric_format(loader, mod, typed_versions["release"], typed_versions["alpha"], typed_versions["beta"])
            else:
                json_generator.generate_forge_legacy_format(loader, mod, typed_versions["latest"], typed_versions["release"])
                json_generator.generate_forge_v1_format(loader, mod, typed_versions)

if __name__ == "__main__":
    main()