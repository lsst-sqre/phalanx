# control-system

Sasquatch configuration for the Observatory Control System

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cluster.name | string | `"sasquatch"` | Name of the Strimzi cluster. Synchronize this with the cluster name in the parent Sasquatch chart. |
| topics | list | `[]` | Create lsst.s3.* related topics for the ts-salkafka user. |
