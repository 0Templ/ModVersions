import requests
from lib.mod_data import VersionData
from packaging.version import Version

def get_mods_data(mods):
    ret = {}
    for mod in mods:
        ret[mod] = load_mod_data(mod)
    return ret

def load_mod_data(mod):
    url = f"https://api.cfwidget.com/minecraft/mc-mods/{mod}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(f"fetched {url}")
        return response.json()
    except requests.RequestException as e:
        print(f"Could not fetch {url}")
        return None

def get_latest(versions, *releases):
    latest = {}
    for version in versions:
        if version.type in releases:
            keys = [(loader, version.type, version.mc_version) for loader in version.loader]
            for key in keys:
                mod_version = Version(version.mc_version)
                if key not in latest or Version(latest[key].mod_version) < mod_version:
                    latest[key] = version
    return list(latest.values())

def get_versions(files):
    ret = []
    if files is None:
        return ret
    for file in files:
        raw = VersionData(
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