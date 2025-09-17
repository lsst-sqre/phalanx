# nightlydigest-backend

Helm chart for the Nightlydigest FastAPI web server.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules applied to the pod. |
| annotations | object | `{}` | This allows for the specification of pod annotations. |
| env | list | `[]` | List of Kubernetes environment variable specifiers. |
| envSecrets | list | `[]` | List of environment variables that should come from secrets. |
| image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the Nightlydigest backend image. |
| image.repository | string | `"lsstts/nightlydigest-backend"` | The Nightlydigest backend image to use. |
| image.tag | int | `nil` | The cycle revision to add to the image tag. |
| namespace | string | `"nightlydigest"` | The overall namespace for the application. |
| nodeSelector | object | `{}` | Node selection rules applied to the pod. |
| resources | object | `{}` | Resource specifications applied to the pod. |
| tolerations | list | `[]` | Toleration specifications applied to the pod. |
