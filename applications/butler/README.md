# butler

Server for Butler data abstraction service

## Source Code

* <https://github.com/lsst/daf_butler>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the butler deployment pod |
| autoscaling.enabled | bool | `true` | Enable autoscaling of butler deployment |
| autoscaling.maxReplicas | int | `10` | Maximum number of butler deployment pods  Each replica can have 40 database connections, so we need to make sure the combined connections are under the postgres connection limit. (Which is configurable, but currently set to 400 at the IDF.) |
| autoscaling.minReplicas | int | `1` | Minimum number of butler deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `25` | Target CPU utilization of butler deployment pods  Butler CPU usage is very low in normal operation because most things are I/O bound.  CPU usage can start creeping up if we have many queries running simultaneously (due to serialization overhead and spatial postprocessing.) In this case the thread pool and database connection pool are probably oversubscribed long before we hit 100% cpu usage, so we want to get more replicas up at fairly low CPU usage. |
| config.additionalS3EndpointUrls | object | No additional URLs | Endpoint URLs for additional S3 services used by the Butler, as a mapping from profile name to URL. |
| config.dp02ClientServerIsDefault | bool | `false` | True if the 'dp02' Butler repository alias should use client/server Butler.  False if it should use DirectButler. |
| config.dp02PostgresUri | string | No configuration file for DP02 will be generated. | Postgres connection string pointing to the registry database hosting Data Preview 0.2 data. |
| config.dp1PostgresUri | string | No configuration file for DP1 will be generated. | Postgres connection string pointing to the registry database hosting Data Preview 1 data. |
| config.pathPrefix | string | `"/api/butler"` | The prefix of the path portion of the URL where the Butler service will be exposed.  For example, if the service should be exposed at `https://data.lsst.cloud/api/butler`, this should be set to `/api/butler` |
| config.pguser | string | Use values specified in per-repository Butler config files. | Postgres username used to connect to the Butler DB |
| config.repositories | object | `{}` | Mapping from Butler repository label to Butler configuration URI for repositories which will be hosted by this server. |
| config.s3EndpointUrl | string | `""` | URL for the primary S3 service where files for datasets are stored by Butler. |
| config.shareNubladoSecrets | bool | `true` | If true, borrow the S3 and Postgres secrets set up in Nublado for end-users.  Otherwise, use secrets specifically set up for the Butler server. |
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
