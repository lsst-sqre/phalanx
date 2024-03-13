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
| apdb.namespace | string | None, must be set | Database namespace for the APDB |
| apdb.url | string | None, must be set | URL to the APDB, in any form recognized by SQLAlchemy |
| cacheCalibs | bool | `true` | Whether or not calibs should be cached between runs of a pod. This is a temporary flag that should only be unset in specific circumstances, and only in the development environment. |
| containerConcurrency | int | `1` | The number of Knative requests that can be handled simultaneously by one container |
| fullnameOverride | string | `"prompt-proto-service"` | Override the full name for resources (includes the release name) |
| image.pullPolicy | string | `IfNotPresent` in prod, `Always` in dev | Pull policy for the PP image |
| image.repository | string | `"ghcr.io/lsst-dm/prompt-service"` | Image to use in the PP deployment |
| image.tag | string | `"latest"` | Overrides the image tag whose default is the chart appVersion. |
| imageNotifications.imageTimeout | string | `"20"` | Timeout to wait after expected script completion for raw image arrival (seconds). |
| imageNotifications.kafkaClusterAddress | string | None, must be set | Hostname and port of the Kafka provider |
| imageNotifications.topic | string | None, must be set | Topic where raw image arrival notifications appear |
| imagePullSecrets | list | `[]` |  |
| instrument.calibRepo | string | None, must be set | URI to the shared repo used for calibrations, templates, and pipeline outputs. If `registry.centralRepoFile` is set, this URI points to a local redirect instead of the central repo itself. |
| instrument.name | string | None, must be set | The "short" name of the instrument |
| instrument.pipelines | string | None, must be set | Machine-readable string describing which pipeline(s) should be run for which visits. Notation is complex and still in flux; see [the source code](https://github.com/lsst-dm/prompt_processing/blob/main/python/activator/config.py) for examples. |
| instrument.skymap | string | `""` | Skymap to use with the instrument |
| knative.cpuLimit | string | `"1"` | The maximum cpu cores. |
| knative.cpuRequest | string | `"1"` | The cpu cores requested. |
| knative.ephemeralStorageLimit | string | `"20Gi"` | The maximum storage space allowed for each container (mostly local Butler). |
| knative.ephemeralStorageRequest | string | `"20Gi"` | The storage space reserved for each container (mostly local Butler). |
| knative.gpu | bool | `false` | GPUs enabled. |
| knative.gpuRequest | string | `"0"` | The number of GPUs to request. |
| knative.idleTimeout | int | `900` | Maximum time that a container can send nothing to the fanout service (seconds). |
| knative.memoryLimit | string | `"8Gi"` | The maximum memory limit. |
| knative.memoryRequest | string | `"2Gi"` | The minimum memory to request. |
| knative.responseStartTimeout | int | `900` | Maximum time that a container can send nothing to the fanout service after initial submission (seconds). |
| knative.timeout | int | `900` | Maximum time that a container can respond to a next_visit request (seconds). |
| logLevel | string | log prompt_processing at DEBUG, other LSST code at INFO, and third-party code at WARNING. | Requested logging levels in the format of [Middleware's \-\-log-level argument](https://pipelines.lsst.io/v/daily/modules/lsst.daf.butler/scripts/butler.html#cmdoption-butler-log-level). |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | See the `values.yaml` file. | Annotations for the prompt-proto-service pod |
| registry.centralRepoFile | bool | `false` | If set, this application's Vault secret must contain a `central_repo_file` key containing a remote Butler configuration, and `instrument.calibRepo` is the local path where this file is mounted. |
| s3.auth_env | bool | `true` | If set, get S3 credentials from this application's Vault secret. |
| s3.disableBucketValidation | string | `"0"` | Set this to disable validation of S3 bucket names, allowing Ceph multi-tenant colon-separated names to be used. |
| s3.endpointUrl | string | None, must be set | S3 endpoint containing `imageBucket` |
| s3.imageBucket | string | None, must be set | Bucket containing the incoming raw images |
| sasquatch.auth_env | bool | `true` | If set, this application's Vault secret must contain a `sasquatch_token` key containing the authentication token for `sasquatch.endpointUrl`. Leave unset to attempt anonymous access. |
| sasquatch.endpointUrl | string | `""` | Url of the Sasquatch proxy server to upload metrics to. Leave blank to disable upload. This is a preliminary implementation of Sasquatch support, and this parameter may be deprecated if we instead support `SasquatchDatastore` in the future. |
| tolerations | list | `[]` |  |
