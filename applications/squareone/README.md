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
| config.docsBaseUrl | string | `"https://rsp.lsst.io"` | Base URL for user documentation (excludes trailing slash) |
| config.docsPageMdx | string | See `values.yaml` | MDX content for the `/docs` page |
| config.emailVerifiedPageMdx | string | See `values.yaml` | MDX content for the `/enrollment/thanks-for-verifying` page |
| config.enableSentry | bool | See `values.yaml` | Enable Sentry |
| config.pendingApprovalPageMdx | string | See `values.yaml` | MDX content for the `/enrollment/pending-approval` page |
| config.pendingVerificationPageMdx | string | See `values.yaml` | MDX content for the `/enrollment/pending-confirmation` |
| config.plausibleDomain | string | `nil` | Plausible tracking domain. For example, `data.lsst.cloud`. @default null disables Plausible tracking |
| config.semaphoreUrl | string | `nil` | URL to the Semaphore (user notifications) API service. @default null disables the Semaphore integration |
| config.sentryDebug | bool | See `values.yaml` | Sentry debug mode |
| config.sentryDsn | string | See `values.yaml` | Sentry DSN |
| config.sentryReplaysOnErrorSampleRate | int | See `values.yaml` | Sentry error replays sample rate |
| config.sentryReplaysSessionSampleRate | int | See `values.yaml` | Sentry replays sample rate |
| config.sentryTracesSampleRate | int | See `values.yaml` | Sentry traces sample rate |
| config.siteDescription | string | `"Access Rubin Observatory Legacy Survey of Space and Time data.\n"` | Site description, used in meta tags |
| config.siteName | string | `"Rubin Science Platform"` | Name of the site, used in the title and meta tags. |
| config.supportPageMdx | string | See `values.yaml` | MDX content for the `/support` page |
| config.timesSquareUrl | string | `nil` | URL to the Times Square (parameterized notebooks) API service. @default null disables the Times Square integration |
| config.verifyEmailPageMdx | string | See `values.yaml` | MDX content for the `/enrollment/thanks-for-signing-up` page |
| fullnameOverride | string | `""` | Overrides the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD Application | Base URL for the environment |
| global.environmentName | string | Set by Argo CD Application | Name of the Phalanx environment |
| global.host | string | Set by Argo CD Application | Host name for ingress |
| global.vaultSecretsPathPrefix | string | Set by Argo CD Application | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy (tip: use Always for development) |
| image.repository | string | `"ghcr.io/lsst-sqre/squareone"` | Squareone Docker image repository |
| image.tag | string | Chart's appVersion | Overrides the image tag. |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.enabled | bool | `true` | Enable ingress |
| ingress.timesSquareScope | string | `"exec:notebook"` | Scope required for /times-square UI |
| nameOverride | string | `""` | Overrides the base name for resources |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` | Annotations for squareone pods |
| replicaCount | int | `1` | Number of squareone pods to run in the deployment. |
| resources | object | see `values.yaml` | Resource requests and limits for squareone pods |
| tolerations | list | `[]` |  |
