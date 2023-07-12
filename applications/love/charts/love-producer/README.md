# love-producer

Helm chart for the LOVE producers.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules applied to all LOVE producer pods |
| annotations | object | `{}` | This allows for the specification of pod annotations. |
| env | object | `{"WEBSOCKET_HOST":"love-nginx/manager/ws/subscription"}` | This section holds a set of key, value pairs for environmental variables |
| envSecrets | object | `{"PROCESS_CONNECTION_PASS":"process-connection-pass"}` | This section holds a set of key, value pairs for secrets |
| image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the LOVE producer image |
| image.repository | string | `"lsstts/love-producer"` | The LOVE producer image to use |
| image.tag | string | `nil` |  |
| nodeSelector | object | `{}` | Node selection rules applied to all LOVE producer pods |
| producers | obj | `[]` | This sections sets the list of producers to use. The producers are collected into producer groups and a CSC producers will be assigned to a given container. The producers should be specified like: _name_: The top-level name for the producer group. _cscs_: Map of _CSC name:index_ Example: ataos: ATAOS:0 The following attributes are optional _resources_ (A resource object specification) _nodeSelector_ (A node selector object specification) _tolerations_ (A list of tolerations) _affinity_ (An affinity object specification) |
| replicaCount | int | `1` | Set the replica count for the LOVE producers |
| resources | object | `{}` | Resource specifications applied to all LOVE producer pods |
| tolerations | list | `[]` | Toleration specifications applied to all LOVE producer pods |
