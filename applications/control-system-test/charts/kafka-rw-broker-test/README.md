# kafka-rw-broker-test

Helm chart for testing Kafka brokers read/write speed.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"quay.io/strimzi/kafka"` |  |
| image.tag | string | `""` |  |
| job.backoffLimit | int | `0` |  |
| job.ttlSecondsAfterFinished | int | `86400` |  |
| kafka.partitions | int | `3` |  |
| kafka.replicationFactor | int | `3` |  |
| kafka.retentionMs | string | `"3600000"` |  |
| kafka.topic | string | `"lsst.sal.kafka-broker-rw-test"` |  |
| namespace | string | `"control-system-test"` |  |
| resources.limits.cpu | string | `"1"` |  |
| resources.limits.memory | string | `"1Gi"` |  |
| resources.requests.cpu | string | `"250m"` |  |
| resources.requests.memory | string | `"512Mi"` |  |
| test.numRecords | int | `10000` |  |
| test.recordSize | int | `1024` |  |
| test.throughput | int | `1000` |  |
| test.timeoutMs | int | `60000` |  |
