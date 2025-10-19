# fov-quicklook

Full focal plane viewer

## Source Code

* <https://github.com/lsst-sqre/fov-quicklook>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.max_object_storage_usage | int | `100000000000` | Maximum allowed storage usage for object storage in bytes |
| config.pathPrefix | string | `"/fov-quicklook"` | URL path prefix |
| config.s3_tile_path_prefix | string | `"fov-quicklook/prod"` | path prefix for object storage for tiles |
| context_menu_templates | list | `[]` | Context menu templates for the frontend |
| coordinator.resources.limits | object | `{"cpu":"4000m","memory":"256Mi"}` | Resource limits for the coordinator |
| coordinator.resources.requests | object | `{"cpu":"100m","memory":"256Mi"}` | Resource requests for the coordinator |
| db.resources.limits | object | `{"cpu":"2000m","memory":"256Mi"}` | Resource limits for the database |
| db.resources.requests | object | `{"cpu":"100m","memory":"256Mi"}` | Resource requests for the database |
| db_storage_class | string | `nil` | Storage class to use for the database |
| frontend.resources.limits | object | `{"cpu":"8000m","memory":"512Mi"}` | Resource limits for the frontend |
| frontend.resources.requests | object | `{"cpu":"100m","memory":"512Mi"}` | Resource requests for the frontend |
| generator.concurrency | int | `20` | Number of concurrent tile generations |
| generator.local_storage | object | `{"sizeLimit":"32Gi"}` | Local storage configuration for the generator |
| generator.replicas | int | `8` | Number of replicas for the generator |
| generator.resources.limits | object | `{"cpu":"12000m","memory":"8Gi"}` | Resource limits for the generator |
| generator.resources.requests | object | `{"cpu":"4000m","memory":"8Gi"}` | Resource requests for the generator |
| image.pullPolicy | string | `"Always"` | Pull policy for the fov-quicklook image |
| image.repository | string | `"ghcr.io/michitaro/rubin-fov-viewer"` | Image to use in the fov-quicklook deployment |
| image.tag | string | `"latest"` | Tag of image to use |
| s3_tile | object | `{"bucket":"fov-quicklook-tile","endpoint":"sdfembs3.sdf.slac.stanford.edu:443","secure":true}` | S3 configuration for the tile storage |
| use_gafaelfawr | bool | `true` | Use gafaelfawr to authenticate |
| use_vault | bool | `true` | Use vault to store secrets |
