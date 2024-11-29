# fov-quicklook

Full focal plane viewer

## Source Code

* <https://github.com/michitaro/rubin-fov-quicklook>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.pathPrefix | string | `"/fov-quicklook"` | URL path prefix |
| db_storage_class | string | `nil` | Storage class to use for the database |
| image.pullPolicy | string | `"Always"` | Pull policy for the fov-quicklook image |
| image.repository | string | `"ghcr.io/michitaro/rubin-fov-viewer"` | Image to use in the fov-quicklook deployment |
| image.tag | string | `"latest"` | Tag of image to use |
| s3_repository | object | `{"bucket":"fov-quicklook-repository","endpoint":"sdfembs3.sdf.slac.stanford.edu:443","secure":true}` | S3 configuration for the repository |
| s3_tile | object | `{"bucket":"fov-quicklook-tile","endpoint":"sdfembs3.sdf.slac.stanford.edu:443","secure":true}` | S3 configuration for the tile storage |
| use_gafaelfawr | bool | `true` | Use gafaelfawr to authenticate |
| use_vault | bool | `true` | Use vault to store secrets |
