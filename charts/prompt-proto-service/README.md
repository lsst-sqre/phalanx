# prompt-proto-service

Event-driven processing of camera images

**Homepage:** <https://github.com/lsst-dm/prompt_processing/blob/main/doc/playbook.rst>

## Source Code

* <https://github.com/lsst-dm/prompt_processing>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| additionalVolumeMounts | list | `[]` | Kubernetes YAML configs for extra container volume(s). Any volumes required by other config options are automatically handled by the Helm chart. |
| affinity | object | `{}` |  |
| alerts.server | string | `"usdf-alert-stream-dev-broker-0.lsst.cloud:9094"` | Server address for the alert stream |
| alerts.topic | string | alert-stream-test | Topic name where alerts will be sent |
| alerts.username | string | `"kafka-admin"` | Username for sending alerts to the alert stream |
| apdb.config | string | None, must be set | URL to a serialized APDB configuration, or the "label:" prefix followed by the indexed name of such a config. |
| cache.baseSize | int | `3` | The default number of datasets of each type to keep. The pipeline only needs one of most dataset types (one bias, one flat, etc.), so this is roughly the number of visits that fit in the cache. |
| cache.patchesPerImage | int | `4` | A factor by which to multiply `baseSize` for templates and other patch-based datasets. |
| cache.refcatsPerImage | int | `4` | A factor by which to multiply `baseSize` for refcat datasets. |
| containerConcurrency | int | `1` | The number of Knative requests that can be handled simultaneously by one container |
| debug.exportOutputs | bool | `true` | Whether or not pipeline outputs should be exported to the central repo. This flag does not turn off APDB writes or alert generation; those must be handled at the pipeline level or by setting up an alternative destination. |
| fullnameOverride | string | `"prompt-proto-service"` | Override the full name for resources (includes the release name) |
| image.pullPolicy | string | `IfNotPresent` in prod, `Always` in dev | Pull policy for the PP image |
| image.repository | string | `"ghcr.io/lsst-dm/prompt-service"` | Image to use in the PP deployment |
| image.tag | string | `"latest"` | Overrides the image tag whose default is the chart appVersion. |
| imageNotifications.consumerOffsetReset | string | `"latest"` | Kafka consumer offset reset setting for image arrival notifications |
| imageNotifications.imageTimeout | int | `20` | Timeout to wait after expected script completion for raw image arrival (seconds). |
| imageNotifications.kafkaClusterAddress | string | None, must be set | Hostname and port of the Kafka provider |
| imageNotifications.topic | string | None, must be set | Topic where raw image arrival notifications appear |
| imagePullSecrets | list | `[]` |  |
| instrument.calibRepo | string | None, must be set | URI to the shared repo used for calibrations, templates, and pipeline outputs. If `registry.centralRepoFile` is set, this URI points to a local redirect instead of the central repo itself. |
| instrument.name | string | None, must be set | The "short" name of the instrument |
| instrument.pipelines.main | string | None, must be set | YAML-formatted config describing which pipeline(s) should be run for which visits' raws. Fields are still in flux; see [the source code](https://github.com/lsst-dm/prompt_processing/blob/main/python/activator/config.py) for examples. |
| instrument.pipelines.preprocessing | string | None, must be set | YAML-formatted config describing which pipeline(s) should be run before which visits' raw arrival. |
| instrument.preloadPadding | int | `30` | Number of arcseconds to pad the spatial region in preloading. |
| instrument.skymap | string | `""` | Skymap to use with the instrument |
| knative.cpuLimit | int | `1` | The maximum cpu cores for the full pod (see `containerConcurrency`). |
| knative.cpuRequest | int | `1` | The cpu cores requested for the full pod (see `containerConcurrency`). |
| knative.ephemeralStorageLimit | string | `"5Gi"` | The maximum storage space allowed for each container (mostly local Butler). This allocation is for the full pod (see `containerConcurrency`) |
| knative.ephemeralStorageRequest | string | `"5Gi"` | The storage space reserved for each container (mostly local Butler). This allocation is for the full pod (see `containerConcurrency`) |
| knative.extraTimeout | int | `10` | To acommodate scheduling problems, Knative waits for a request for twice `worker.timeout`. This parameter adds extra time to that minimum (seconds). |
| knative.gpu | bool | `false` | GPUs enabled. |
| knative.gpuRequest | int | `0` | The number of GPUs to request for the full pod (see `containerConcurrency`). |
| knative.idleTimeout | int | `0` | Maximum time that a container can send nothing to Knative (seconds). This is only useful if the container runs async workers. If 0, idle timeout is ignored. |
| knative.memoryLimit | string | `"8Gi"` | The maximum memory limit for the full pod (see `containerConcurrency`). |
| knative.memoryRequest | string | `"2Gi"` | The minimum memory to request for the full pod (see `containerConcurrency`). |
| knative.responseStartTimeout | int | `0` | Maximum time that a container can send nothing to Knative after initial submission (seconds). This is only useful if the container runs async workers. If 0, startup timeout is ignored. |
| logLevel | string | log prompt_processing at DEBUG, other LSST code at INFO, and third-party code at WARNING. | Requested logging levels in the format of [Middleware's \-\-log-level argument](https://pipelines.lsst.io/v/daily/modules/lsst.daf.butler/scripts/butler.html#cmdoption-butler-log-level). |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | See the `values.yaml` file. | Annotations for the prompt-proto-service pod |
| raw_microservice | string | `""` | The URI to a microservice that maps image metadata to a file location. If empty, Prompt Processing does not use a microservice. |
| registry.centralRepoFile | bool | `false` | If set, this application's Vault secret must contain a `central_repo_file` key containing a remote Butler configuration, and `instrument.calibRepo` is the local path where this file is mounted. |
| s3.auth_env | bool | `true` | If set, get S3 credentials from this application's Vault secret. |
| s3.disableBucketValidation | int | `0` | Set this to disable validation of S3 bucket names, allowing Ceph multi-tenant colon-separated names to be used. |
| s3.endpointUrl | string | None, must be set | S3 endpoint containing `imageBucket` |
| s3.imageBucket | string | None, must be set | Bucket containing the incoming raw images |
| sasquatch.auth_env | bool | `true` | If set, this application's Vault secret must contain a `sasquatch_token` key containing the authentication token for `sasquatch.endpointUrl`. Leave unset to attempt anonymous access. |
| sasquatch.endpointUrl | string | `""` | Url of the Sasquatch proxy server to upload metrics to. Leave blank to disable upload. This is a preliminary implementation of Sasquatch support, and this parameter may be deprecated if we instead support `SasquatchDatastore` in the future. |
| sasquatch.namespace | string | `"lsst.prompt"` | Namespace in the Sasquatch system with which to associate metrics. |
| tolerations | list | `[]` |  |
| worker.grace_period | int | `45` | When Knative shuts down a pod, the time its workers have to abort processing and save intermediate results (seconds). |
| worker.restart | int | `0` | The number of requests to process before rebooting a worker. If 0, workers process requests indefinitely. |
| worker.timeout | int | `900` | Maximum time that a worker can process a next_visit request (seconds). |
