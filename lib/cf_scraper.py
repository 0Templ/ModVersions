import requests
from mod_data import RawVersionData

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

def get_latest_raws(raws, *releases):
    ret = []
    seen = []
    for raw in raws:
        if raw.type in releases:
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