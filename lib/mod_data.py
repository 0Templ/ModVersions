import re

AVAILABLE_LOADERS = ["fabric", "neoforge", "forge"]

class RawVersionData:

    def __init__(self, id, url, display, name, type, filesize, versions, downloads, uploaded_at):
        self.id = id
        self.url = url
        self.display = display
        self.name = name
        self.type = type
        self.filesize = filesize
        self.versions = versions
        self.downloads = downloads
        self.upload_date = uploaded_at
        self.version = self.extract_mc_version()
        self.loader = self.try_to_define_loader()

    def __str__(self):
        return f"(id={self.id}, filename={self.name}, type={self.type}, version={self.version}, versions={self.versions}, date={self.upload_date}, url={self.url}, loader={self.loader})"

    def __repr__(self):
        return self.__str__()

    def extract_mc_version(self):
        for version in self.versions:
            if version[0].isdigit():
                return version
        return None

    def try_to_define_loader(self):
        for version in self.versions:
            version = version.lower().strip()
            if version in AVAILABLE_LOADERS:
                return version
        name = self.name.lower().strip()
        for version in AVAILABLE_LOADERS:
            if version in name:
                return version
        return None

    def build(self):
        return VersionData(self.version, mod_version_from_file_name(self.name), self.loader, self.url, self.type)

class VersionData:
    def __init__(self, mc_version, mod_version, loader, url, release):
        self.mc_version = mc_version
        self.mod_version = mod_version
        self.loader = loader
        self.url = url
        self.release = release

    def __str__(self):
        return f"(mc_version={self.mc_version}, mod_version={self.mod_version}, loader={self.loader}, release={self.release}, url={self.url})"

    def __repr__(self):
        return self.__str__()

def mod_version_from_file_name(filename):
    matches = list(re.finditer(r'-([^-]*)', filename))
    ret = matches[1].group()[1:]
    if len(matches) < 2:
        return "unknown"
    if ret.find(".jar") != -1:
        ret = ret[:-4]
    return ret

