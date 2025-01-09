import json
import os
import re
import requests
from lib import mod_data

def load_mod_data(mod):
    url = f"https://api.cfwidget.com/minecraft/mc-mods/{mod}"
    response = requests.get(url)
    print("response: ", response.status_code)
    if response.status_code != 200:
        print(f"Could not fetch {url} ({response.status_code}: {response.reason})")
        return None
    return response.json()

def mod_version_from_file_name(filename, i):
    matches = list(re.finditer(r'-([^-]*)', filename))
    ret = matches[i].group()[1:]
    if ret.find(".jar") != -1:
        ret = ret[:-4]
    return ret

def get_versions_from_data(json_data):
    ret = []
    if json_data == None:
        return ret
    data = json_data['files']
    for file in data:
        vd = mod_data.FileData(
            file['id'],
            file['url'],
            file['display'],
            file['name'],
            file['type'],
            file['version'],
            file['filesize'],
            file['versions'],
            file['downloads'],
            file['uploaded_at']
        )
        ret.append(vd)
    return ret

def get_versions(data_list):
    ret = {}
    for data in data_list:
        ret[data] = get_versions_from_data(data_list)
    return ret

def get_versions_for(versions, loader, releases):
    ret = []
    seen = []
    for vdata in versions:
        if loader in vdata.versions and vdata.type in releases:
            for version in vdata.versions:
                if version not in seen and not re.search("[a-zA-Z]", version):
                    seen.append(version)
                    ret.append(mod_data.VersionData(version, mod_version_from_file_name(vdata.filename, 1), loader, vdata.url, vdata.type))
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


def load_all_mod_data():
    mods = get_mods()
    all_mod_data = {}
    for mod in mods:
        all_mod_data[mod] = load_mod_data(mod)
    return all_mod_data
