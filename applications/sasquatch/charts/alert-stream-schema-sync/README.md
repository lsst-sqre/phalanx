# alert-stream-schema-sync

Syncs data into schema registry

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| clusterName | string | `"sasquatch"` | Strimzi "cluster name" of the broker to use as a backend. |
| compatibilityLevel | string | `"none"` | Compatibility level for the Schema Registry. Options are: none, backward, backward_transitive, forward, forward_transitive, full, and full_transitive. |
| hostname | string | `nil` | Hostname for an ingress which sends traffic to the Schema Registry. |
| name | string | `"sasquatch-schema-registry"` | Name used by the registry, and by its users. |
| port | int | `8081` | Port where the registry is listening. NOTE: Not actually configurable in strimzi-registry-operator, so this basically cannot be changed. |
| schemaSync | object | `{"image":{"pullPolicy":"Always","repository":"lsstdm/lsst_alert_packet","tag":"tickets-DM-53520"},"subject":"alert-packet"}` | Configuration for the Job which injects the most recent alert_packet schema into the Schema Registry |
| schemaSync.image.repository | string | `"lsstdm/lsst_alert_packet"` | Repository of a container which has the alert_packet syncLatestSchemaToRegistry.py program. |
| schemaSync.image.tag | string | `"tickets-DM-53520"` | Version of the container to use. If container isn't updating in Argo, switch to digest. |
| schemaSync.subject | string | `"alert-packet"` | Subject name to use when inserting data into the Schema Registry |
| schemaTopic | string | `"registry-schemas"` | Name of the topic used by the Schema Registry to store data. |
| tls | bool | `true` |  |
