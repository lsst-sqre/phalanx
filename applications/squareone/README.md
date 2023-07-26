# squareone

Squareone is the homepage UI for the Rubin Science Platform.

**Homepage:** <https://squareone.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/squareone>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| autoscaling.enabled | bool | `false` |  |
| autoscaling.maxReplicas | int | `100` |  |
| autoscaling.minReplicas | int | `1` |  |
| autoscaling.targetCPUUtilizationPercentage | int | `80` |  |
| config.apiAspectPageMdx | string | See `values.yaml` | MDX content for the `/api-aspect` page |
| config.coManageRegistryUrl | string | `nil` | URL to the COmanage registry, if the environment uses COmanage for identity. @default null disables the COmanage integration |
| config.docsPageMdx | string | See `values.yaml` | MDX content for the `/docs` page |
| config.emailVerifiedPageMdx | string | See `values.yaml` | MDX content for the `/enrollment/thanks-for-verifying` page |
| config.pendingApprovalPageMdx | string | See `values.yaml` | MDX content for the `/enrollment/pending-approval` page |
| config.pendingVerificationPageMdx | string | See `values.yaml` | MDX content for the `/enrollment/pending-confirmation` |
| config.semaphoreUrl | string | `nil` | URL to the Semaphore (user notifications) API service. @default null disables the Semaphore integration |
| config.siteDescription | string | `"Access Rubin Observatory Legacy Survey of Space and Time data.\n"` | Site description, used in meta tags |
| config.siteName | string | `"Rubin Science Platform"` | Name of the site, used in the title and meta tags. |
| config.supportPageMdx | string | See `values.yaml` | MDX content for the `/support` page |
| config.timesSquareUrl | string | `nil` | URL to the Times Square (parameterized notebooks) API service. @default null disables the Times Square integration |
| config.verifyEmailPageMdx | string | See `values.yaml` | MDX content for the `/enrollment/thanks-for-signing-up` page |
| fullnameOverride | string | `""` | Overrides the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD Application | Base URL for the environment |
| global.host | string | Set by Argo CD Application | Host name for ingress |
| global.vaultSecretsPathPrefix | string | Set by Argo CD Application | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy (tip: use Always for development) |
| image.repository | string | `"ghcr.io/lsst-sqre/squareone"` | Squareone Docker image repository |
| image.tag | string | Chart's appVersion | Overrides the image tag. |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.enabled | bool | `true` | Enable ingress |
| ingress.tls | bool | `true` | Enable Let's Encrypt TLS management in this chart. This should be false if TLS is managed elsewhere, such as in an ingress-nginx app. |
| nameOverride | string | `""` | Overrides the base name for resources |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` | Annotations for squareone pods |
| replicaCount | int | `1` | Number of squareone pods to run in the deployment. |
| resources | object | `{}` |  |
| tolerations | list | `[]` |  |
