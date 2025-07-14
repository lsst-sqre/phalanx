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
| butler_writer.enabled | bool | `false` | If false, output datasets will be written directly to the central Butler database.  If true, a Kafka message will be sent to a service to aggregate these writes instead. |
| butler_writer.image.repository | string | `"ghcr.io/lsst-dm/prompt_processing_butler_writer"` | Image to use for the Butler writer service |
| butler_writer.image.tag | string | `"tickets-dm-49670"` | Docker container version to use for the Butler writer service |
| butler_writer.kafka_topic | string | `"rubin-prompt-processing-butler-output"` | Kafka topic that prompt processing output events will be written to, for consumption by the Butler writer service. |
| butler_writer.output_file_path | string | `""` | Root path where output dataset files will be written when transferring back to the central repository.  Only used if butler_writer.enable is true. |
| butler_writer.resources.cpuLimit | int | `1` | The maximum cpu cores for the Butler writer service. |
| butler_writer.resources.cpuRequest | float | `0.25` | The cpu cores requested for the Butler writer service. |
| butler_writer.resources.memoryLimit | string | `"4Gi"` | The maximum memory limit for the Butler writer service. |
| butler_writer.resources.memoryRequest | string | `"2Gi"` | The minimum memory to request for the Butler writer service. |
| cache.baseSize | int | `3` | The default number of datasets of each type to keep. The pipeline only needs one of most dataset types (one bias, one flat, etc.), so this is roughly the number of visits that fit in the cache. |
| cache.patchesPerImage | int | `4` | A factor by which to multiply `baseSize` for templates and other patch-based datasets. |
| cache.refcatsPerImage | int | `4` | A factor by which to multiply `baseSize` for refcat datasets. |
| debug.exportOutputs | bool | `true` | Whether or not pipeline outputs should be exported to the central repo. This flag does not turn off APDB writes or alert generation; those must be handled at the pipeline level or by setting up an alternative destination. |
| debug.monitorDaxApdb | bool | `false` | Whether `dax_apdb` should run in debug mode and log metrics. |
| fullnameOverride | string | `"prompt-keda"` | Override the full name for resources (includes the release name) |
| iers_cache | string | `""` | The URI where IERS data has been pre-downloaded and cached for use by Prompt Processing. If empty, Prompt Processing does not try to update IERS data. |
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
| instrument.centralRepo | string | None, must be set | URI to the shared repo used for pipeline inputs and outputs. If `registry.centralRepoFile` is set, this URI points to a local redirect instead of the central repo itself. |
| instrument.exportTypes | string | `"- .*"` | Dataset types to export. |
| instrument.name | string | None, must be set | The "short" name of the instrument |
| instrument.pipelines.main | string | None, must be set | YAML-formatted config describing which pipeline(s) should be run for which visits' raws. Fields are still in flux; see [the source code](https://github.com/lsst-dm/prompt_processing/blob/main/python/activator/config.py) for examples. |
| instrument.pipelines.preprocessing | string | None, must be set | YAML-formatted config describing which pipeline(s) should be run before which visits' raw arrival. |
| instrument.preloadPadding | int | `30` | Number of arcseconds to pad the spatial region in preloading. |
| instrument.readRepo | string | Matches `centralRepo` | Optional URI to a separate repo used for pipeline inputs. If `registry.centralRepoFile` is set, this URI points to a local redirect instead of the central repo itself. |
| instrument.repoWait | int | `30` | The average time to wait (in seconds) before retrying a failed connection to the shared repo. |
| instrument.skymap | string | `""` | Skymap to use with the instrument |
| keda.failedJobsHistoryLimit | int | `25` | How many failed jobs should be kept available in Kubernetes. |
| keda.maxReplicaCount | int | `10` | Maximum number of replicas to scale to. |
| keda.minReplicaCount | int | `3` | Minimum number of replicas to start with. |
| keda.pollingInterval | int | `2` | Polling interval for Keda to poll scalar for scaling determination. |
| keda.redisStreams.activationLagCount | string | `"1"` | Lag count at which scaler triggers |
| keda.redisStreams.consumerGroup | string | `""` | Redis Consumer Group name |
| keda.redisStreams.expiration | int | `3600` | Maximum message age to process, in seconds. |
| keda.redisStreams.host | string | `""` | Address of Redis Streams Cluster |
| keda.redisStreams.lagCount | string | `"1"` | Number of lagging entries in the consumer group, alternative to pendingEntriesCount scaler trigger |
| keda.redisStreams.msgListenTimeout | int | `900` | Time to wait for fanned out messages before spawning new pod. |
| keda.redisStreams.pendingEntriesCount | string | `"1"` | Number of entries in the Pending Entries List for the specified consumer group in the Redis Stream |
| keda.redisStreams.retry | int | `30` | The time to wait (in seconds) before retrying a stream connection failure. |
| keda.redisStreams.streamName | string | `""` | Name of Redis Stream |
| keda.scalingStrategy | string | `"eager"` | Scaling algorithm |
| keda.successfulJobsHistoryLimit | int | `25` | How many completed jobs should be kept available in Kubernetes. |
| logLevel | string | log prompt_processing at DEBUG, other LSST code at INFO, and third-party code at WARNING. | Requested logging levels in the format of [Middleware's \-\-log-level argument](https://pipelines.lsst.io/v/daily/modules/lsst.daf.butler/scripts/butler.html#cmdoption-butler-log-level). |
| mpSky_service | string | `""` | The URI to the MPSky ephemerides service. Empty value is allowed, but its handling is undefined. |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selection rules for the Prompt Porcessing pod |
| podAnnotations | object | `{"prometheus.io/port":"8000","prometheus.io/scrape":"true"}` | Pod annotations for the Prompt Processing Pod |
| raw_microservice | string | `""` | The URI to a microservice that maps image metadata to a file location. If empty, Prompt Processing does not use a microservice. |
| registry.centralRepoFile | bool | `false` | If set, this application's Vault secret must contain a `central_repo_file` key containing a remote Butler configuration, and `instrument.centralRepo` is the local path where this file is mounted. If `instrument.readRepo` is also set, the secret must contain a `read_repo_file` key. |
| resources | object | See `values.yaml` | Kubernetes resource requests and limits |
| s3.auth_env | bool | `false` | If set, define environment variables with S3 credentials from this application's Vault secret. |
| s3.aws_profile | string | `""` | If set, specify a S3 credential profile and `cred_file_auth` must be true. If empty and `auth_env`=`false`, the `default` profile is used. |
| s3.checksum | string | `"WHEN_REQUIRED"` | If set, configure S3 checksum options. |
| s3.cred_file_auth | bool | `true` | If set, get a S3 credential file from this application's Vault secret. Must be true if `aws_profile` is set. |
| s3.disableBucketValidation | int | `0` | Set this to disable validation of S3 bucket names, allowing Ceph multi-tenant colon-separated names to be used. |
| s3.endpointUrl | string | None, must be set | S3 endpoint containing `imageBucket` |
| s3.imageBucket | string | None, must be set | Bucket containing the incoming raw images |
| sasquatch.auth_env | bool | `true` | If set, this application's Vault secret must contain a `sasquatch_token` key containing the authentication token for `sasquatch.endpointUrl`. Leave unset to attempt anonymous access. |
| sasquatch.endpointUrl | string | `""` | Url of the Sasquatch proxy server to upload metrics to. Leave blank to disable upload. This is a preliminary implementation of Sasquatch support, and this parameter may be deprecated if we instead support `SasquatchDatastore` in the future. |
| sasquatch.namespace | string | `"lsst.prompt"` | Namespace in the Sasquatch system with which to associate metrics. |
| tolerations | list | `[]` | Tolerations for the Prompt Processing pod |
| worker.grace_period | int | `45` | When Kubernetes shuts down a pod, the time its workers have to abort processing and save intermediate results (seconds). |
| worker.restart | int | `0` | The number of requests to process before rebooting a worker. If 0, workers process requests indefinitely. |
