import json
import os

from packaging.version import InvalidVersion, Version


def generate_v2_format(mod, source_versions_by_loader):
    path = "v2"
    output_path = f"{path}/{mod}.json"
    os.makedirs(path, exist_ok=True)

    data = {"versions": {}}

    for source, versions_by_loader in source_versions_by_loader.items():
        for loader, versions in versions_by_loader.items():
            loader = loader.lower()
            for version in versions:
                for mc_version in version.mc_versions:
                    sources = data.setdefault("versions", {}) \
                        .setdefault(mc_version, {}) \
                        .setdefault(loader, {}) \
                        .setdefault("sources", {})
                    current = sources.get(source)
                    if current is None or is_newer_version(version.mod_version, current["version"]):
                        sources[source] = {
                            "version": version.mod_version,
                            "url": version.url
                        }

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def is_newer_version(candidate, current):
    candidate_version = parse_version(candidate)
    current_version = parse_version(current)
    if candidate_version is None or current_version is None:
        return False
    return current_version < candidate_version


def parse_version(value):
    try:
        return Version(value)
    except InvalidVersion:
        return None


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
