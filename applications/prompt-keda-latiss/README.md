# prompt-keda-latiss

KEDA Prompt Processing instance for LATISS

**Homepage:** <https://github.com/lsst-dm/prompt_processing/blob/main/doc/playbook.rst>

## Source Code

* <https://github.com/lsst-dm/prompt_processing>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| prompt-keda.additionalVolumeMounts | list | `[]` | Kubernetes YAML configs for extra container volume(s). Any volumes required by other config options are automatically handled by the Helm chart. |
| prompt-keda.affinity | object | `{}` | Affinity rules for the Prompt Processing Pod |
| prompt-keda.alerts.server | string | `""` | Server address for the alert stream |
| prompt-keda.alerts.topic | string | `""` | Topic name where alerts will be sent |
| prompt-keda.alerts.username | string | `""` | Username for sending alerts to the alert stream |
| prompt-keda.apdb.config | string | None, must be set | URL to a serialized APDB configuration, or the "label:" prefix followed by the indexed name of such a config. |
| prompt-keda.cache.baseSize | int | `3` | The default number of datasets of each type to keep. The pipeline only needs one of most dataset types (one bias, one flat, etc.), so this is roughly the number of visits that fit in the cache. |
| prompt-keda.cache.patchesPerImage | int | `6` | A factor by which to multiply `baseSize` for templates and other patch-based datasets. |
| prompt-keda.cache.refcatsPerImage | int | `4` | A factor by which to multiply `baseSize` for refcat datasets. |
| prompt-keda.debug.exportOutputs | bool | `true` | Whether or not pipeline outputs should be exported to the central repo. This flag does not turn off APDB writes or alert generation; those must be handled at the pipeline level or by setting up an alternative destination. |
| prompt-keda.fullnameOverride | string | `"prompt-keda-latiss"` | Override the full name for resources (includes the release name) |
| prompt-keda.image.pullPolicy | string | `IfNotPresent` in prod, `Always` in dev | Pull policy for the PP image |
| prompt-keda.image.repository | string | `"ghcr.io/lsst-dm/prompt-service"` | Image to use in the PP deployment |
| prompt-keda.image.tag | string | `"latest"` | Overrides the image tag whose default is the chart appVersion. |
| prompt-keda.imageNotifications.consumerOffsetReset | string | `"latest"` | Kafka consumer offset reset setting for image arrival notifications |
| prompt-keda.imageNotifications.imageTimeout | int | `20` | Timeout to wait after expected script completion for raw image arrival (seconds). |
| prompt-keda.imageNotifications.kafkaClusterAddress | string | None, must be set | Hostname and port of the Kafka provider |
| prompt-keda.imageNotifications.topic | string | None, must be set | Topic where raw image arrival notifications appear |
| prompt-keda.initializer.cleanup_delay | int | `3600` | Time after which to remove old initializer pods (seconds). |
| prompt-keda.initializer.cron.day_obs_tz | int | `-12` | Time zone in which day_obs is computed. |
| prompt-keda.initializer.cron.suspend | bool | `false` | Whether or not to pause daily initializer runs. This makes it impossible to run Prompt Processing, but avoids repo clutter if the telescope is offline. |
| prompt-keda.initializer.image.repository | string | `"ghcr.io/lsst-dm/prompt-init"` | Image to use for the PP initializer |
| prompt-keda.initializer.podAnnotations | object | See the `values.yaml` file. | Pod annotations for the init-output Job |
| prompt-keda.initializer.resources.cpuLimit | int | `1` | The maximum cpu cores for the initializer. |
| prompt-keda.initializer.resources.cpuRequest | int | `1` | The cpu cores requested for the initializer. |
| prompt-keda.initializer.resources.memoryLimit | string | `"1Gi"` | The maximum memory limit for the initializer. |
| prompt-keda.initializer.resources.memoryRequest | string | `"512Mi"` | The minimum memory to request for the initializer. |
| prompt-keda.initializer.retries | int | `6` | Maximum number of times to attempt initializing the central repo. If the initializer fails, the PP service cannot run! |
| prompt-keda.initializer.timeout | int | `120` | Maximum time for a single attempt to initialize the central repo (seconds). |
| prompt-keda.instrument.calibRepo | string | None, must be set | URI to the shared repo used for calibrations, templates, and pipeline outputs. If `registry.centralRepoFile` is set, this URI points to a local redirect instead of the central repo itself. |
| prompt-keda.instrument.name | string | `"LATISS"` | The "short" name of the instrument |
| prompt-keda.instrument.pipelines.main | string | None, must be set | YAML-formatted config describing which pipeline(s) should be run for which visits' raws. Fields are still in flux; see [the source code](https://github.com/lsst-dm/prompt_processing/blob/main/python/activator/config.py) for examples. |
| prompt-keda.instrument.pipelines.preprocessing | string | None, must be set | YAML-formatted config describing which pipeline(s) should be run before which visits' raw arrival. |
| prompt-keda.instrument.preloadPadding | int | `30` | Number of arcseconds to pad the spatial region in preloading. |
| prompt-keda.instrument.skymap | string | `"latiss_v1"` | Skymap to use with the instrument |
| prompt-keda.keda.failedJobsHistoryLimit | int | `5` |  |
| prompt-keda.keda.maxReplicaCount | int | `30` |  |
| prompt-keda.keda.minReplicaCount | int | `3` |  |
| prompt-keda.keda.pollingInterval | int | `2` |  |
| prompt-keda.keda.redisStreams.activationLagCount | string | `"1"` |  |
| prompt-keda.keda.redisStreams.consumerGroup | string | `"latiss_consumer_group"` |  |
| prompt-keda.keda.redisStreams.expiration | int | `3600` | Maximum message age to process, in seconds. |
| prompt-keda.keda.redisStreams.host | string | `"prompt-redis.prompt-redis"` |  |
| prompt-keda.keda.redisStreams.lagCount | string | `"1"` |  |
| prompt-keda.keda.redisStreams.msgListenTimeout | int | `900` |  |
| prompt-keda.keda.redisStreams.pendingEntriesCount | string | `"1"` |  |
| prompt-keda.keda.redisStreams.streamName | string | `"instrument:latiss"` |  |
| prompt-keda.keda.scalingStrategy | string | `"eager"` |  |
| prompt-keda.keda.successfulJobsHistoryLimit | int | `5` |  |
| prompt-keda.logLevel | string | log prompt_processing at DEBUG, other LSST code at INFO, and third-party code at WARNING. | Requested logging levels in the format of [Middleware's \-\-log-level argument](https://pipelines.lsst.io/v/daily/modules/lsst.daf.butler/scripts/butler.html#cmdoption-butler-log-level). |
| prompt-keda.nameOverride | string | `""` | Override the base name for resources |
| prompt-keda.nodeSelector | object | `{}` | Node selection rules for the Prompt Processing pod |
| prompt-keda.podAnnotations | object | `{}` | Pod annotations for the Prompt Processing Pod |
| prompt-keda.raw_microservice | string | `""` | The URI to a microservice that maps image metadata to a file location. If empty, Prompt Processing does not use a microservice. |
| prompt-keda.registry.centralRepoFile | bool | `false` | If set, this application's Vault secret must contain a `central_repo_file` key containing a remote Butler configuration, and `instrument.calibRepo` is the local path where this file is mounted. |
| prompt-keda.resources | object | See `values.yaml` | Kubernetes resource requests and limits |
| prompt-keda.s3.auth_env | bool | `true` | If set, get S3 credentials from this application's Vault secret. |
| prompt-keda.s3.checksum | string | `"WHEN_REQUIRED"` | If set, configure S3 checksum options. |
| prompt-keda.s3.disableBucketValidation | string | `"0"` | Set this to disable validation of S3 bucket names, allowing Ceph multi-tenant colon-separated names to be used. |
| prompt-keda.s3.endpointUrl | string | `""` |  |
| prompt-keda.s3.imageBucket | string | None, must be set | Bucket containing the incoming raw images |
| prompt-keda.sasquatch.auth_env | bool | `true` | If set, this application's Vault secret must contain a `sasquatch_token` key containing the authentication token for `sasquatch.endpointUrl`. Leave unset to attempt anonymous access. |
| prompt-keda.sasquatch.endpointUrl | string | `""` | Url of the Sasquatch proxy server to upload metrics to. Leave blank to disable upload. This is a preliminary implementation of Sasquatch support, and this parameter may be deprecated if we instead support `SasquatchDatastore` in the future. |
| prompt-keda.sasquatch.namespace | string | `"lsst.prompt"` | Namespace in the Sasquatch system with which to associate metrics. |
| prompt-keda.tolerations | list | `[]` | Tolerations for the Prompt Processing pod |
| prompt-keda.worker.grace_period | int | `45` | When Kubernetes shuts down a pod, the time its workers have to abort processing and save intermediate results (seconds). |
| prompt-keda.worker.restart | int | `0` | The number of requests to process before rebooting a worker. If 0, workers process requests indefinitely. |
