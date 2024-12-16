# prompt-proto-service-lsstcomcam

Prompt Proto Service is an event driven service for processing camera images. This instance of the service handles LSSTComCam images.

**Homepage:** <https://github.com/lsst-dm/prompt_processing/blob/main/doc/playbook.rst>

## Source Code

* <https://github.com/lsst-dm/prompt_processing>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| prompt-proto-service.additionalVolumeMounts | list | `[]` | Kubernetes YAML configs for extra container volume(s). Any volumes required by other config options are automatically handled by the Helm chart. |
| prompt-proto-service.affinity | object | `{}` | Affinity rules for the prompt processing pods |
| prompt-proto-service.alerts.server | string | `"usdf-alert-stream-dev.lsst.cloud:9094"` | Server address for the alert stream |
| prompt-proto-service.alerts.topic | string | `""` | Topic name where alerts will be sent |
| prompt-proto-service.alerts.username | string | `"kafka-admin"` | Username for sending alerts to the alert stream |
| prompt-proto-service.apdb.config | string | None, must be set | URL to a serialized APDB configuration, or the "label:" prefix followed by the indexed name of such a config. |
| prompt-proto-service.cache.baseSize | int | `3` | The default number of datasets of each type to keep. The pipeline only needs one of most dataset types (one bias, one flat, etc.), so this is roughly the number of visits that fit in the cache. |
| prompt-proto-service.cache.patchesPerImage | int | `16` | A factor by which to multiply `baseSize` for templates and other patch-based datasets. |
| prompt-proto-service.cache.refcatsPerImage | int | `6` | A factor by which to multiply `baseSize` for refcat datasets. |
| prompt-proto-service.containerConcurrency | int | `1` | The number of Knative requests that can be handled simultaneously by one container |
| prompt-proto-service.image.pullPolicy | string | `IfNotPresent` in prod, `Always` in dev | Pull policy for the PP image |
| prompt-proto-service.image.repository | string | `"ghcr.io/lsst-dm/prompt-service"` | Image to use in the PP deployment |
| prompt-proto-service.image.tag | string | `"latest"` | Overrides the image tag whose default is the chart appVersion. |
| prompt-proto-service.imageNotifications.consumerOffsetReset | string | `"latest"` | Kafka consumer offset reset setting for image arrival notifications |
| prompt-proto-service.imageNotifications.imageTimeout | int | `20` | Timeout to wait after expected script completion for raw image arrival (seconds). |
| prompt-proto-service.imageNotifications.kafkaClusterAddress | string | None, must be set | Hostname and port of the Kafka provider |
| prompt-proto-service.imageNotifications.topic | string | None, must be set | Topic where raw image arrival notifications appear |
| prompt-proto-service.instrument.calibRepo | string | None, must be set | URI to the shared repo used for calibrations, templates, and pipeline outputs. If `registry.centralRepoFile` is set, this URI points to a local redirect instead of the central repo itself. |
| prompt-proto-service.instrument.name | string | `"LSSTComCam"` | The "short" name of the instrument |
| prompt-proto-service.instrument.pipelines.main | string | None, must be set | YAML-formatted config describing which pipeline(s) should be run for which visits' raws. Fields are still in flux; see [the source code](https://github.com/lsst-dm/prompt_processing/blob/main/python/activator/config.py) for examples. |
| prompt-proto-service.instrument.pipelines.preprocessing | string | None, must be set | YAML-formatted config describing which pipeline(s) should be run before which visits' raw arrival. |
| prompt-proto-service.instrument.preloadPadding | int | `50` | Number of arcseconds to pad the spatial region in preloading. |
| prompt-proto-service.instrument.skymap | string | `"lsst_cells_v1"` | Skymap to use with the instrument |
| prompt-proto-service.knative.cpuLimit | int | `1` | The maximum cpu cores for the full pod (see `containerConcurrency`). |
| prompt-proto-service.knative.cpuRequest | int | `1` | The cpu cores requested for the full pod (see `containerConcurrency`). |
| prompt-proto-service.knative.ephemeralStorageLimit | string | `"8Gi"` | The maximum storage space allowed for each container (mostly local Butler). This allocation is for the full pod (see `containerConcurrency`) |
| prompt-proto-service.knative.ephemeralStorageRequest | string | `"8Gi"` | The storage space reserved for each container (mostly local Butler). This allocation is for the full pod (see `containerConcurrency`) |
| prompt-proto-service.knative.gpu | bool | `false` | GPUs enabled. |
| prompt-proto-service.knative.gpuRequest | int | `0` | The number of GPUs to request for the full pod (see `containerConcurrency`). |
| prompt-proto-service.knative.idleTimeout | int | `900` | Maximum time that a container can send nothing to Knative (seconds). This is only useful if the container runs async workers. If 0, idle timeout is ignored. |
| prompt-proto-service.knative.memoryLimit | string | `"8Gi"` | The maximum memory limit for the full pod (see `containerConcurrency`). |
| prompt-proto-service.knative.memoryRequest | string | `"2Gi"` | The minimum memory to request for the full pod (see `containerConcurrency`). |
| prompt-proto-service.knative.responseStartTimeout | int | `900` | Maximum time that a container can send nothing to Knative after initial submission (seconds). This is only useful if the container runs async workers. If 0, idle timeout is ignored. |
| prompt-proto-service.logLevel | string | log prompt_processing at DEBUG, other LSST code at INFO, and third-party code at WARNING. | Requested logging levels in the format of [Middleware's \-\-log-level argument](https://pipelines.lsst.io/v/daily/modules/lsst.daf.butler/scripts/butler.html#cmdoption-butler-log-level). |
| prompt-proto-service.podAnnotations | object | See the `values.yaml` file. | Annotations for the prompt-proto-service pod |
| prompt-proto-service.registry.centralRepoFile | bool | `false` | If set, this application's Vault secret must contain a `central_repo_file` key containing a remote Butler configuration, and `instrument.calibRepo` is the local path where this file is mounted. |
| prompt-proto-service.s3.auth_env | bool | `true` | If set, get S3 credentials from this application's Vault secret. |
| prompt-proto-service.s3.disableBucketValidation | int | `0` | Set this to disable validation of S3 bucket names, allowing Ceph multi-tenant colon-separated names to be used. |
| prompt-proto-service.s3.endpointUrl | string | None, must be set | S3 endpoint containing `imageBucket` |
| prompt-proto-service.s3.imageBucket | string | None, must be set | Bucket containing the incoming raw images |
| prompt-proto-service.sasquatch.auth_env | bool | `true` | If set, this application's Vault secret must contain a `sasquatch_token` key containing the authentication token for `sasquatch.endpointUrl`. Leave unset to attempt anonymous access. |
| prompt-proto-service.sasquatch.endpointUrl | string | `""` | Url of the Sasquatch proxy server to upload metrics to. Leave blank to disable upload. This is a preliminary implementation of Sasquatch support, and this parameter may be deprecated if we instead support `SasquatchDatastore` in the future. |
| prompt-proto-service.sasquatch.namespace | string | `"lsst.prompt"` | Namespace in the Sasquatch system with which to associate metrics. |
| prompt-proto-service.worker.grace_period | int | `45` | When Knative shuts down a pod, the time its workers have to abort processing and save intermediate results (seconds). |
| prompt-proto-service.worker.restart | int | `0` | The number of requests to process before rebooting a worker. If 0, workers process requests indefinitely. |
| prompt-proto-service.worker.timeout | int | `900` | Maximum time that a worker can process a next_visit request (seconds). |
