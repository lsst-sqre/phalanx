# fov-quicklook

Full focal plane viewer

## Source Code

* <https://github.com/michitaro/rubin-fov-quicklook>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.pathPrefix | string | `"/fov-quicklook"` | URL path prefix |
| context_menu_templates | list | `[]` | Context menu templates for the frontend |
| coordinator.resources.limits | object | `{"cpu":"4000m","memory":"256Mi"}` | Resource limits for the coordinator |
| coordinator.resources.requests | object | `{"cpu":"100m","memory":"256Mi"}` | Resource requests for the coordinator |
| db.resources.limits | object | `{"cpu":"2000m","memory":"256Mi"}` | Resource limits for the database |
| db.resources.requests | object | `{"cpu":"100m","memory":"256Mi"}` | Resource requests for the database |
| db_storage_class | string | `nil` | Storage class to use for the database |
| frontend.resources.limits | object | `{"cpu":"8000m","memory":"512Mi"}` | Resource limits for the frontend |
| frontend.resources.requests | object | `{"cpu":"100m","memory":"512Mi"}` | Resource requests for the frontend |
| generator.mergedDir.sizeLimit | string | `"32Gi"` | Size limit for the merged directory |
| generator.replicas | int | `9` | Number of replicas for the generator |
| generator.resources.limits | object | `{"cpu":"16000m","memory":"32Gi"}` | Resource limits for the generator |
| generator.resources.requests | object | `{"cpu":"8000m","memory":"32Gi"}` | Resource requests for the generator |
| generator.workdir.medium | string | `"Memory"` | Work directory type for the generator |
| generator.workdir.sizeLimit | string | `"32Gi"` | Size limit for the shared memory work directory |
| image.pullPolicy | string | `"Always"` | Pull policy for the fov-quicklook image |
| image.repository | string | `"ghcr.io/michitaro/rubin-fov-viewer"` | Image to use in the fov-quicklook deployment |
| image.tag | string | `"latest"` | Tag of image to use |
| s3_tile | object | `{"bucket":"fov-quicklook-tile","endpoint":"sdfembs3.sdf.slac.stanford.edu:443","secure":true}` | S3 configuration for the tile storage |
| use_gafaelfawr | bool | `true` | Use gafaelfawr to authenticate |
| use_vault | bool | `true` | Use vault to store secrets |
