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
| cache.size | string | `"50Gi"` | Size of the cache volume. The application evicts least-recently-used windows to stay under its own `maxCacheBytes` setting, so this is the ceiling rather than an expected steady state. |
| cache.storageClassName | string | `"rook-ceph-block"` | Storage class for the cache volume |
| config.defaultSite | string | the first entry of `config.sites` | Name of the site the UI starts on. |
| config.lokiUsername | string | `"omega"` | Loki HTTP basic-auth username. The password comes from the `loki-password` Vault secret. Setting both server-side means nobody has to type Loki credentials into the browser to use the tool. |
| config.sites | list | See the per-environment values files | Sites the deployment can query. A *site* pairs a Loki cluster (where the logs live) with the ConsDB endpoint that owns shutter-close truth for that cluster's data; the two must match or a dataId resolves against the wrong observatory. Each entry needs `name`, `cluster`, `namespace`, `lokiAddr` and `consdbUrl`, and may carry `consdbTokenFile` — omit that for a ConsDB reached at a cluster-internal Service address, which never passes through Gafaelfawr and so needs no bearer token. Rendered into the `sites.toml` the application reads. |
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
