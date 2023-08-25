# prompt-processing-hsc

Deployment for prompt proto service for HSC images

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| file://../../charts/prompt-proto-service | prompt-proto-service | 1.0.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| prompt-proto-service.apdb.db | string | `"lsst-devl"` |  |
| prompt-proto-service.apdb.ip | string | `"usdf-prompt-processing-dev.slac.stanford.edu:5432"` |  |
| prompt-proto-service.apdb.namespace | string | `"pp_apdb"` |  |
| prompt-proto-service.apdb.user | string | `"rubin"` |  |
| prompt-proto-service.image.pullPolicy | string | `"IfNotPresent"` |  |
| prompt-proto-service.image.repository | string | `"ghcr.io/lsst-dm/prompt-proto-service"` |  |
| prompt-proto-service.image.tag | string | `"latest"` |  |
| prompt-proto-service.imageNotifications.imageTimeout | string | `"120"` |  |
| prompt-proto-service.imageNotifications.kafkaClusterAddress | string | `"prompt-processing-kafka-bootstrap.kafka:9092"` |  |
| prompt-proto-service.imageNotifications.topic | string | `"rubin-prompt-processing"` |  |
| prompt-proto-service.instrument.calibRepo | string | `"s3://rubin:rubin-pp-users/central_repo/"` |  |
| prompt-proto-service.instrument.name | string | `"HSC"` |  |
| prompt-proto-service.instrument.pipelines | string | `"(survey=\"SURVEY\")=[${PROMPT_PROTOTYPE_DIR}/pipelines/${RUBIN_INSTRUMENT}/ApPipe.yaml]"` |  |
| prompt-proto-service.instrument.skymap | string | `"hsc_rings_v1"` |  |
| prompt-proto-service.knative.ephemeralStorageLimit | string | `"20Gi"` |  |
| prompt-proto-service.knative.ephemeralStorageRequest | string | `"8Gi"` |  |
| prompt-proto-service.knative.idleTimeout | int | `900` |  |
| prompt-proto-service.knative.maxScale | int | `100` |  |
| prompt-proto-service.knative.minScale | int | `3` |  |
| prompt-proto-service.knative.responseStartTimeout | int | `900` |  |
| prompt-proto-service.knative.timeout | int | `900` |  |
| prompt-proto-service.podAnnotations | object | `{"autoscaling.knative.dev/max-scale":"100","autoscaling.knative.dev/min-scale":"3","autoscaling.knative.dev/target-burst-capacity":"-1","autoscaling.knative.dev/target-utilization-percentage":"60","revision":"1"}` | Annotations for the prompt-proto-service pod |
| prompt-proto-service.registry.db | string | `"ppcentralbutler"` |  |
| prompt-proto-service.registry.ip | string | `"usdf-prompt-processing-dev.slac.stanford.edu:5432"` |  |
| prompt-proto-service.registry.user | string | `"pp"` |  |
| prompt-proto-service.s3.auth_env | bool | `true` |  |
| prompt-proto-service.s3.disableBucketValidation | string | `"1"` |  |
| prompt-proto-service.s3.endpointUrl | string | `"https://s3dfrgw.slac.stanford.edu"` |  |
| prompt-proto-service.s3.imageBucket | string | `"rubin:rubin-pp"` |  |
| prompt-proto-service.vaultSecretsPath | string | `"secret/rubin/usdf-prompt-processing-dev/prompt-proto-service-hsc"` |  |

