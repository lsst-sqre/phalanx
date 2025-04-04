# next-visit-fan-out-keda

Temporary application for processing next visit events with keda.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the next-visit-fan-out deployment pod |
| debug | bool | `false` | If set, enable debug logging. |
| detectorConfig | object | See `values.yaml`. | A mapping, for each instrument, of detector number to whether that detector is "active" (i.e., producing images). |
| fullnameOverride | string | `""` |  |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"us-central1-docker.pkg.dev/prompt-proto/prompt/nextvisit-fanout"` |  |
| image.tag | string | `""` |  |
| instruments | string | None, must be set. | The instruments that are initialized when the fan-out service starts up as a space-delimited string. This list is a subset of the keys of `detectorConfig` because the latter handles some special cases. |
| kafka.expiration | float | `3600` | Maximum message age to consider, in seconds. |
| kafka.offset | string | `"latest"` |  |
| kafka.saslMechamism | string | `"SCRAM-SHA-512"` |  |
| kafka.securityProtocol | string | `"SASL_PLAINTEXT"` |  |
| keda.redisHealthCheckInterval | int | `3` | Redis health check interval in seconds. |
| keda.redisHost | string | See `values.yaml`. | Redis cluster host. |
| keda.redisRetryCount | int | `3` | Redis max retry count |
| keda.redisRetryDelayCap | int | `5` | Maximum delay time for Redis retries in seconds. |
| keda.redisRetryInitialDelay | int | `1` | Initial delay for first Redis retry in seconds. |
| keda.redisStreams | object | See `values.yaml`. | A mapping of instrument to that instrument's Keda Scaled Job. |
| knative.maxMessages | string | None, must be set. | The maximum number of messages that can be forwarded to all Knative instances combined. |
| knative.retryRequests | bool | `true` | Whether or not to retry requests that returned a suitable response. |
| knative.urls | object | See `values.yaml`. | A mapping of instrument to that instrument's Knative service. |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` | Node selection rules for the next-visit-fan-out deployment pod |
| platform | string | `"keda"` | Platform to submit events to.  Either knative or keda. |
| podAnnotations."prometheus.io/port" | string | `"8000"` |  |
| podAnnotations."prometheus.io/scrape" | string | `"true"` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` | Resource limits and requests for the next-visit-fan-out deployment pod |
| tolerations | list | `[]` | Tolerations for the next-visit-fan-out deployment pod |
