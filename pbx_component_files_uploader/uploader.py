from .exceptions.errors import NotAllowed
from .ext.selectel.selectel import Selectel
from .ext.digitalocean.digitalocean import DigitalOcean


class Uploader:

    STORAGE_SELECTEL = 'selectel'
    STORAGE_DIGITALOCEAN = 'digitalocean'

    def __init__(self, service: str, auth: dict = {}, options: dict = {}) -> None:
        if self.is_allowed_storage(service=service):
            self.service = service
        else:
            raise NotAllowed('Service ' + service + ' is not allowed')
        self.auth = auth
        self.options = options

    def is_allowed_storage(self, service: str) -> bool:
        return service in [self.STORAGE_SELECTEL, self.STORAGE_DIGITALOCEAN]

    def upload(self, srcFilePath, dstName) -> str:
        if self.service == self.STORAGE_SELECTEL:
            selectel = Selectel(self.auth, self.options)
            return selectel.upload(srcFilePath=srcFilePath, dstFileName=dstName)
        if self.service == self.STORAGE_DIGITALOCEAN:
            digitalocean = DigitalOcean(self.auth, self.options)
            return digitalocean.upload(srcFilePath=srcFilePath, dstFileName=dstName)
