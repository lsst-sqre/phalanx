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
| config.appLinks | list | `[{"href":"/argo-cd/","internal":false,"label":"Argo CD"}]` | App menu items |
| config.coManageRegistryUrl | string | null disables the COmanage integration | URL to the COmanage registry, if the environment uses COmanage for identity. |
| config.docsBaseUrl | string | `"https://rsp.lsst.io"` | Base URL for user documentation (excludes trailing slash) |
| config.enableAppsMenu | bool | `false` | Enable the App menu |
| config.enableSentry | bool | `false` | Enable Sentry |
| config.headerLogoAlt | string | `"Logo"` | Alternative text for header logo for accessibility |
| config.headerLogoData | string | null uses Squareone's default built-in logo | Base64-encoded image data for header logo (without data URL prefix). Must be used with headerLogoMimeType. Used only if both headerLogoUrl and headerLogoFile are null. |
| config.headerLogoFile | string | null uses Squareone's default built-in logo | Filename of a logo image in the content/{environment}/ directory (e.g., "header-logo.png"). The file will be base64-encoded automatically. Used only if headerLogoUrl is null. Supported formats: .png, .jpg, .jpeg, .svg, .webp, .gif. Note: unlike MDX files, logo files do NOT fall back to idfprod if not found in the environment directory. |
| config.headerLogoHeight | int | `50` | Height of header logo in pixels |
| config.headerLogoMimeType | string | `nil` | MIME type for base64-encoded logo data (e.g., 'image/png', 'image/svg+xml'). Required when headerLogoData is provided. |
| config.headerLogoUrl | string | null uses Squareone's default built-in logo | URL to an external header logo image (HTTPS only). Takes priority over headerLogoFile and headerLogoData. |
| config.headerLogoWidth | string | null maintains aspect ratio | Width of header logo in pixels. If not provided, maintains aspect ratio based on height. |
| config.plausibleDomain | string | null disables Plausible tracking | Plausible tracking domain. For example, `data.lsst.cloud`. |
| config.semaphoreUrl | string | null disables the Semaphore integration | URL to the Semaphore (user notifications) API service. |
| config.sentryDebug | bool | `false` | Sentry debug mode |
| config.sentryDsn | string | `nil` | Sentry DSN |
| config.sentryReplaysOnErrorSampleRate | int | `0` | Sentry error replays sample rate |
| config.sentryReplaysSessionSampleRate | int | `0` | Sentry replays sample rate |
| config.sentryTracesSampleRate | int | `0` | Sentry traces sample rate |
| config.showPreview | bool | `true` | Show a "preview" badge in the homepage |
| config.siteDescription | string | See `values.yaml` | Site description, used in meta tags |
| config.siteName | string | `"Rubin Science Platform"` | Name of the site, used in the title and meta tags. |
| config.timesSquareUrl | string | null disables the Times Square integration | URL to the Times Square (parameterized notebooks) API service. |
| fullnameOverride | string | `""` | Overrides the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD Application | Base URL for the environment |
| global.environmentName | string | Set by Argo CD Application | Name of the Phalanx environment |
| global.host | string | Set by Argo CD Application | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
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
| resources | object | see `values.yaml` | Resource requests and limits for Squareone pods |
| tolerations[0].effect | string | `"NoSchedule"` |  |
| tolerations[0].key | string | `"kubernetes.io/arch"` |  |
| tolerations[0].operator | string | `"Equal"` |  |
| tolerations[0].value | string | `"amd64"` |  |
| tolerations[1].effect | string | `"NoSchedule"` |  |
| tolerations[1].key | string | `"kubernetes.io/arch"` |  |
| tolerations[1].operator | string | `"Equal"` |  |
| tolerations[1].value | string | `"arm64"` |  |
