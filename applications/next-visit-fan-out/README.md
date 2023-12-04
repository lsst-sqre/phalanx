# next-visit-fan-out

Poll next visit events from Kafka, duplicate them, and send them to all applications that need to receive them.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the next-visit-fan-out deployment pod |
| detectorConfigFile | string | `"detector.yaml"` |  |
| fullnameOverride | string | `""` |  |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"us-central1-docker.pkg.dev/prompt-proto/prompt/nextvisit-fanout"` |  |
| image.tag | string | `""` |  |
| kafka.offset | string | `"latest"` |  |
| kafka.saslMechamism | string | `"SCRAM-SHA-512"` |  |
| kafka.securityProtocol | string | `"SASL_PLAINTEXT"` |  |
| knative.hscUrl | string | `"http://prompt-proto-service.prompt-proto-service-hsc/next-visit"` |  |
| knative.latissUrl | string | `"http://prompt-proto-service.prompt-proto-service-latiss/next-visit"` |  |
| knative.lsstcamUrl | string | `"http://prompt-proto-service.prompt-proto-service-lsstcam/next-visit"` |  |
| knative.lsstcomcamUrl | string | `"http://prompt-proto-service.prompt-proto-service-lsstcomcam/next-visit"` |  |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` | Node selection rules for the next-visit-fan-out deployment pod |
| podAnnotations."prometheus.io/port" | string | `"8000"` |  |
| podAnnotations."prometheus.io/scrape" | string | `"true"` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` | Resource limits and requests for the next-visit-fan-out deployment pod |
| tolerations | list | `[]` | Tolerations for the next-visit-fan-out deployment pod |
