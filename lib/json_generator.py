import json
import os


def generate_fabric_format(loader, mod, stable, alpha, beta):
    loader = loader.lower()
    os.makedirs(loader, exist_ok=True)
    data = {}
    for release_type, versions in [("release", stable), ("alpha", alpha), ("beta", beta)]:
        for version in versions:
            for mc_version in version.mc_versions:
                data.setdefault(mc_version, {})[release_type] = {
                    "url": version.url,
                    "version": version.mod_version
                }
    with open(f"{loader}/{mod}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def generate_forge_v1_format(loader, mod, versions):
    format_version = "v1"
    loader = loader.lower()
    path = f"{loader}/{mod}/{format_version}"
    os.makedirs(path, exist_ok=True)
    per_mc = {}
    for version in versions["latest"]:
        for mc_version in version.mc_versions:
            per_mc.setdefault(mc_version, version)
    for mc_version, version in per_mc.items():
        data = {
            "homepage": f"{version.url}",
            "promos": {f"{mc_version}-recommended": version.mod_version}
        }
        with open(f"{path}/{mc_version}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


def generate_forge_legacy_format(loader, mod, latest, stable):
    loader = loader.lower()
    os.makedirs(loader, exist_ok=True)
    data = {
        "homepage": f"https://www.curseforge.com/minecraft/mc-mods/{mod}",
        "promos": {}
    }

    for version in latest:
        for mc_version in version.mc_versions:
            data["promos"][f"{mc_version}-latest"] = version.mod_version
    for version in stable:
        for mc_version in version.mc_versions:
            data["promos"][f"{mc_version}-recommended"] = version.mod_version

    with open(f"{loader}/{mod}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
