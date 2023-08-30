# ook

Ook is the librarian service for Rubin Observatory. Ook indexes documentation content into the Algolia search engine that powers the Rubin Observatory documentation portal, www.lsst.io.

**Homepage:** <https://ook.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/ook>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| audit.affinity | object | `{}` | Affinity rules for Ook audit pods |
| audit.enabled | bool | `true` | Enable the audit job |
| audit.nodeSelector | object | `{}` | Node selection rules for Ook audit pods |
| audit.podAnnotations | object | `{}` | Annotations for Ook audit pods |
| audit.reingest | bool | `true` | Reingest missing documents |
| audit.resources | object | `{}` | Resource limits and requests for Ook audit pods |
| audit.schedule | string | `"15 2 * * *"` | Cron schedule string for ook audit job (UTC) |
| audit.tolerations | list | `[]` | Tolerations for Ook audit pods |
| audit.ttlSecondsAfterFinished | int | `86400` | Time (second) to keep a finished job before cleaning up |
| config.logLevel | string | `"INFO"` | Logging level: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" |
| config.registryUrl | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | Cluster URL for the Confluent Schema Registry |
| config.subjectCompatibility | string | `"FORWARD"` | Schema subject compatibility. |
| config.subjectSuffix | string | `""` | Schema subject suffix. Should be empty for production but can be set to a value to create unique subjects in the Confluent Schema Registry for testing. |
| config.topics.ingest | string | `"lsst.square-events.ook.ingest"` | Kafka topic name for ingest events |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"ghcr.io/lsst-sqre/ook"` | Squarebot image repository |
| image.tag | string | The appVersion of the chart | Tag of the image |
| imagePullSecrets | list | `[]` | Secret names to use for all Docker pulls |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.path | string | `"/ook"` | Path prefix where Squarebot is hosted |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` | Annotations for API and worker pods |
| replicaCount | int | `1` | Number of API pods to run |
| resources | object | `{}` |  |
| service.port | int | `80` | Port of the service to create and map to the ingress |
| service.type | string | `"ClusterIP"` | Type of service to create |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.create | bool | `true` | Specifies whether a service account should be created |
| serviceAccount.name | string | `""` |  |
| tolerations | list | `[]` |  |
