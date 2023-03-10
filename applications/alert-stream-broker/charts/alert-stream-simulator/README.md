# alert-stream-simulator

Producer which repeatedly publishes a static set of alerts into a Kafka topic

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| clusterName | string | `"alert-broker"` | Name of a Strimzi Kafka cluster to connect to. |
| clusterPort | int | `9092` | Port to connect to on the Strimzi Kafka cluster. It should be an internal TLS listener. |
| fullnameOverride | string | `""` | Explicitly sets the full name used for the deployment and job (includes the release name). |
| image.imagePullPolicy | string | `"IfNotPresent"` | Pull policy for the Deployment |
| image.repository | string | `"lsstdm/alert-stream-simulator"` | Source repository for the image which holds the rubin-alert-stream program. |
| image.tag | string | `"v1.2.1"` | Tag to use for the rubin-alert-stream container. |
| kafkaUserName | string | `"alert-stream-simulator"` | The username of the Kafka user identity used to connect to the broker. |
| maxBytesRetained | string | `"24000000000"` | Maximum number of bytes for the replay topic, per partition, per replica. Default is 100GB, but should be lower to not fill storage. |
| maxMillisecondsRetained | string | `"604800000"` | Maximum amount of time to save simulated alerts in the replay topic, in milliseconds. Default is 7 days. |
| nameOverride | string | `""` | Explicitly sets the name of the deployment and job. |
| repeatInterval | int | `37` | How often (in seconds) to repeat the sample data into the replay topic. |
| replayTopicName | string | `"alerts-simulated"` | Name of the topic which will receive the repeated alerts on an interval. |
| replayTopicPartitions | int | `8` |  |
| replayTopicReplicas | int | `2` |  |
| schemaID | int | `1` | Integer ID to use in the prefix of alert data packets. This should be a valid Confluent Schema Registry ID associated with the schema used. |
| staticTopicName | string | `"alerts-static"` | Name of the topic which will hold a static single visit of sample data. |
| strimziAPIVersion | string | `"v1beta2"` | API version of the Strimzi installation's custom resource definitions |
