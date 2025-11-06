# butler-writer-service

Write proxy for the Butler that buffers concurrent requests.

## Source Code

* <https://github.com/lsst-dm/prompt_processing_butler_writer>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the pod |
| fullnameOverride | string | `""` |  |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | When to download an image. `IfNotPresent` uses a cached image if possible, and is the best choice for stable releases. `Always` checks for the latest tag online, and is needed for development builds. |
| image.repository | string | `"ghcr.io/lsst-dm/prompt_processing_butler_writer"` | Image to use for the Butler writer service |
| image.tag | string | None, must be set | Docker container version to use for the Butler writer service |
| kafka.clusterAddress | string | None, must be set | Address of Kafka broker containing Prompt Processing output events, for consumption by the Butler writer service. |
| kafka.topic | string | None, must be set | Kafka topic containing Prompt Processing output events, for consumption by the Butler writer service. |
| kafka.username | string | None, must be set | Username for Kafka broker containing Prompt Processing output events, for consumption by the Butler writer service. |
| logLevel | string | `"INFO"` | Global logging level to use in the writer service. |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` | Node selection rules for the pod |
| outputRepo | string | None, must be set | URI to the repo the writer should write to. |
| podAnnotations | object | `{}` | Pod annotations for the writer |
| resources.cpuLimit | int | `1` | The maximum cpu cores for the Butler writer service. |
| resources.cpuRequest | float | `0.25` | The cpu cores requested for the Butler writer service. |
| resources.memoryLimit | string | `"1Gi"` | The maximum memory limit for the Butler writer service. |
| resources.memoryRequest | string | `"0.5Gi"` | The minimum memory to request for the Butler writer service. |
| s3.aws_profile | string | `""` | If set, specify a S3 credential profile from the credential file. If empty, the `default` profile is used. |
| s3.checksum | string | `"WHEN_REQUIRED"` | If set, configure S3 checksum options. |
| s3.endpointUrl | string | None, must be set | S3 endpoint where datasets are buffered. |
| tolerations | list | `[]` | Tolerations for the pod |
