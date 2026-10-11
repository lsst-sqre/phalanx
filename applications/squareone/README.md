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
| config.adminPageScopes | object | `{"notifications":["admin:notifications"],"oidcClients":["admin:oidc"],"sentry":["exec:admin"],"serviceTokens":["admin:token"]}` | Maps each admin page id (`notifications`, `serviceTokens`, `oidcClients`, `sentry`) to the Gafaelfawr scopes granting access to it. Holding any one of a page's scopes is sufficient; an empty list hides the page. Override only the pages that differ — the rest keep their defaults. Keep this consistent with `ingress.adminScopes`, which decides who gets past the /admin ingress at all. |
| config.appLinks | list | `[]` | Additional Apps menu items for applications that service discovery does not describe. Each item has a `label`, an `href`, and `internal` (true for a Squareone route, false for another application). Items whose `href` duplicates a discovered service are dropped. |
| config.docsBaseUrl | string | `"https://rsp.lsst.io"` | Base URL for user documentation (excludes trailing slash) |
| config.enableAppsMenu | bool | `false` | Enable the Apps menu in the header. Its items come from Repertoire service discovery: Times Square when that application is enabled, and the Argo CD, Chronograf, Kafdrop, and WebDAV UI services, each shown only to users with the scopes the service requires. |
| config.enableSentry | bool | `false` | Enable Sentry |
| config.enableUserNotifications | bool | `false` | Enable the user-facing notifications UI: the unread badge in the header user menu and the /notifications inbox and detail pages. Squareone finds the Semaphore API through Repertoire service discovery, so the `semaphore` application must be enabled in the environment. |
| config.headerLogoAlt | string | `"Logo"` | Alternative text for header logo for accessibility |
| config.headerLogoData | string | null uses Squareone's default built-in logo | Base64-encoded image data for header logo (without data URL prefix). Must be used with headerLogoMimeType. Used only if both headerLogoUrl and headerLogoFile are null. |
| config.headerLogoFile | string | null uses Squareone's default built-in logo | Filename of a logo image in the content/{environment}/ directory (e.g., "header-logo.png"). The file will be base64-encoded automatically. Used only if headerLogoUrl is null. Supported formats: .png, .jpg, .jpeg, .svg, .webp, .gif. Note: unlike MDX files, logo files do NOT fall back to idfprod if not found in the environment directory. |
| config.headerLogoHeight | int | `50` | Height of header logo in pixels |
| config.headerLogoMimeType | string | `nil` | MIME type for base64-encoded logo data (e.g., 'image/png', 'image/svg+xml'). Required when headerLogoData is provided. |
| config.headerLogoUrl | string | null uses Squareone's default built-in logo | URL to an external header logo image (HTTPS only). Takes priority over headerLogoFile and headerLogoData. |
| config.headerLogoWidth | string | null maintains aspect ratio | Width of header logo in pixels. If not provided, maintains aspect ratio based on height. |
| config.plausibleDomain | string | null disables Plausible tracking | Plausible tracking domain. For example, `data.lsst.cloud`. |
| config.sentryDebug | bool | `false` | Sentry debug mode |
| config.sentryDsn | string | `nil` | Sentry DSN |
| config.sentryReplaysOnErrorSampleRate | int | `0` | Sentry error replays sample rate |
| config.sentryReplaysSessionSampleRate | int | `0` | Sentry replays sample rate |
| config.sentryTracesSampleRate | int | `0` | Sentry traces sample rate |
| config.showPreview | bool | `true` | Show a "preview" badge in the homepage |
| config.siteDescription | string | See `values.yaml` | Site description, used in meta tags |
| config.siteName | string | The environment title from Repertoire service discovery, else "Rubin Science Platform" | Name of the site, used in the title and meta tags. Set this only to override the environment's title from Repertoire service discovery. |
| config.timesSquareUrl | string | null, resolved from service discovery | URL to the Times Square (parameterized notebooks) API service. When unset, Squareone defaults it from Repertoire service discovery (`services.internal.times-square.url`), which lists Times Square only in environments that deploy it. The `/times-square/` pages are disabled when neither this value nor discovery provides a URL. |
| config.useDiscoveryDefaults | bool | `true` | Omit `baseUrl` and `environmentName` from the Squareone configuration so that Squareone derives them from Repertoire service discovery (the `squareone` UI service URL and `environment.label`). Requires Repertoire 3.0 or later. Set to `false` to render them from `global.baseUrl` and `global.environmentName` instead. |
| config.userNotificationsPollIntervalSeconds | int | `300` | Background polling cadence, in seconds, for the unread notification count in the header user menu. Only relevant when enableUserNotifications is true. |
| fullnameOverride | string | `""` | Overrides the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD Application | Base URL for the environment |
| global.environmentName | string | Set by Argo CD Application | Name of the Phalanx environment |
| global.host | string | Set by Argo CD Application | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPathPrefix | string | Set by Argo CD Application | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy (tip: use Always for development) |
| image.repository | string | `"ghcr.io/lsst-sqre/squareone"` | Squareone Docker image repository |
| image.tag | string | Chart's appVersion | Overrides the image tag. |
| ingress.adminScopes | list | `["exec:admin","admin:notifications","admin:token","admin:oidc"]` | Scopes that grant access to the /admin UI. Holding any one of them is sufficient; which admin pages each scope reveals is decided by Squareone's own `adminPageScopes` configuration. |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.delegateScopes | list | Gafaelfawr's default known scopes; see `values.yaml` | Scopes requested for the internal token Gafaelfawr delegates to Squareone on the /times-square and /admin ingresses (`config.delegate.internal.scopes`). Gafaelfawr strips its session cookie from requests crossing a `GafaelfawrIngress`, so Squareone's server-side prefetch of the signed-in user's scopes reads them back from this token instead. A delegated token only carries the requested scopes the user actually holds, so this list must cover every scope the UI gates on: it defaults to Gafaelfawr's full known-scope list, and an environment that defines extra scopes in its Gafaelfawr `config.knownScopes` should add them here. (A Gafaelfawr request header carrying the user's scopes would make this list unnecessary; that has not been requested.) |
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
