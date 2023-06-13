# love-producer

Helm chart for the LOVE producers.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the LOVE producer pods |
| env | object | `{"WEBSOCKET_HOST":"love-nginx/manager/ws/subscription"}` | This section holds a set of key, value pairs for environmental variables |
| envSecrets | object | `{"PROCESS_CONNECTION_PASS":"process-connection-pass"}` | This section holds a set of key, value pairs for secrets |
| image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the LOVE producer image |
| image.repository | string | `"lsstts/love-producer"` | The LOVE producer image to use |
| image.tag | string | `nil` |  |
| nodeSelector | object | `{}` | Node selection rules for the LOVE producer pods |
| podAnnotations | object | `{}` | This allows the specification of pod annotations. |
| producers | object | `{}` | This sections sets the list of producers to use. The producers should be specified like: _name_: _CSC name:index_ Example: ataos: ATAOS:0 |
| replicaCount | int | `1` | Set the replica count for the LOVE producers |
| resources | object | `{}` | Resource specifications for the LOVE producer pods |
| tolerations | list | `[]` | Toleration specifications for the LOVE producer pods |
