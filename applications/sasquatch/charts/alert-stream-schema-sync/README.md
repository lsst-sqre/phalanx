# alert-stream-schema-sync

Syncs data into schema registry

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| schemaRegistryUrl | string | `"http://sasquatch-schema-registry:8081"` | URL for Schema Registry |
| schemaSync | object | `{"image":{"pullPolicy":"IfNotPresent","repository":"lsstdm/lsst_alert_packet","tag":""},"subject":"alert-packet"}` | Configuration for the Job which injects the most recent alert_packet schema into the Schema Registry |
| schemaSync.image.repository | string | `"lsstdm/lsst_alert_packet"` | Repository of a container which has the alert_packet syncLatestSchemaToRegistry.py program. |
| schemaSync.image.tag | string | `""` | Version of the container to use. If container isn't updating in Argo, switch to digest. |
| schemaSync.subject | string | `"alert-packet"` | Subject name to use when inserting data into the Schema Registry |
