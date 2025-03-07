# rolex2

Helm chart for the Rubin Observatory Log EXplorer (ROLEX) v2 app.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Configuration for deployment affinity |
| autoscaling | object | `{"enabled":false,"maxReplicas":100,"minReplicas":1,"targetCPUUtilizationPercentage":80}` | Auto scaling configuration. |
| fullnameOverride | string | `""` | Specify the deployed application name specifically. Overrides all other names. |
| image | object | `{"nexus3":null,"pullPolicy":"IfNotPresent","repository":"lsstts/rolex","tag":""}` | This section holds the configuration of the container image. |
| image.nexus3 | string | `nil` | The tag name for the Nexus3 Docker repository secrets if private images need to be pulled |
| image.pullPolicy | string | `"IfNotPresent"` | The policy to apply when pulling an image for deployment |
| image.repository | string | `"lsstts/rolex"` | The Docker registry name of the container image |
| image.tag | string | `""` | The tag of the container image |
| imagePullSecrets | list | `[]` | The list of pull secrets needed for the images. |
| ingress.annotations | object | `{}` | Annotations for the ingress |
| ingress.className | string | `""` | Assign the Ingress class name |
| ingress.enabled | bool | `false` | Enable ingress |
| ingress.hosts[0] | object | `{"host":"chart-example.local","paths":[{"path":"/","pathType":"ImplementationSpecific"}]}` | Hostname for the ingress service |
| ingress.hosts[0].paths | list | `[{"path":"/","pathType":"ImplementationSpecific"}]` | Paths for the ingress service |
| initialDelaySeconds | int | `10` | Initial delay in verifying service liveness status |
| nameOverride | string | `""` | Adds an extra string to the release name. |
| namespace | string | `"rolex2"` | This is the namespace in which rolex will be placed |
| nodeSelector | object | `{}` | Configurations for the deployment node selector |
| periodSeconds | int | `300` | How frequent to verify service liveness status |
| podAnnotations | object | `{}` | This allows the specification of pod annotations. |
| replicaCount | int | `1` | Number of replicas. |
| resources | object | `{}` | Reserved resources for the deployment. |
| service.path | string | `""` | The internal path to the service. |
| service.port | int | `80` | The internal port number to use for the Service. |
| service.type | string | `"ClusterIP"` | The Service type for the application. This is either ClusterIP (internal access) or LoadBalancer (external access) |
| timeoutSeconds | int | `30` | Response timeout when verifying service liveness status |
| tolerations | list | `[]` | Configuration for deployment toleration |
