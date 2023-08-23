# cadc-tap

![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-informational?style=flat-square) ![AppVersion: 1.4.5](https://img.shields.io/badge/AppVersion-1.4.5-informational?style=flat-square)

IVOA TAP service

## Source Code

* <https://github.com/lsst-sqre/tap-postgres>
* <https://github.com/lsst-sqre/lsst-tap-service>
* <https://github.com/opencadc/tap>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the Gafaelfawr frontend pod |
| config.datalinkPayloadUrl | string | `"https://github.com/lsst/sdm_schemas/releases/download/1.2.2/datalink-snippets.zip"` | Datalink payload URL |
| config.gafaelfawrHost | string | Value of `ingress.host` | Gafaelfawr hostname to get user information from a token |
| config.gcsBucket | string | None, must be set | Name of GCS bucket in which to store results |
| config.gcsBucketType | string | GCS | GCS bucket type (GCS or S3) |
| config.gcsBucketUrl | string | None, must be set | Base URL for results stored in GCS bucket |
| config.jvmMaxHeapSize | string | `"4G"` | Java heap size, which will set the maximum size of the heap. Otherwise Java would determine it based on how much memory is available and black maths. |
| config.tapSchemaAddress | string | `"cadc-tap-schema-db:3306"` | Address to a MySQL database containing TAP schema data |
| config.vaultSecretName | string | `""` | Vault secret name, this is appended to the global path to find the vault secrets associated with this deployment. |
| fullnameOverride | string | `"cadc-tap"` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the tap image |
| image.repository | string | `"ghcr.io/lsst-sqre/lsst-tap-service"` | tap image to use |
| image.tag | string | The appVersion of the chart | Tag of tap image to use |
| ingress.anonymousAnnotations | object | `{}` | Additional annotations to use for endpoints that allow anonymous access, such as `/capabilities` and `/availability` |
| ingress.authenticatedAnnotations | object | `{}` | Additional annotations to use for endpoints that are authenticated, such as `/sync`, `/async`, and `/tables` |
| ingress.path | string | `""` | External path to the tap service, the path eventually gets rewritten by tomcat. |
| mockdb.affinity | object | `{}` | Affinity rules for the mock db pod |
| mockdb.enabled | bool | `true` | Spin up a container to pretend to be the database. |
| mockdb.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the mock database image |
| mockdb.image.repository | string | `"ghcr.io/lsst-sqre/lsst-tap-mock-qserv"` | Mock database image to use |
| mockdb.image.tag | string | The appVersion of the chart | Tag of mock db image to use |
| mockdb.nodeSelector | object | `{}` | Node selection rules for the mock db pod |
| mockdb.podAnnotations | object | `{}` | Annotations for the mock db pod |
| mockdb.port | int | `3306` | Port to connect to the mock-db on |
| mockdb.resources | object | `{}` | Resource limits and requests for the mock db pod |
| mockdb.tolerations | list | `[]` | Tolerations for the mock db pod |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the Gafaelfawr frontend pod |
| podAnnotations | object | `{}` | Annotations for the Gafaelfawr frontend pod |
| qserv.host | string | `"mock-qserv:3306"` (the mock QServ) | QServ hostname:port to connect to |
| replicaCount | int | `1` | Number of pods to start |
| resources | object | `{}` | Resource limits and requests for the Gafaelfawr frontend pod |
| tapSchema.affinity | object | `{}` | Affinity rules for the TAP schema database pod |
| tapSchema.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the TAP schema image |
| tapSchema.image.repository | string | `"lsstsqre/tap-schema-mock"` | TAP schema image to ue. This must be overridden by each environment with the TAP schema for that environment. |
| tapSchema.image.tag | string | `"2.0.2"` | Tag of TAP schema image |
| tapSchema.nodeSelector | object | `{}` | Node selection rules for the TAP schema database pod |
| tapSchema.podAnnotations | object | `{}` | Annotations for the TAP schema database pod |
| tapSchema.resources | object | `{}` | Resource limits and requests for the TAP schema database pod |
| tapSchema.tolerations | list | `[]` | Tolerations for the TAP schema database pod |
| tolerations | list | `[]` | Tolerations for the Gafaelfawr frontend pod |
| uws.affinity | object | `{}` | Affinity rules for the UWS database pod |
| uws.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the UWS database image |
| uws.image.repository | string | `"ghcr.io/lsst-sqre/lsst-tap-uws-db"` | UWS database image to use |
| uws.image.tag | string | The appVersion of the chart | Tag of UWS database image to use |
| uws.nodeSelector | object | `{}` | Node selection rules for the UWS database pod |
| uws.podAnnotations | object | `{}` | Annotations for the UWS databse pod |
| uws.resources | object | `{}` | Resource limits and requests for the UWS database pod |
| uws.tolerations | list | `[]` | Tolerations for the UWS database pod |
| vaultSecretsPath | string | None, must be set | Path to the Vault secret (`secret/k8s_operator/<host>/tap`, for example) |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.11.0](https://github.com/norwoodj/helm-docs/releases/v1.11.0)
