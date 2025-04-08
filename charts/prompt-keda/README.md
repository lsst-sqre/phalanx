# prompt-keda

Event-driven processing of camera images

**Homepage:** <https://github.com/lsst-dm/prompt_processing/blob/main/doc/playbook.rst>

## Source Code

* <https://github.com/lsst-dm/prompt_processing>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| additionalVolumeMounts | list | `[]` | Kubernetes YAML configs for extra container volume(s). Any volumes required by other config options are automatically handled by the Helm chart. |
| affinity | object | `{}` | Affinity rules for the Prompt Processing Pod |
| alerts.server | string | `""` | Server address for the alert stream |
| alerts.topic | string | `""` | Topic name where alerts will be sent |
| alerts.username | string | `""` | Username for sending alerts to the alert stream |
| apdb.config | string | None, must be set | URL to a serialized APDB configuration, or the "label:" prefix followed by the indexed name of such a config. |
| cache.baseSize | int | `3` | The default number of datasets of each type to keep. The pipeline only needs one of most dataset types (one bias, one flat, etc.), so this is roughly the number of visits that fit in the cache. |
| cache.patchesPerImage | int | `4` | A factor by which to multiply `baseSize` for templates and other patch-based datasets. |
| cache.refcatsPerImage | int | `4` | A factor by which to multiply `baseSize` for refcat datasets. |
| debug.exportOutputs | bool | `true` | Whether or not pipeline outputs should be exported to the central repo. This flag does not turn off APDB writes or alert generation; those must be handled at the pipeline level or by setting up an alternative destination. |
| fullnameOverride | string | `"prompt-keda"` | Override the full name for resources (includes the release name) |
| image.pullPolicy | string | `IfNotPresent` in prod, `Always` in dev.  Set to `IfNotPresent` for scale testing in dev. | Pull policy for the Prompt Processing image |
| image.repository | string | `"ghcr.io/lsst-dm/prompt-service"` | Image to use in the Prompt Processing deployment |
| image.tag | string | `"latest"` | Overrides the image tag whose default is the chart appVersion. |
| imageNotifications.consumerOffsetReset | string | `"latest"` | Kafka consumer offset reset setting for image arrival notifications |
| imageNotifications.imageTimeout | int | `20` | Timeout to wait after expected script completion for raw image arrival (seconds). |
| imageNotifications.kafkaClusterAddress | string | None, must be set | Hostname and port of the Kafka provider |
| imageNotifications.topic | string | None, must be set | Topic where raw image arrival notifications appear |
| initializer.cleanup_delay | int | `3600` | Time after which to remove old initializer pods (seconds). |
| initializer.cron.day_obs_tz | int | `-12` | Time zone in which day_obs is computed. |
| initializer.cron.suspend | bool | `false` | Whether or not to pause daily initializer runs. This makes it impossible to run Prompt Processing, but avoids repo clutter if the telescope is offline. |
| initializer.image.repository | string | `"ghcr.io/lsst-dm/prompt-init"` | Image to use for the PP initializer |
| initializer.podAnnotations | object | See the `values.yaml` file. | Pod annotations for the init-output Job |
| initializer.resources.cpuLimit | int | `1` | The maximum cpu cores for the initializer. |
| initializer.resources.cpuRequest | int | `1` | The cpu cores requested for the initializer. |
| initializer.resources.memoryLimit | string | `"1Gi"` | The maximum memory limit for the initializer. |
| initializer.resources.memoryRequest | string | `"512Mi"` | The minimum memory to request for the initializer. |
| initializer.retries | int | `6` | Maximum number of times to attempt initializing the central repo. If the initializer fails, the PP service cannot run! |
| initializer.timeout | int | `120` | Maximum time for a single attempt to initialize the central repo (seconds). |
| instrument.calibRepo | string | None, must be set | URI to the shared repo used for calibrations, templates, and pipeline outputs. If `registry.centralRepoFile` is set, this URI points to a local redirect instead of the central repo itself. |
| instrument.name | string | None, must be set | The "short" name of the instrument |
| instrument.pipelines.main | string | None, must be set | YAML-formatted config describing which pipeline(s) should be run for which visits' raws. Fields are still in flux; see [the source code](https://github.com/lsst-dm/prompt_processing/blob/main/python/activator/config.py) for examples. |
| instrument.pipelines.preprocessing | string | None, must be set | YAML-formatted config describing which pipeline(s) should be run before which visits' raw arrival. |
| instrument.preloadPadding | int | `30` | Number of arcseconds to pad the spatial region in preloading. |
| instrument.skymap | string | `""` | Skymap to use with the instrument |
| keda.failedJobsHistoryLimit | int | `25` |  |
| keda.maxReplicaCount | int | `10` |  |
| keda.minReplicaCount | int | `3` |  |
| keda.pollingInterval | int | `2` |  |
| keda.redisStreams.activationLagCount | string | `"1"` |  |
| keda.redisStreams.consumerGroup | string | `""` |  |
| keda.redisStreams.expiration | int | `3600` | Maximum message age to process, in seconds. |
| keda.redisStreams.host | string | `""` |  |
| keda.redisStreams.lagCount | string | `"1"` |  |
| keda.redisStreams.msgListenTimeout | int | `900` |  |
| keda.redisStreams.pendingEntriesCount | string | `"1"` |  |
| keda.redisStreams.streamName | string | `""` |  |
| keda.scalingStrategy | string | `"eager"` |  |
| keda.successfulJobsHistoryLimit | int | `25` |  |
| logLevel | string | log prompt_processing at DEBUG, other LSST code at INFO, and third-party code at WARNING. | Requested logging levels in the format of [Middleware's \-\-log-level argument](https://pipelines.lsst.io/v/daily/modules/lsst.daf.butler/scripts/butler.html#cmdoption-butler-log-level). |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selection rules for the Prompt Porcessing pod |
| podAnnotations | object | `{"prometheus.io/port":"8000","prometheus.io/scrape":"true"}` | Pod annotations for the Prompt Processing Pod |
| raw_microservice | string | `""` | The URI to a microservice that maps image metadata to a file location. If empty, Prompt Processing does not use a microservice. |
| registry.centralRepoFile | bool | `false` | If set, this application's Vault secret must contain a `central_repo_file` key containing a remote Butler configuration, and `instrument.calibRepo` is the local path where this file is mounted. |
| resources | object | See `values.yaml` | Kubernetes resource requests and limits |
| s3.auth_env | bool | `true` | If set, get S3 credentials from this application's Vault secret. |
| s3.disableBucketValidation | int | `0` | Set this to disable validation of S3 bucket names, allowing Ceph multi-tenant colon-separated names to be used. |
| s3.endpointUrl | string | None, must be set | S3 endpoint containing `imageBucket` |
| s3.imageBucket | string | None, must be set | Bucket containing the incoming raw images |
| sasquatch.auth_env | bool | `true` | If set, this application's Vault secret must contain a `sasquatch_token` key containing the authentication token for `sasquatch.endpointUrl`. Leave unset to attempt anonymous access. |
| sasquatch.endpointUrl | string | `""` | Url of the Sasquatch proxy server to upload metrics to. Leave blank to disable upload. This is a preliminary implementation of Sasquatch support, and this parameter may be deprecated if we instead support `SasquatchDatastore` in the future. |
| sasquatch.namespace | string | `"lsst.prompt"` | Namespace in the Sasquatch system with which to associate metrics. |
| tolerations | list | `[]` | Tolerations for the Prompt Processing pod |
| worker.grace_period | int | `45` | When Kubernetes shuts down a pod, the time its workers have to abort processing and save intermediate results (seconds). |
| worker.restart | int | `0` | The number of requests to process before rebooting a worker. If 0, workers process requests indefinitely. |
