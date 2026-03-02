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
| config.coManageRegistryUrl | string | `nil` | URL to the COmanage registry, if the environment uses COmanage for identity. @default null disables the COmanage integration |
| config.docsBaseUrl | string | `"https://rsp.lsst.io"` | Base URL for user documentation (excludes trailing slash) |
| config.enableAppsMenu | bool | `false` | Enable the App menu |
| config.enableSentry | bool | See `values.yaml` | Enable Sentry |
| config.headerLogoAlt | string | See `values.yaml` | Alternative text for header logo for accessibility |
| config.headerLogoData | string | `nil` | Base64-encoded image data for header logo (without data URL prefix). Must be used with headerLogoMimeType. Used only if both headerLogoUrl and headerLogoFile are null. @default null uses Squareone's default built-in logo |
| config.headerLogoFile | string | `nil` | Filename of a logo image in the content/{environment}/ directory (e.g., "header-logo.png"). The file will be base64-encoded automatically. Used only if headerLogoUrl is null. Supported formats: .png, .jpg, .jpeg, .svg, .webp, .gif. Note: unlike MDX files, logo files do NOT fall back to idfprod if not found in the environment directory. @default null uses Squareone's default built-in logo |
| config.headerLogoHeight | int | See `values.yaml` | Height of header logo in pixels |
| config.headerLogoMimeType | string | See `values.yaml` | MIME type for base64-encoded logo data (e.g., 'image/png', 'image/svg+xml'). Required when headerLogoData is provided. |
| config.headerLogoUrl | string | `nil` | URL to an external header logo image (HTTPS only). Takes priority over headerLogoFile and headerLogoData. @default null uses Squareone's default built-in logo |
| config.headerLogoWidth | string | `nil` | Width of header logo in pixels. If not provided, maintains aspect ratio based on height. @default null maintains aspect ratio |
| config.plausibleDomain | string | `nil` | Plausible tracking domain. For example, `data.lsst.cloud`. @default null disables Plausible tracking |
| config.semaphoreUrl | string | `nil` | URL to the Semaphore (user notifications) API service. @default null disables the Semaphore integration |
| config.sentryDebug | bool | See `values.yaml` | Sentry debug mode |
| config.sentryDsn | string | See `values.yaml` | Sentry DSN |
| config.sentryReplaysOnErrorSampleRate | int | See `values.yaml` | Sentry error replays sample rate |
| config.sentryReplaysSessionSampleRate | int | See `values.yaml` | Sentry replays sample rate |
| config.sentryTracesSampleRate | int | See `values.yaml` | Sentry traces sample rate |
| config.showPreview | bool | `true` | Show a "preview" badge in the homepage |
| config.siteDescription | string | `"Access Rubin Observatory Legacy Survey of Space and Time data.\n"` | Site description, used in meta tags |
| config.siteName | string | `"Rubin Science Platform"` | Name of the site, used in the title and meta tags. |
| config.timesSquareUrl | string | `nil` | URL to the Times Square (parameterized notebooks) API service. @default null disables the Times Square integration |
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
| tolerations[0].effect | string | `"NoSchedule"` |  |
| tolerations[0].key | string | `"kubernetes.io/arch"` |  |
| tolerations[0].operator | string | `"Equal"` |  |
| tolerations[0].value | string | `"arm64"` |  |
