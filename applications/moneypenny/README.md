# moneypenny

User provisioning actions

## Source Code

* <https://github.com/lsst-sqre/moneypenny>
* <https://github.com/lsst-sqre/farthing>
* <https://github.com/lsst-sqre/inituserhome>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the vo-cutouts frontend pod |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the moneypenny image |
| image.repository | string | `"lsstsqre/moneypenny"` | moneypenny image to use |
| image.tag | string | The appVersion of the chart | Tag of moneypenny image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the vo-cutouts frontend pod |
| orders.commission | list | `[{"image":"lsstsqre/farthing","name":"farthing","securityContext":{"allowPrivilegeEscalation":false,"runAsNonRootUser":true,"runAsUser":1000}}]` | List of specifications for containers to run to commission a new user. Each member of the list should set a container `name`, `image`, and `securityContext` and may contain `volumeMounts`. |
| orders.retire | list | `[{"image":"lsstsqre/farthing","name":"farthing","securityContext":{"allowPrivilegeEscalation":false,"runAsNonRootUser":true,"runAsUser":1000}}]` | List of specifications for containers to run to retire a user.  Each member of the list should set a container `name`, `image`, and `securityContext` and may contain `volumeMounts`. |
| orders.volumes | list | `[]` | Additional volumes to mount when commissioning or retiring users. |
| podAnnotations | object | `{}` | Annotations for the vo-cutouts frontend pod |
| quips | string | A small selection | Moneypenny quotes |
| replicaCount | int | `1` | Number of pods to start |
| resources | object | `{}` | Resource limits and requests for the vo-cutouts frontend pod |
| serviceAccount.name | string | Name based on the fullname template | Name of the service account to use |
| tolerations | list | `[]` | Tolerations for the vo-cutouts frontend pod |
