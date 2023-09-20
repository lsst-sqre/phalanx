# prompt-proto-service-hsc

Deployment for prompt proto service for HSC images

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| prompt-proto-service.additionalVolumeMounts | list | `[]` | Kubernetes YAML configs for extra container volume(s). Any volumes required by other config options are automatically handled by the Helm chart. |
| prompt-proto-service.apdb.db | string | `"lsst-devl"` | PostgreSQL database name for the APDB |
| prompt-proto-service.apdb.ip | string | None, must be set | IP address or hostname and port of the APDB |
| prompt-proto-service.apdb.namespace | string | `"pp_apdb"` | Database namespace for the APDB |
| prompt-proto-service.apdb.user | string | `"rubin"` | Database user for the APDB |
| prompt-proto-service.image.pullPolicy | string | `IfNotPresent` in prod, `Always` in dev | Pull policy for the PP image |
| prompt-proto-service.image.repository | string | `"ghcr.io/lsst-dm/prompt-proto-service"` | Image to use in the PP deployment |
| prompt-proto-service.image.tag | string | `"latest"` | Overrides the image tag whose default is the chart appVersion. |
| prompt-proto-service.imageNotifications.imageTimeout | string | `"120"` | Timeout to wait after expected script completion for raw image arrival (seconds). |
| prompt-proto-service.imageNotifications.kafkaClusterAddress | string | None, must be set | Hostname and port of the Kafka provider |
| prompt-proto-service.imageNotifications.topic | string | None, must be set | Topic where raw image arrival notifications appear |
| prompt-proto-service.instrument.calibRepo | string | None, must be set | URI to the shared repo used for calibrations, templates, and pipeline outputs. If `registry.centralRepoFile` is set, this URI points to a local redirect instead of the central repo itself. |
| prompt-proto-service.instrument.name | string | `"HSC"` | The "short" name of the instrument |
| prompt-proto-service.instrument.pipelines | string | None, must be set | Machine-readable string describing which pipeline(s) should be run for which visits. Notation is complex and still in flux; see [the source code](https://github.com/lsst-dm/prompt_prototype/blob/main/python/activator/config.py) for examples. |
| prompt-proto-service.instrument.skymap | string | `"hsc_rings_v1"` | Skymap to use with the instrument |
| prompt-proto-service.knative.ephemeralStorageLimit | string | `"20Gi"` | The maximum storage space allowed for each container (mostly local Butler). |
| prompt-proto-service.knative.ephemeralStorageRequest | string | `"20Gi"` | The storage space reserved for each container (mostly local Butler). |
| prompt-proto-service.knative.idleTimeout | int | `900` | Maximum time that a container can send nothing to the fanout service (seconds). |
| prompt-proto-service.knative.responseStartTimeout | int | `900` | Maximum time that a container can send nothing to the fanout service after initial submission (seconds). |
| prompt-proto-service.knative.timeout | int | `900` | Maximum time that a container can respond to a next_visit request (seconds). |
| prompt-proto-service.logLevel | string | log prompt_prototype at DEBUG, other LSST code at INFO, and third-party code at WARNING. | Requested logging levels in the format of [Middleware's \-\-log-level argument](https://pipelines.lsst.io/v/daily/modules/lsst.daf.butler/scripts/butler.html#cmdoption-butler-log-level). |
| prompt-proto-service.podAnnotations | object | See the `values.yaml` file. | Annotations for the prompt-proto-service pod |
| prompt-proto-service.registry.centralRepoFile | bool | `false` | If set, this application's Vault secret must contain a `central_repo_file` key containing a remote Butler configuration, and `instrument.calibRepo` is the local path where this file is mounted. |
| prompt-proto-service.registry.db | string | None, must be set | PostgreSQL database name for the Butler registry database |
| prompt-proto-service.registry.ip | string | None, must be set | IP address or hostname and port of the Butler registry database |
| prompt-proto-service.registry.user | string | None, must be set | Database user for the Butler registry database |
| prompt-proto-service.s3.auth_env | bool | `true` | If set, get S3 credentials from this application's Vault secret. |
| prompt-proto-service.s3.disableBucketValidation | string | `"0"` | Set this to disable validation of S3 bucket names, allowing Ceph multi-tenant colon-separated names to be used. |
| prompt-proto-service.s3.endpointUrl | string | None, must be set | S3 endpoint containing `imageBucket` |
| prompt-proto-service.s3.imageBucket | string | None, must be set | Bucket containing the incoming raw images |
