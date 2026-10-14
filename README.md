# pbx-lv2-records-uploader

Simple selectel upload

```python
    from pbx_component_files_uploader.uploader import Uploader

    api = Uploader(Uploader.STORAGE_SELECTEL, {
        'username': 'user',
        'password': 'pass',
        'container': 'container_name'
    }, {
        'token_cache_dir': '/path/to/cache/dir'
    })

    uploadedFileUrl = api.upload(
        '/path/to/src/file', 'dst_folder/dst_filename')
```

DigitalOcean Spaces upload (S3-compatible, via boto3)

```python
    from pbx_component_files_uploader.uploader import Uploader

    api = Uploader(Uploader.STORAGE_DIGITALOCEAN, {
        'access_key': 'spaces_access_key',
        'secret_key': 'spaces_secret_key',
        'bucket': 'bucket_name',
        'region': 'fra1'  # optional, default 'fra1'
    }, {
        'acl': 'public-read',        # optional, default 'public-read'
        'endpoint_url': 'https://fra1.digitaloceanspaces.com',  # optional
        'max_retries': 3             # optional, default 3
    })

    uploadedFileUrl = api.upload(
        '/path/to/src/file', 'dst_folder/dst_filename')
```
