# log-explorer

Rapid analysis log explorer

## Source Code

* <https://github.com/lsst-so/ra_log_explorer>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the log-explorer deployment pod |
| cache | object | See `values.yaml` | Persistent volume for the log cache. Fetching a night out of Loki takes minutes, so the cache is what makes the tool usable a second time; an emptyDir would throw it away on every pod restart. |
| cache.mountPath | string | `"/var/cache/ra-log-explorer"` | Where the cache volume is mounted, and what the application is told to use as its cache root. |
| cache.sizeGi | int | `50` | Size of the cache volume, in GiB. Given as a bare number rather than a quantity string because it sets two things that must not disagree: the volume's size, and the byte ceiling the application's LRU eviction keeps the cache under (`usagePercent` of it). Deriving both from one value is what stops the app happily filling a disk it thinks is bigger than it is. |
| cache.storageClassName | string | `"rook-ceph-block"` | Storage class for the cache volume |
| cache.usagePercent | int | `85` | Percentage of the volume the application will fill before it starts evicting least-recently-used windows. The headroom covers filesystem overhead and the gap between a fetch finishing and the eviction sweep that follows it — the cache is briefly over its ceiling in between. |
| config.liveLagS | int | `60` | How far behind "now", in seconds, each live poll stops. Covers Loki ingestion lag: a log line stamped t can be ingested seconds after t, and a poll that raced it would miss it. Raise this if the end-of-night verification pass reports pods needing refetches. |
| config.livePollS | int | `300` | Poll interval, in seconds, for live mode: the server continuously fetches the current night's logs (all pods) into its cache, so exposure views during the night are served by slicing what is already on disk instead of querying Loki. Nightly data volume lands on the cache PVC (~9 GiB measured for a busy night, before LRU eviction reclaims it), so `cache.sizeGi` must keep room for a few nights. 0 disables live mode and returns the app to purely on-demand fetching. 300 keeps the Loki query load modest; an exposure becomes viewable at most ~5 minutes after its shutter+5min ideal. |
| config.lokiPassword | string | `""` | Loki password in the clear, for bringing an environment up before its Vault secret exists. **Do not commit a real value**: this repository is public, and anything set here also shows in plain text in `kubectl describe pod` and the Argo CD UI. Pass it as a Helm parameter override on the Argo CD Application instead, and clear it once the `loki-password` Vault secret is populated. Empty (the normal state) reads the password from that secret, and the pod starts either way — with neither, log fetches fail with a legible error and the rest of the app works. |
| config.lokiUsername | string | `"omega"` | Loki HTTP basic-auth username. The password comes from the `loki-password` Vault secret. Both are set server-side because the application takes no configuration from the browser at all: one process serves every user, so a credentials field would let whoever filled it in last break fetches for everybody else. |
| config.site | object | See the per-environment values files | The one site this deployment serves. A *site* pairs a Loki cluster (where the logs live) with the ConsDB endpoint that owns shutter-close truth for that cluster's data; the two must match or a dataId resolves against the wrong observatory. Singular on purpose: an instance on manke *is* BTS and one on yagan *is* the summit, and because the same 13-digit dataId exists at both with different obs_end values, an instance that could be pointed at the other one would return answers that looked plausible rather than obviously wrong. Needs `name`, `cluster`, `namespace`, `lokiAddr` and `consdbUrl`; `consdbTokenFile` is omitted because an in-cluster ConsDB Service address never passes through Gafaelfawr and so takes no bearer token. Rendered into the `sites.toml` the application reads. |
| config.windowAfterS | int | `300` | Seconds after shutter close that a fetch window ends. As above, a starting value rather than a cap. Worth raising where the pipeline runs slower than the exposure cadence. |
| config.windowBeforeS | int | `5` | Seconds before shutter close that a fetch window starts. This is the *starting* value of an editable field, not a cap: widening a window to catch a neighbouring exposure is a normal investigative move. |
| config.workers | int | `8` | Parallel log-download workers per fetch. Each is a `logcli` process streaming one pod's window, so this trades cluster load and pod CPU against how long a night-wide fetch takes. |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the log-explorer image |
| image.repository | string | `"ghcr.io/lsst-so/ra_log_explorer"` | Image to use in the log-explorer deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| imagePullSecrets | list | See `values.yaml` | Image pull secrets. Needed only if the GHCR package is made private; a public package pulls without credentials. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| ingress.path | string | `"/log-explorer"` | Path the app is served under. Passed to the application as `RA_LOG_EXPLORER_BASE_PATH` as well as being the ingress path, so the URLs it serves and the URLs the ingress routes cannot drift apart. |
| nodeSelector | object | `{}` | Node selection rules for the log-explorer deployment pod |
| podAnnotations | object | `{}` | Annotations for the log-explorer deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start. Must stay at 1: the log cache is a ReadWriteOnce volume, and loaded exposures live in the serving process's memory, so a second replica would answer with different state depending on which pod the request landed on. |
| resources | object | See `values.yaml` | Resource limits and requests for the log-explorer deployment pod |
| tolerations | list | `[]` | Tolerations for the log-explorer deployment pod |
