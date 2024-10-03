# butler

Server for Butler data abstraction service

## Source Code

* <https://github.com/lsst/daf_butler>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the butler deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of butler deployment |
| autoscaling.maxReplicas | int | `100` | Maximum number of butler deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of butler deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of butler deployment pods |
| config.additionalS3ProfileName | string | No second S3 profile is available. | Profile name identifying a second S3 endpoint and set of credentials to use for accessing files in the datastore. |
| config.dp02ClientServerIsDefault | bool | `false` | True if the 'dp02' Butler repository alias should use client/server Butler.  False if it should use DirectButler. |
| config.dp02PostgresUri | string | No configuration file for DP02 will be generated. | Postgres connection string pointing to the registry database hosting Data Preview 0.2 data. |
| config.pathPrefix | string | `"/api/butler"` | The prefix of the path portion of the URL where the Butler service will be exposed.  For example, if the service should be exposed at `https://data.lsst.cloud/api/butler`, this should be set to `/api/butler` |
| config.pguser | string | Use values specified in per-repository Butler config files. | Postgres username used to connect to the Butler DB |
| config.repositories | object | `{}` | Mapping from Butler repository label to Butler configuration URI for repositories which will be hosted by this server. |
| config.s3EndpointUrl | string | `""` | URL for the S3 service where files for datasets are stored by Butler. |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the butler image |
| image.repository | string | `"ghcr.io/lsst/daf_butler"` | Image to use in the butler deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the butler deployment pod |
| podAnnotations | object | `{}` | Annotations for the butler deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | see `values.yaml` | Resource limits and requests for the butler deployment pod |
| tolerations | list | `[]` | Tolerations for the butler deployment pod |
