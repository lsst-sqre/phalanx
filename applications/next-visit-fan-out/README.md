# next-visit-fan-out

A Helm chart for Kubernetes

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| detectorConfigFile | string | `"detector.yaml"` |  |
| fullnameOverride | string | `""` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"us-central1-docker.pkg.dev/prompt-proto/prompt/nextvisit-fanout"` |  |
| image.tag | string | `""` |  |
| imagePullSecrets[0].name | string | `"regcred"` |  |
| kafka.offset | string | `"latest"` |  |
| kafka.saslMechamism | string | `"SCRAM-SHA-512"` |  |
| kafka.securityProtocol | string | `"SASL_PLAINTEXT"` |  |
| knative.hscUrl | string | `"http://prompt-proto-service.prompt-proto-service/next-visit"` |  |
| knative.latissUrl | string | `"http://prompt-proto-service.prompt-proto-service/next-visit"` |  |
| knative.lsstcamUrl | string | `"http://prompt-proto-service.prompt-proto-service/next-visit"` |  |
| knative.lsstcomcamUrl | string | `"http://prompt-proto-service.prompt-proto-service/next-visit"` |  |
| nameOverride | string | `""` |  |
| namespace | string | `"next-visit-fan-out"` |  |
| podAnnotations."prometheus.io/port" | string | `"8000"` |  |
| podAnnotations."prometheus.io/scrape" | string | `"true"` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
