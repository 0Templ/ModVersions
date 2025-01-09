class FileData:

    def __init__(self, id, url, display, filename, type, version, filesize, versions, downloads, upload_date):
        self.id = id
        self.url = url
        self.display = display
        self.filename = filename
        self.type = type
        self.version = version
        self.filesize = filesize
        self.versions = versions
        self.downloads = downloads
        self.upload_date = upload_date

    def __str__(self):
        return f"(id={self.id}, filename={self.filename}, type={self.type}, version={self.version}, versions={self.versions}, date={self.upload_date}, url={self.url})"

    def __repr__(self):
        return self.__str__()

class VersionData:
    def __init__(self, mc_version, mod_version, loader, url, type):
        self.mc_version = mc_version
        self.mod_version = mod_version
        self.loader = loader
        self.url = url
        self.type = type
    def __str__(self):
        return f"(mc_version={self.mc_version}, mod_version={self.mod_version}, loader={self.loader}, type={self.type}, url={self.url})"

    def __repr__(self):
        return self.__str__()

