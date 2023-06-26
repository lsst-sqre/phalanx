# giftless

Git-LFS server with GCS S3 backend

## Source Code

* <https://github.com/datopian/giftless>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.AUTH_PROVIDERS[0] | string | `"giftless.auth.allow_anon:read_only"` |  |
| config.TRANSFER_ADAPTERS.basic.factory | string | `"giftless.transfer.basic_external:factory"` |  |
| config.TRANSFER_ADAPTERS.basic.options.storage_class | string | `"giftless.storage.google_cloud:GoogleCloudStorage"` |  |
| config.TRANSFER_ADAPTERS.basic.options.storage_options.account_key_file | string | `"/etc/secret/giftless-gcp-key.json"` |  |
| config.TRANSFER_ADAPTERS.basic.options.storage_options.bucket_name | string | `"rubin-gitlfs-experimental"` |  |
| config.TRANSFER_ADAPTERS.basic.options.storage_options.project_name | string | `"plasma-geode-127520"` |  |
| image.repository | string | `"docker.io/datopian/giftless"` |  |
| ingress.annotations | object | `{}` |  |
| ingress.hostname | string | `""` |  |
| server.debug | bool | `false` |  |
| server.port | int | `5000` |  |
| server.processes | int | `2` |  |
| server.threads | int | `2` |  |
