# fov-quicklook

Full focal plane viewer

## Source Code

* <https://github.com/lsst-sqre/fov-quicklook>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| butler_settings | object | `{"data_repos":{"embargo":"s3://embargo@rubin-summit-users/butler.yaml"},"envs":[{"name":"DAF_BUTLER_REPOSITORY_INDEX","value":"/var/run/fov-quicklook/config/data-repos.yaml"},{"name":"AWS_SHARED_CREDENTIALS_FILE","value":"/var/run/fov-quicklook/secrets/aws-credentials.ini"},{"name":"PGUSER","value":"rubin"},{"name":"PGPASSFILE","value":"/var/run/fov-quicklook/secrets/postgres-credentials.txt"},{"name":"S3_ENDPOINT_URL","value":"https://s3dfrgw.slac.stanford.edu"},{"name":"LSST_DISABLE_BUCKET_VALIDATION","value":"1"},{"name":"LSST_RESOURCES_S3_PROFILE_embargo","value":"https://sdfembs3.sdf.slac.stanford.edu"}],"volume_mounts":[{"mountPath":"/var/run/fov-quicklook/secrets/aws-credentials.ini","name":"aws-credentials","subPath":"aws-credentials.ini"},{"mountPath":"/var/run/fov-quicklook/secrets/postgres-credentials.txt","name":"postgres-credentials","subPath":"postgres-credentials.txt"},{"mountPath":"/var/run/fov-quicklook/config","name":"butler-config"}],"volumes":[{"name":"aws-credentials","secret":{"secretName":"fov-quicklook"}},{"name":"postgres-credentials","secret":{"secretName":"fov-quicklook"}},{"configMap":{"name":"fov-quicklook-butler-config"},"name":"butler-config"}]}` | Butler settings for the fov-quicklook application |
| config.max_object_storage_usage | int | `100000000000` | Maximum allowed storage usage for object storage in bytes |
| config.pathPrefix | string | `"/fov-quicklook"` | URL path prefix |
| config.s3_tile_path_prefix | string | `"fov-quicklook/prod"` | path prefix for object storage for tiles |
| context_menu_templates | list | `[]` | Context menu templates for the frontend |
| coordinator.resources.limits | object | `{"cpu":"4000m","memory":"512Mi"}` | Resource limits for the coordinator |
| coordinator.resources.requests | object | `{"cpu":"100m","memory":"512Mi"}` | Resource requests for the coordinator |
| db.resources.limits | object | `{"cpu":"2000m","memory":"256Mi"}` | Resource limits for the database |
| db.resources.requests | object | `{"cpu":"100m","memory":"256Mi"}` | Resource requests for the database |
| db_storage_class | string | `nil` | Storage class to use for the database |
| frontend.replicas | int | `2` |  |
| frontend.resources.limits | object | `{"cpu":"8000m","memory":"512Mi"}` | Resource limits for the frontend |
| frontend.resources.requests | object | `{"cpu":"100m","memory":"512Mi"}` | Resource requests for the frontend |
| generator.concurrency | int | `20` | Number of concurrent tile generations |
| generator.local_storage | object | `{"sizeLimit":"32Gi"}` | Local storage configuration for the generator |
| generator.replicas | int | `8` | Number of replicas for the generator |
| generator.resources.limits | object | `{"cpu":"12000m","memory":"8Gi"}` | Resource limits for the generator |
| generator.resources.requests | object | `{"cpu":"2000m","memory":"8Gi"}` | Resource requests for the generator |
| image.pullPolicy | string | `"Always"` | Pull policy for the fov-quicklook image |
| image.repository | string | `"ghcr.io/lsst-sqre/fov-quicklook:main"` | Image to use in the fov-quicklook deployment |
| image.tag | string | `"latest"` | Tag of image to use |
| s3_tile | object | `{"bucket":"fov-quicklook-tile","endpoint":"sdfembs3.sdf.slac.stanford.edu:443","secure":true}` | S3 configuration for the tile storage |
| use_gafaelfawr | bool | `true` | Use gafaelfawr to authenticate |
| use_vault | bool | `true` | Use vault to store secrets |
