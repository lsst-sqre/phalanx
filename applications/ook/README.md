# ook

Ook is the librarian service for Rubin Observatory. Ook indexes documentation content into the Algolia search engine that powers the Rubin Observatory documentation portal, www.lsst.io.

**Homepage:** <https://ook.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/ook>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| audit.affinity | object | `{}` | Affinity rules for Ook audit pods |
| audit.enabled | bool | `true` | Enable the audit job |
| audit.nodeSelector | object | `{}` | Node selection rules for Ook audit pods |
| audit.podAnnotations | object | `{}` | Annotations for Ook audit pods |
| audit.reingest | bool | `true` | Reingest missing documents |
| audit.resources | object | `{}` | Resource limits and requests for Ook audit pods |
| audit.schedule | string | `"15 2 * * *"` | Cron schedule string for ook audit job (UTC) |
| audit.tolerations | list | `[]` | Tolerations for Ook audit pods |
| audit.ttlSecondsAfterFinished | int | `86400` | Time (second) to keep a finished job before cleaning up |
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy sidecar, used with Cloud SQL databases on Google Cloud |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.resources | object | See `values.yaml` | Resource requests and limits for Cloud SQL pod |
| cloudsql.image.tag | string | `"1.38.1"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | `""` | Instance connection name for a Cloud SQL PostgreSQL instance |
| cloudsql.serviceAccount | string | `""` | The Google service account that has an IAM binding to the `ook` Kubernetes service accounts and has the `cloudsql.client` role |
| config.algolia.documents_index | string | `"documents_dev"` | Name of the Algolia index for documents |
| config.databaseUrl | string | `""` | Database URL |
| config.intersphinx.activeWindow | string | `"30d"` | Active window for the intersphinx refresh job. The scheduled refresh only revalidates cached inventories requested by a client within this window; inventories last requested longer ago are skipped (not deleted) |
| config.intersphinx.negativeTtl | string | `"5m"` | Negative-cache TTL for cold-miss intersphinx inventory fetch failures. A repeat request inside this window returns the error without re-contacting upstream |
| config.intersphinx.ttl | string | `"1h"` | Freshness TTL for cached intersphinx inventories. An inventory fetched within this window is served as a fresh cache hit; an older one is served stale on the request path while the refresh job revalidates it |
| config.linkcheck.blockedRecheckInterval | string | `"1h"` | Delay until the next recheck of a bot-blocked link, revisited at this near-term cadence because a block is inconclusive and tends to flap |
| config.linkcheck.brokenMinAttempts | int | `3` | Minimum number of consecutive failed attempts before a previously-OK link is declared broken instead of failing |
| config.linkcheck.brokenRecheckInterval | string | `"24h"` | Delay until the next recheck of a broken link, revisited at this slow cadence so a since-fixed link can heal without waiting to be resubmitted |
| config.linkcheck.brokenThreshold | string | `"48h"` | Minimum span of consecutive failures before a previously-OK link is declared broken instead of failing |
| config.linkcheck.checkRetention | string | `"30d"` | Age beyond which link-check submission records are purged by the scheduled linkcheck-recheck maintenance command |
| config.linkcheck.freshnessTtl | string | `"24h"` | Age below which a URL's stored check result is considered fresh and is not rechecked on submission |
| config.linkcheck.hostInterval | string | `"1s"` | Minimum politeness interval between link-check requests to the same host |
| config.linkcheck.maxConcurrency | int | `10` | Maximum number of concurrent link-check HTTP requests across all hosts |
| config.linkcheck.maxUrlsPerCheck | int | `1000` | Maximum number of unique canonical URLs accepted in a single link-check submission |
| config.linkcheck.recheckIntervals | list | `["1h","4h","24h","48h"]` | Delays until the next recheck of a failing link, indexed by the number of consecutive failures so far |
| config.linkcheck.requestTimeout | string | `"30s"` | Total timeout applied to each link-check HTTP request |
| config.linkcheck.userAgent | string | `""` | Override for the User-Agent header sent on every link-check request. Leave empty to use Ook's built-in browser-prefixed hybrid default, which carries the running Ook version and repo URL |
| config.logLevel | string | `"INFO"` | Logging level: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" |
| config.migrateCountryCodes | bool | false to disable country code migration | Whether to migrate country codes in the database |
| config.topics.ingest | string | `"lsst.square-events.ook.ingest"` | Kafka topic name for ingest events |
| config.topics.linkcheck | string | `"lsst.square-events.ook.linkcheck"` | Kafka topic name for link-check execution requests |
| config.updateSchema | bool | false to disable schema upgrades | Whether to run the database migration job |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"ghcr.io/lsst-sqre/ook"` | Squarebot image repository |
| image.tag | string | The appVersion of the chart | Tag of the image |
| imagePullSecrets | list | `[]` | Secret names to use for all Docker pulls |
| ingestLsstTexmf.affinity | object | `{}` | Affinity rules for job pods |
| ingestLsstTexmf.enabled | bool | `false` | Enable the ingest-lsst-texmf job |
| ingestLsstTexmf.gitRef | string | `"main"` | Git ref to use for the ingest-lsst-texmf job |
| ingestLsstTexmf.nodeSelector | object | `{}` | Node selection rules for job pods |
| ingestLsstTexmf.podAnnotations | object | `{}` | Annotations for job pods |
| ingestLsstTexmf.resources | object | `{}` | Resource limits and requests for job pods |
| ingestLsstTexmf.schedule | string | `"0 10 * * *"` | Cron schedule string for inget-lsst-texmf job (UTC) |
| ingestLsstTexmf.tolerations | list | `[]` | Tolerations for job pods |
| ingestLsstTexmf.ttlSecondsAfterFinished | int | `86400` | Time (second) to keep a finished job before cleaning up |
| ingestUpdated.affinity | object | `{}` | Affinity rules for Ook audit pods |
| ingestUpdated.enabled | bool | `false` | Enable the ingest-updated job |
| ingestUpdated.nodeSelector | object | `{}` | Node selection rules for Ook audit pods |
| ingestUpdated.podAnnotations | object | `{}` | Annotations for Ook audit pods |
| ingestUpdated.resources | object | `{}` | Resource limits and requests for Ook audit pods |
| ingestUpdated.schedule | string | `"15 3 * * *"` | Cron schedule string for ook audit job (UTC) |
| ingestUpdated.tolerations | list | `[]` | Tolerations for Ook audit pods |
| ingestUpdated.ttlSecondsAfterFinished | int | `86400` | Time (second) to keep a finished job before cleaning up |
| ingestUpdated.window | string | `"2d"` | Time window to look for updated documents (e.g. 1h, 2d, 3w). This must be set to a value greater than the cron schedule for the ingest-updated job. |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.path | string | `"/ook"` | Path prefix where Squarebot is hosted |
| intersphinxRefresh.affinity | object | `{}` | Affinity rules for Ook intersphinx-refresh pods |
| intersphinxRefresh.enabled | bool | `false` | Enable the intersphinx-refresh job |
| intersphinxRefresh.nodeSelector | object | `{}` | Node selection rules for Ook intersphinx-refresh pods |
| intersphinxRefresh.podAnnotations | object | `{}` | Annotations for Ook intersphinx-refresh pods |
| intersphinxRefresh.resources | object | `{}` | Resource limits and requests for Ook intersphinx-refresh pods |
| intersphinxRefresh.schedule | string | `"15 * * * *"` | Cron schedule string for the ook intersphinx-refresh job (UTC) |
| intersphinxRefresh.tolerations | list | `[]` | Tolerations for Ook intersphinx-refresh pods |
| intersphinxRefresh.ttlSecondsAfterFinished | int | `86400` | Time (second) to keep a finished job before cleaning up |
| linkcheckRecheck.affinity | object | `{}` | Affinity rules for Ook linkcheck-recheck pods |
| linkcheckRecheck.enabled | bool | `false` | Enable the linkcheck-recheck job |
| linkcheckRecheck.nodeSelector | object | `{}` | Node selection rules for Ook linkcheck-recheck pods |
| linkcheckRecheck.podAnnotations | object | `{}` | Annotations for Ook linkcheck-recheck pods |
| linkcheckRecheck.resources | object | `{}` | Resource limits and requests for Ook linkcheck-recheck pods |
| linkcheckRecheck.schedule | string | `"45 4 * * *"` | Cron schedule string for the ook linkcheck-recheck job (UTC) |
| linkcheckRecheck.tolerations | list | `[]` | Tolerations for Ook linkcheck-recheck pods |
| linkcheckRecheck.ttlSecondsAfterFinished | int | `86400` | Time (second) to keep a finished job before cleaning up |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` | Annotations for API and worker pods |
| replicaCount | int | `1` | Number of API pods to run |
| resources | object | See `values.yaml` | Resource requests and limits for Ook pod |
| service.port | int | `80` | Port of the service to create and map to the ingress |
| service.type | string | `"ClusterIP"` | Type of service to create |
| tolerations | list | `[]` |  |
