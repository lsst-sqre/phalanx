# audio-broadcaster

Helm chart for the audio-broadcaster.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the ts_audio_broadcaster pods |
| env | object | `{"WEBSERVER_PORT":8888}` | This section holds a set of key, value pairs for environmental variables |
| fullnameOverride | string | `""` | Specify the deployed application name specifically. Overrides all other names. |
| image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the ts_audio_broadcaster image |
| image.repository | string | `"lsstts/audio_broadcaster"` | The ts_audio_broadcaster image to use |
| image.revision | int | `nil` | The cycle revision to add to the image tag |
| ingress.annotations | object | `{}` | Annotations for the ts_audio_broadcaster ingress |
| ingress.className | string | `"nginx"` | Assign the Ingress class name |
| ingress.hostname | string | `"audio-broadcaster.local"` | Hostname for the ts_audio_broadcaster ingress |
| ingress.httpPath | string | `"/"` | Path name associated with the ts_audio_broadcaster ingress |
| ingress.pathType | string | `"Exact"` | Set the Kubernetes path type for the ts_audio_broadcaster ingress |
| microphones | list | `[]` | This sections sets the list of producers to use. The microphones should be specified like: _name_: _host_: _Microphone host_ _port_: _Microphone port_ Example: auxtel1: host: localhost port: 4444 |
| nameOverride | string | `""` | Adds an extra string to the release name. |
| namespace | string | `"love"` | The overall namespace for the ts_audio_broadcaster |
| nodeSelector | object | `{}` | Node selection rules for the ts_audio_broadcaster pods |
| podAnnotations | object | `{}` | This allows the specification of pod annotations. |
| ports.container | int | `80` | Container port for the ts_audio_broadcaster service |
| ports.node | int | `30000` | Node port for the ts_audio_broadcaster service |
| replicaCount | int | `1` | Set the replica count for the ts_audio_broadcasters |
| resources | object | `{}` | Resource specifications for the ts_audio_broadcaster pods |
| serviceType | string | `"ClusterIP"` | Service type specification |
| tolerations | list | `[]` | Toleration specifications for the ts_audio_broadcaster pods |
