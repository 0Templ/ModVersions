import json
import os
import requests
from lib.mod_data import RawVersionData


def load_all_mod_data():
    mods = get_mods()
    all_mod_data = {}
    for mod in mods:
        all_mod_data[mod] = load_mod_data(mod)
    return all_mod_data


def load_mod_data(mod):
    url = f"https://api.cfwidget.com/minecraft/mc-mods/{mod}"
    response = requests.get(url)
    print("response: ", response.status_code)
    if response.status_code != 200:
        print(f"Could not fetch {url} ({response.status_code}: {response.reason})")
        return None
    return response.json()


def get_latest_raws(raws, *releases):
    ret = []
    seen = []
    for raw in raws:
        if raw.type in releases and raw.loader:
            m = (raw.loader, raw.version)
            if m not in seen:
                seen.append(m)
                ret.append(raw)
    return ret

def get_raws(files):
    ret = []
    if files is None:
        return ret
    for file in files:
        raw = RawVersionData(
            file['id'],
            file['url'],
            file['display'],
            file['name'],
            file['type'],
            file['filesize'],
            file['versions'],
            file['downloads'],
            file['uploaded_at']
        )
        ret.append(raw)
    return ret


def get_loaders():
    ret = []
    if os.path.exists('mods.json'):
        with open('mods.json', 'r') as file:
            loaders = json.load(file)
        for loader in loaders:
            ret.append(loader)
    else:
        print("mods.json was not found")
    return ret

def get_mods():
    ret = []
    if os.path.exists('mods.json'):
        with open('mods.json', 'r') as file:
            loaders = json.load(file)
        for loader in loaders:
            for mod in loaders[loader]:
                if mod not in ret:
                    ret.append(mod)
    else:
        print("mods.json was not found")

    return ret

