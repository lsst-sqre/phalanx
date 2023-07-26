# cadc-tap

IVOA TAP service

## Source Code

* <https://github.com/lsst-sqre/tap-postgres>
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
| fullnameOverride | string | `"cadc-tap"` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the tap image |
| image.repository | string | `"ghcr.io/lsst-sqre/tap-postgres-service"` | tap image to use |
| image.tag | string | The appVersion of the chart | Tag of tap image to use |
| ingress.anonymousAnnotations | object | `{}` | Additional annotations to use for endpoints that allow anonymous access, such as `/capabilities` and `/availability` |
| ingress.authenticatedAnnotations | object | `{}` | Additional annotations to use for endpoints that are authenticated, such as `/sync`, `/async`, and `/tables` |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the Gafaelfawr frontend pod |
| pg.database | string | `"pg12db"` | Postgres database to connect to |
| pg.host | string | `"mock-pg:5432"` (the mock pg) | Postgres hostname:port to connect to |
| pg.mock.affinity | object | `{}` | Affinity rules for the mock postgres pod |
| pg.mock.enabled | bool | `true` | Spin up a container to pretend to be postgres. |
| pg.mock.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the mock postgres image |
| pg.mock.image.repository | string | `"ghcr.io/lsst-sqre/tap-postgres-db"` | Mock postgres image to use |
| pg.mock.image.tag | string | The appVersion of the chart | Tag of mock postgres image to use |
| pg.mock.nodeSelector | object | `{}` | Node selection rules for the mock postgres pod |
| pg.mock.podAnnotations | object | `{}` | Annotations for the mock postgres pod |
| pg.mock.resources | object | `{}` | Resource limits and requests for the mock postgres pod |
| pg.mock.tolerations | list | `[]` | Tolerations for the mock postgres pod |
| pg.username | string | `"tapadm"` | Postgres username to use to connect |
| podAnnotations | object | `{}` | Annotations for the Gafaelfawr frontend pod |
| replicaCount | int | `1` | Number of pods to start |
| resources | object | `{}` | Resource limits and requests for the Gafaelfawr frontend pod |
| tapSchema.affinity | object | `{}` | Affinity rules for the mock QServ pod |
| tapSchema.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the TAP schema image |
| tapSchema.image.repository | string | `"lsstsqre/tap-schema-mock"` | TAP schema image to ue. This must be overridden by each environment with the TAP schema for that environment. |
| tapSchema.image.tag | string | `"2.0.2"` | Tag of TAP schema image |
| tapSchema.nodeSelector | object | `{}` | Node selection rules for the mock QServ pod |
| tapSchema.podAnnotations | object | `{}` | Annotations for the mock QServ pod |
| tapSchema.resources | object | `{}` | Resource limits and requests for the TAP schema database pod |
| tapSchema.tolerations | list | `[]` | Tolerations for the mock QServ pod |
| tolerations | list | `[]` | Tolerations for the Gafaelfawr frontend pod |
| uws.affinity | object | `{}` | Affinity rules for the UWS database pod |
| uws.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the UWS database image |
| uws.image.repository | string | `"ghcr.io/lsst-sqre/tap-postgres-uws"` | UWS database image to use |
| uws.image.tag | string | The appVersion of the chart | Tag of UWS database image to use |
| uws.nodeSelector | object | `{}` | Node selection rules for the UWS database pod |
| uws.podAnnotations | object | `{}` | Annotations for the UWS databse pod |
| uws.resources | object | `{}` | Resource limits and requests for the UWS database pod |
| uws.tolerations | list | `[]` | Tolerations for the UWS database pod |
| vaultSecretsPath | string | None, must be set | Path to the Vault secret (`secret/k8s_operator/<host>/tap`, for example) |
