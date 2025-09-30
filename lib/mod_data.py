import re

AVAILABLE_LOADERS = ["fabric", "neoforge", "forge"]

class VersionData:

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
        self.mc_version = self.extract_mc_version()
        self.mod_version = self.mod_version_from_file_name()
        self.loader = self.try_to_define_loader()

    def __str__(self):
        return f"(id={self.id}, filename={self.name}, type={self.type}, version={self.mc_version}, versions={self.versions}, date={self.upload_date}, url={self.url}, loader={self.loader})"

    def __repr__(self):
        return self.__str__()

    def extract_mc_version(self):
        for version in self.versions:
            if version[0].isdigit():
                return version
        return None

    def try_to_define_loader(self):
        ret = []
        for version in self.versions:
            version = version.lower().strip()
            if version in AVAILABLE_LOADERS:
                ret.append(version)
        name = self.name.lower().strip()
        for version in AVAILABLE_LOADERS:
            if version in name and not version.isdigit() and version not in ret:
                ret.append(version)
        return ret

    def mod_version_from_file_name(self):
        matches = list(re.finditer(r'-([^-]*)', self.name))
        ret = matches[1].group()[1:]
        if len(matches) < 2:
            return "unknown"
        if ret.find(".jar") != -1:
            ret = ret[:-4]
        return ret

