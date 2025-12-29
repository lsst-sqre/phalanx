# repertoire

Service discovery

**Homepage:** <https://repertoire.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/repertoire>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the repertoire deployment pod |
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy, used with Cloud SQL databases on Google Cloud. This will be run as a sidecar for the main Gafaelfawr pods, and as a separate service (behind a `NetworkPolicy`) for other, lower-traffic services. |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.tag | string | `"1.37.9"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | None, must be set if Cloud SQL Auth Proxy is enabled | Instance connection name for a Cloud SQL PostgreSQL instance |
| cloudsql.resources | object | See `values.yaml` | Resource limits and requests for the Cloud SQL Proxy container |
| cloudsql.serviceAccount | string | None, must be set if Cloud SQL Auth Proxy is enabled | The Google service account that has an IAM binding to the `gafaelfawr` Kubernetes service account and has the `cloudsql.client` role |
| config.applications | list | Set by Argo CD | List of applications deployed in this Phalanx environment (do not set) |
| config.availableDatasets | list | `[]` | Datasets available in the Phalanx environment. This should be overridden by environments to list the datasets they provide. |
| config.baseHostname | string | Set by Argo CD | Base hostname of the Phalanx environment (do not set) |
| config.butlerConfigs | object | Set by Argo CD | Butler configuration mapping (do not set) |
| config.datasets | object | See `values.yaml` | Known datasets. Each member of the list is a dictionary with key `description`. Datasets are only shown if also listed in `availableDatasets`. |
| config.hips.datasets | object | See `values.yaml` | Known HiPS datasets. Each should be a mapping of a label to an object containing the key `paths`, whose values are paths to the roots of HiPS surveys relative to the result of processing `sourceTemplate`. |
| config.hips.legacy.dataset | string | `nil` | If set, specifies the dataset that should be shown at the legacy HiPS list route that does not include the dataset name. If not set, no legacy HiPS list will be created. |
| config.hips.legacy.pathPrefix | string | `"/api/hips"` | Path prefix at which the legacy HiPS list should be served |
| config.hips.pathPrefix | string | `"/api/hips/v2"` | Path prefix at which the HiPS lists should be served |
| config.hips.sourceTemplate | string | See `values.yaml` | Jinja template to construct the base URLs of the underlying HiPS surveys, used to construct the HiPS list. |
| config.influxdbDatabases | object | `{}` | Dictionary of InfluxDB database names to connection information for that database, with keys `url`, `database`, `username`, `passwordKey`, and `schemaRegistry`. `passwordKey` must match an entry in `secrets.yaml`. |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.metrics.application | string | `"repertoire"` | Name under which to log metrics. Generally there is no reason to change this. |
| config.metrics.enabled | bool | `false` | Whether to enable sending metrics |
| config.metrics.events.topicPrefix | string | `"lsst.square.metrics.events"` | Topic prefix for events. It may sometimes be useful to change this in development environments. |
| config.metrics.schemaManager.registryUrl | string | Sasquatch in the local cluster | URL of the Confluent-compatible schema registry server |
| config.metrics.schemaManager.suffix | string | `""` | Suffix to add to all registered subjects. This is sometimes useful for experimentation during development. |
| config.pathPrefix | string | `"/repertoire"` | URL path prefix |
| config.rules | object | See `values.yaml` | Rules for determining the expected URLs of deployed services that use the main hostname. See the [Repertoire documentation](https://repertoire.lsst.io/) for more information. |
| config.sentry.enabled | bool | `false` | Whether to enable the Sentry integration |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
| config.subdomainRules | object | See `values.yaml` | Rules for determining the expected URLs of deployed services that use a subdomain. See the [Repertoire documentation](https://repertoire.lsst.io/) for more information. |
| config.tap.schemaSourceTemplate | string | lsst/sdm_schemas on GitHub | Template for schema artifact URLs (use {schemaVersion} placeholder) |
| config.tap.schemaVersion | string | `"w.2025.49"` | Default schema version for all TAP services (can be overridden per-app) |
| config.tap.servers | object | See `values.yaml` | TAP Server configuration by application name. Configuration is used to populate & update the TAP_SCHEMA database for each enabled TAP application |
| config.useSubdomains | list | `[]` | List of services that use subdomains instead of the main hostname. See the [Repertoire documentation](https://repertoire.lsst.io/) for more information. |
| global.environmentName | string | Set by Argo CD | Name of the Phalanx environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the repertoire image |
| image.repository | string | `"ghcr.io/lsst-sqre/repertoire"` | Image to use in the repertoire deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the repertoire deployment pod |
| podAnnotations | object | `{}` | Annotations for the repertoire deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the repertoire deployment pod |
| schemaHook.resources | object | See `values.yaml` | Resource limits and requests for the TAP schema update Helm hook job |
| tolerations | list | Tolerate GKE arm64 taint | Tolerations for the repertoire deployment pod |
