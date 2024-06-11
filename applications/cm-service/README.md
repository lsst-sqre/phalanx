# cm-service

Campaign Management for Rubin Data Release Production

## Source Code

* <https://github.com/lsst-dm/cm-service>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the cm-service deployment pod |
| config.databaseEcho | bool | `false` | Whether to echo SQLAlchemy generated SQL to the log |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.outputVolume.storage | string | `"1Gi"` | Minimum storage requested in service output area PVC |
| config.outputVolume.storageClassName | string | `nil` | If specified, name of storage class requested in service output area PVC |
| config.outputVolume.subPath | string | `nil` | If specified, sub-path within bound PV to be mounted at service output area |
| config.pathPrefix | string | `"/cm-service/v1"` | URL path prefix |
| config.workerImage | string | `"ghcr.io/lsst-dm/cm-service-worker"` | Image tag for utility stack container |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the cm-service image |
| image.repository | string | `"ghcr.io/lsst-dm/cm-service"` | Image to use in the cm-service deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the cm-service deployment pod |
| podAnnotations | object | `{}` | Annotations for the cm-service deployment pod |
| redis.config.secretKey | string | `"password"` |  |
| redis.config.secretName | string | `"redis-secret"` |  |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the cm-service deployment pod |
| tolerations | list | `[]` | Tolerations for the cm-service deployment pod |
