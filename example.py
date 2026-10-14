from pbx_component_files_uploader.uploader import Uploader

if __name__ == '__main__':
    api = Uploader(Uploader.STORAGE_SELECTEL, {
        'username': 'user',
        'password': 'pass',
        'container': 'tmp'
    }, {
        'token_cache_dir': 'tmp'
    })

    uploadedFileUrl = api.upload('test.txt', 'test.txt')

    doApi = Uploader(Uploader.STORAGE_DIGITALOCEAN, {
        'access_key': 'spaces_access_key',
        'secret_key': 'spaces_secret_key',
        'bucket': 'tmp',
        'region': 'fra1'
    })

    uploadedFileUrl = doApi.upload('test.txt', 'test.txt')
