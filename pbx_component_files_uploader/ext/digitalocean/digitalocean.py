from pathlib import Path
from multiprocessing import get_logger

import boto3

from pbx_component_files_uploader.interfaces.base_uploader import BaseUploader
from pbx_component_files_uploader.exceptions.errors import UploadError, EmptyAuthField

log = get_logger()
log.name = 'digitalocean'


class DigitalOcean(BaseUploader):

    DEFAULT_REGION = 'fra1'
    DEFAULT_RETRIES = 3
    DEFAULT_ACL = 'public-read'

    def __init__(self, authData: dict, options: dict = {}):
        self.accessKey = authData.get('access_key')
        self.secretKey = authData.get('secret_key')
        self.bucket = authData.get('bucket')
        self.region = authData.get('region', self.DEFAULT_REGION)

        for field, value in (
                ('access_key', self.accessKey),
                ('secret_key', self.secretKey),
                ('bucket', self.bucket)):
            if not value:
                raise EmptyAuthField(field)

        self.endpointUrl = options.get('endpoint_url') or \
            'https://{region}.digitaloceanspaces.com'.format(region=self.region)
        self.acl = options.get('acl', self.DEFAULT_ACL)
        self.maxRetries = options.get('max_retries', self.DEFAULT_RETRIES)

        self.client = boto3.client(
            's3',
            region_name=self.region,
            endpoint_url=self.endpointUrl,
            aws_access_key_id=self.accessKey,
            aws_secret_access_key=self.secretKey,
        )

    def build_url(self, dstFile) -> str:
        key = dstFile.lstrip('/')
        defaultEndpoint = 'https://{region}.digitaloceanspaces.com'.format(region=self.region)
        if self.endpointUrl == defaultEndpoint:
            return 'https://{bucket}.{region}.digitaloceanspaces.com/{key}'.format(
                bucket=self.bucket, region=self.region, key=key)
        return '{endpoint}/{bucket}/{key}'.format(
            endpoint=self.endpointUrl.rstrip('/'), bucket=self.bucket, key=key)

    def upload(self, srcFilePath: str, dstFileName: str) -> str:
        srcFile = Path(srcFilePath)
        if not srcFile.is_file():
            raise ValueError(f'No such file [{srcFilePath}]')

        if not dstFileName:
            raise ValueError('Empty [dstFileName] field')

        errorDesc = ''
        for i in range(self.maxRetries):
            try:
                self.client.upload_file(
                    str(srcFile), self.bucket, dstFileName.lstrip('/'),
                    ExtraArgs={'ACL': self.acl})
                return self.build_url(dstFileName)
            except Exception as e:
                errorDesc = str(e)
                log.debug(f'Attempt [{i + 1}]. Failed to upload. Cause [{errorDesc}]')

        raise UploadError(400, f'Failed upload file [{srcFilePath}]. Cause [{errorDesc}]')
