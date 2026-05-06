import requests
from lib.mod_data import VersionData
from packaging.version import Version, InvalidVersion

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
    except requests.RequestException:
        print(f"Could not fetch {url}")
        return None

def _parse_version(value):
    try:
        return Version(value)
    except InvalidVersion:
        return None

def get_latest(versions, *releases):
    latest = {}
    for version in versions:
        if version.type not in releases:
            continue
        new_mod_version = _parse_version(version.mod_version)
        for loader in version.loader:
            for mc_version in version.mc_versions:
                key = (loader, version.type, mc_version)
                current = latest.get(key)
                if current is None:
                    latest[key] = version
                    continue
                current_mod_version = _parse_version(current.mod_version)
                if new_mod_version is None or current_mod_version is None:
                    continue
                if current_mod_version < new_mod_version:
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
