# nightlydigest-backend

Helm chart for the Nightlydigest FastAPI web server.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules applied to the pod. |
| annotations | object | `{}` | This allows for the specification of pod annotations. |
| env | list | `[]` | List of Kubernetes environment variable specifiers. |
| envSecrets | list | `[]` | List of environment variables that should come from secrets. |
| gid | int | `73006` | The group ID to run the backend container as. Match runAsGroup in securityContext for mounted volumes. |
| image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the Nightlydigest backend image. |
| image.repository | string | `"lsstts/nightlydigest-backend"` | The Nightlydigest backend image to use. |
| image.tag | int | `nil` | The cycle revision to add to the image tag. |
| namespace | string | `"nightlydigest"` | The overall namespace for the application. |
| nodeSelector | object | `{}` | Node selection rules applied to the pod. |
| producer | object | `{"enabled":false,"gcpBucketName":"default","gcpProjectId":"default","restartPolicy":"Never","schedule":"0 * * * *"}` | Configuration for the Nightly Digest Producer component. |
| producer.enabled | bool | `false` | If the Nightly Digest Producer component should be enabled. |
| producer.gcpBucketName | string | `"default"` | GCP bucket name for the Nightly Digest Producer component. |
| producer.gcpProjectId | string | `"default"` | GCP project ID for the Nightly Digest Producer component. |
| producer.restartPolicy | string | `"Never"` | The cron job restart policy type |
| producer.schedule | string | `"0 * * * *"` | The cron job schedule in cron format |
| replicas | int | `1` | The number of replicas for the backend deployment. |
| resources | object | `{}` | Resource specifications applied to the pod. |
| tolerations | list | `[]` | Toleration specifications applied to the pod. |
| uid | int | `73006` | The user ID to run the backend container as. Match runAsUser and fsGroup in securityContext for mounted volumes. |
