# alert-stream-schema-registry

Confluent Schema Registry for managing schema versions for the Alert Stream

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| clusterName | string | `"alert-broker"` | Strimzi "cluster name" of the broker to use as a backend. |
| compatibilityLevel | string | `"None"` |  |
| hostname | string | `"usdf-alert-schemas-dev.slac.stanford.edu"` | Hostname for an ingress which sends traffic to the Schema Registry. |
| name | string | `"alert-schema-registry"` | Name used by the registry, and by its users. |
| port | int | `8081` | Port where the registry is listening. NOTE: Not actually configurable in strimzi-registry-operator, so this basically cannot be changed. |
| schemaSync | object | `{"image":{"digest":"sha256:f7d31cbb66621000921ae8894c316f9172026e1d2decabde06b09954bd3c4acb","pullPolicy":"Always","repository":"lsstdm/lsst_alert_packet"},"subject":"alert-packet"}` | Configuration for the Job which injects the most recent alert_packet schema into the Schema Registry |
| schemaSync.image.digest | string | `"sha256:f7d31cbb66621000921ae8894c316f9172026e1d2decabde06b09954bd3c4acb"` | Version of the container to use. If container isn't updating in Argo, switch to digest. tag: tickets-DM-42606 |
| schemaSync.image.repository | string | `"lsstdm/lsst_alert_packet"` | Repository of a container which has the alert_packet syncLatestSchemaToRegistry.py program. |
| schemaSync.subject | string | `"alert-packet"` | Subject name to use when inserting data into the Schema Registry |
| schemaTopic | string | `"registry-schemas"` | Name of the topic used by the Schema Registry to store data. |
| strimziAPIVersion | string | `"v1beta2"` | Version of the Strimzi Custom Resource API. The correct value depends on the deployed version of Strimzi. See [this blog post](https://strimzi.io/blog/2021/04/29/api-conversion/) for more. |
| tls | bool | `true` |  |
