import re

import requests

from lib.mod_data import AVAILABLE_LOADERS


API_URL = "https://api.modrinth.com/v2"
HEADERS = {"User-Agent": "ModVersions/1.0"}


class ModrinthVersionData:

    def __init__(self, mod, file):
        self.id = file["id"]
        self.url = f"https://modrinth.com/mod/{mod}/version/{self.id}"
        self.type = file["version_type"]
        self.mod_version = file["version_number"]
        self.mc_versions = file["game_versions"]
        self.loader = self.extract_loaders(file["loaders"])

    def extract_loaders(self, loaders):
        ret = []
        for loader in loaders:
            loader = loader.lower().strip()
            if loader in AVAILABLE_LOADERS and loader not in ret:
                ret.append(loader)
        return ret


def get_mods_data(mods):
    ret = {}
    for mod in mods:
        ret[mod] = load_mod_data(mod)
    return ret


def load_mod_data(mod):
    project = find_project(mod)
    if project is None:
        print(f"Could not find Modrinth project for {mod}")
        return None

    slug = project["slug"]
    url = f"{API_URL}/project/{slug}/version"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        print(f"fetched {url}")
        return {
            "slug": slug,
            "files": response.json()
        }
    except requests.RequestException:
        print(f"Could not fetch {url}")
        return None


def find_project(mod):
    direct_url = f"{API_URL}/project/{mod}"
    try:
        response = requests.get(direct_url, headers=HEADERS, timeout=10)
        if response.ok:
            return response.json()
    except requests.RequestException:
        pass

    search_url = f"{API_URL}/search"
    try:
        response = requests.get(
            search_url,
            params={
                "query": mod.replace("-", " "),
                "facets": '[[\"project_type:mod\"]]',
                "limit": 10
            },
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        hits = response.json().get("hits", [])
        if not hits:
            return None
        return find_best_match(mod, hits)
    except requests.RequestException:
        print(f"Could not search Modrinth project for {mod}")
        return None


def find_best_match(mod, hits):
    normalized_mod = normalize(mod)
    for hit in hits:
        if normalize(hit["slug"]) == normalized_mod:
            return hit
    for hit in hits:
        if normalize(hit["title"]) == normalized_mod:
            return hit
    return hits[0]


def normalize(value):
    return re.sub(r"[^a-z0-9]", "", value.lower())


def get_versions(data):
    ret = []
    if data is None or data.get("files") is None:
        return ret
    for file in data["files"]:
        ret.append(ModrinthVersionData(data["slug"], file))
    return ret
