# rubin-too-producer

Helm chart for the Rubin Observatory Targets of Opportunity Producer.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Configuration for deployment affinity |
| fullnameOverride | string | `""` | Specify the deployed application name specifically. Overrides all other names. |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image | object | `{"nexus3":null,"pullPolicy":"IfNotPresent","repository":"lsstts/rubin_too_producer","tag":""}` | This section holds the configuration of the container image. |
| image.nexus3 | string | `nil` | The tag name for the Nexus3 Docker repository secrets if private images need to be pulled |
| image.pullPolicy | string | `"IfNotPresent"` | The policy to apply when pulling an image for deployment |
| image.repository | string | `"lsstts/rubin_too_producer"` | The Docker registry name of the container image |
| image.tag | string | `""` | The tag of the container image |
| nameOverride | string | `""` | Adds an extra string to the release name. |
| namespace | string | `"rubin-too-producer"` | This is the namespace in which the application will be placed |
| nodeSelector | object | `{}` | Configurations for the deployment node selector |
| podAnnotations | object | `{}` | This allows the specification of pod annotations. |
| replicaCount | int | `1` | Number of replicas. |
| resources | object | `{}` | Reserved resources for the deployment. |
| tolerations | list | `[]` | Configuration for deployment toleration |
