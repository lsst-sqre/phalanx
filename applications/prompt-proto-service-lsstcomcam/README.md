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
| prompt-proto-service.apdb.namespace | string | `"pp_apdb_lsstcomcam"` | Database namespace for the APDB |
| prompt-proto-service.apdb.url | string | None, must be set | URL to the APDB, in any form recognized by SQLAlchemy |
| prompt-proto-service.image.pullPolicy | string | `IfNotPresent` in prod, `Always` in dev | Pull policy for the PP image |
| prompt-proto-service.image.repository | string | `"ghcr.io/lsst-dm/prompt-service"` | Image to use in the PP deployment |
| prompt-proto-service.image.tag | string | `"latest"` | Overrides the image tag whose default is the chart appVersion. |
| prompt-proto-service.imageNotifications.imageTimeout | string | `"20"` | Timeout to wait after expected script completion for raw image arrival (seconds). |
| prompt-proto-service.imageNotifications.kafkaClusterAddress | string | None, must be set | Hostname and port of the Kafka provider |
| prompt-proto-service.imageNotifications.topic | string | None, must be set | Topic where raw image arrival notifications appear |
| prompt-proto-service.instrument.calibRepo | string | None, must be set | URI to the shared repo used for calibrations, templates, and pipeline outputs. If `registry.centralRepoFile` is set, this URI points to a local redirect instead of the central repo itself. |
| prompt-proto-service.instrument.calibRepoPguser | string | None, must be set | Postgres username to access the shared butler repo for calibrations, templates, and pipeline outputs. If `registry.centralRepoFile` is set, a local redirect is used and its config may override this config. |
| prompt-proto-service.instrument.name | string | `""` | The "short" name of the instrument |
| prompt-proto-service.instrument.pipelines | string | None, must be set | Machine-readable string describing which pipeline(s) should be run for which visits. Notation is complex and still in flux; see [the source code](https://github.com/lsst-dm/prompt_processing/blob/main/python/activator/config.py) for examples. |
| prompt-proto-service.instrument.skymap | string | `""` | Skymap to use with the instrument |
| prompt-proto-service.knative.cpuLimit | string | `"1"` | The maximum cpu cores. |
| prompt-proto-service.knative.cpuRequest | string | `"1"` | The cpu cores requested. |
| prompt-proto-service.knative.ephemeralStorageLimit | string | `"20Gi"` | The maximum storage space allowed for each container (mostly local Butler). |
| prompt-proto-service.knative.ephemeralStorageRequest | string | `"20Gi"` | The storage space reserved for each container (mostly local Butler). |
| prompt-proto-service.knative.gpu | bool | `false` | GPUs enabled. |
| prompt-proto-service.knative.gpuRequest | string | `"0"` | The number of GPUs to request. |
| prompt-proto-service.knative.idleTimeout | int | `900` | Maximum time that a container can send nothing to the fanout service (seconds). |
| prompt-proto-service.knative.memoryLimit | string | `"8Gi"` | The maximum memory limit. |
| prompt-proto-service.knative.memoryRequest | string | `"2Gi"` | The minimum memory to request. |
| prompt-proto-service.knative.responseStartTimeout | int | `900` | Maximum time that a container can send nothing to the fanout service after initial submission (seconds). |
| prompt-proto-service.knative.timeout | int | `900` | Maximum time that a container can respond to a next_visit request (seconds). |
| prompt-proto-service.logLevel | string | log prompt_processing at DEBUG, other LSST code at INFO, and third-party code at WARNING. | Requested logging levels in the format of [Middleware's \-\-log-level argument](https://pipelines.lsst.io/v/daily/modules/lsst.daf.butler/scripts/butler.html#cmdoption-butler-log-level). |
| prompt-proto-service.podAnnotations | object | See the `values.yaml` file. | Annotations for the prompt-proto-service pod |
| prompt-proto-service.registry.centralRepoFile | bool | `false` | If set, this application's Vault secret must contain a `central_repo_file` key containing a remote Butler configuration, and `instrument.calibRepo` is the local path where this file is mounted. |
| prompt-proto-service.s3.auth_env | bool | `true` | If set, get S3 credentials from this application's Vault secret. |
| prompt-proto-service.s3.disableBucketValidation | string | `"0"` | Set this to disable validation of S3 bucket names, allowing Ceph multi-tenant colon-separated names to be used. |
| prompt-proto-service.s3.endpointUrl | string | None, must be set | S3 endpoint containing `imageBucket` |
| prompt-proto-service.s3.imageBucket | string | None, must be set | Bucket containing the incoming raw images |
| prompt-proto-service.sasquatch.auth_env | bool | `true` | If set, this application's Vault secret must contain a `sasquatch_token` key containing the authentication token for `sasquatch.endpointUrl`. Leave unset to attempt anonymous access. |
| prompt-proto-service.sasquatch.endpointUrl | string | `""` | Url of the Sasquatch proxy server to upload metrics to. Leave blank to disable upload. This is a preliminary implementation of Sasquatch support, and this parameter may be deprecated if we instead support `SasquatchDatastore` in the future. |
| prompt-proto-service.sasquatch.namespace | string | `"lsst.prompt"` | Namespace in the Sasquatch system with which to associate metrics. |
