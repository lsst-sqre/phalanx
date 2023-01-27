# exposurelog

Log messages related to an exposure

## Source Code

* <https://github.com/lsst-sqre/exposurelog>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the exposurelog pod |
| autoscaling | object | `{"enabled":false,"maxReplicas":100,"minReplicas":1,"targetCPUUtilizationPercentage":80,"targetMemoryUtilizationPercentage":80}` | Exposurelog autoscaling settings |
| autoscaling.enabled | bool | false | enable exposurelog autoscaling |
| autoscaling.maxReplicas | int | `100` | maximum number of exposurelog replicas |
| autoscaling.minReplicas | int | `1` | minimum number of exposurelog replicas |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization for exposurelog pod autoscale calculations |
| autoscaling.targetMemoryUtilizationPercentage | int | `80` | Target memory utilization for exposurelog pod autoscale calculations |
| config | object | `{"butler_uri_1":"","butler_uri_2":"","nfs_path_1":"","nfs_path_2":"","nfs_server_1":"","nfs_server_2":"","site_id":""}` | Application-specific configuration |
| config.butler_uri_1 | string | `""` | URI for butler registry 1 (required).  Format: * For a volume mounted using `nfs_path_1` (see above):   An absolute path starting with `/volume_1/`. * For a network URI: see the daf_butler documentation. * For a sandbox deployment: specify `LSSTCam` for butler_uri_1. |
| config.butler_uri_2 | string | `""` | URI for butler registry 2 (optional).  Format: * For a volume mounted using `nfs_path_2` (see above):   An absolute path starting with `/volume_2/`. * For a network URI: see the daf_butler documentation. * For a sandbox deployment: specify `LATISS` for butler_uri_2. |
| config.nfs_path_1 | string | `""` | NFS path to butler registry 1 Only specify a non-blank value if reading the registry from an NFS-mounted file. If not blank then mount the specified NFS path as internal volume /volume1 |
| config.nfs_path_2 | string | `""` | NFS path to butler registry 2 Only specify a non-blank value if reading the registry from an NFS-mounted file. If not blank then mount the specified NFS path as internal volume /volume2 |
| config.nfs_server_1 | string | `""` | Name of the NFS server that exports nfs_path_1 Specify a non-blank value if and only if the corresponding nfs_path_1 is not blank. |
| config.nfs_server_2 | string | `""` | Name of the NFS server that exports nfs_path_2 Specify a non-blank value if and only if the corresponding nfs_path_1 is not blank. |
| config.site_id | string | `""` | Site ID; a non-empty string of up to 16 characters. This should be different for each non-sandbox deployment. Sandboxes should use `test`. |
| db.database | string | `"exposurelog"` | database name |
| db.host | string | `"postgres.postgres"` | database host |
| db.port | int | `5432` | database port |
| db.user | string | `"exposurelog"` | database user |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"Always"` | Pull policy for the exposurelog image |
| image.repository | string | `"lsstsqre/exposurelog"` | exposurelog image to use |
| image.tag | string | The appVersion of the chart | Tag of exposure image to use |
| ingress.gafaelfawrAuthQuery | string | `""` | Gafaelfawr auth query string |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the exposurelog pod |
| podAnnotations | object | `{}` | Annotations for the exposurelog pod |
| podSecurityContext | object | `{}` | Security context for the exposurelog pod |
| replicaCount | int | `1` | How many exposurelog pods to run |
| resources | object | `{}` | Resource limits and requests for the exposurelog pod |
| securityContext | object | `{}` | Security context for the exposurelog deployment |
| tolerations | list | `[]` | Tolerations for the exposurelog pod |
