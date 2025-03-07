# sia

Simple Image Access (SIA) IVOA Service using Butler

## Source Code

* <https://github.com/lsst-sqre/sia>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the sia deployment pod |
| config.butlerDataCollections | list | `[]` | List of data (Butler) Collections Expected attributes: `config`, `label`, `name`, `butler_type`, `repository` & `datalink_url` |
| config.directButlerEnabled | bool | `false` | Whether direct butler access is enabled |
| config.enableSentry | bool | `false` | Whether to send trace and telemetry information to Sentry. This traces every call and therefore should only be enabled in non-production environments. |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/api/sia"` | URL path prefix |
| config.pgUser | string | `"rubin"` | User to use from the PGPASSFILE if sia is using a direct Butler connection |
| config.sentryTracesSampleRate | float | `0` |  |
| config.slackAlerts | bool | `false` | Whether to send alerts and status to Slack. |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the sia image |
| image.repository | string | `"ghcr.io/lsst-sqre/sia"` | Image to use in the sia deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| ingress.path | string | `"/api/sia"` | Path prefix where app is hosted |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selection rules for the sia deployment pod |
| podAnnotations | object | `{}` | Annotations for the sia deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the sia deployment pod |
| tolerations | list | `[]` | Tolerations for the sia deployment pod |
