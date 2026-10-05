# river-next

SQL and TAP database of Rubin catalog products, with its own ClickHouse server

## Source Code

* <https://github.com/mjuric/mppdb>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the pod |
| clickhouse.affinity | object | Preferred anti-affinity against ephemcache pods | Affinity rules for the ClickHouse pod. The default prefers nodes not running ephemcache's large batch pods. |
| clickhouse.backend | string | `"pod"` | Where the front end's ClickHouse server runs: `pod` (this chart's StatefulSet) or `external` (the same server and data directory run on the failover host, `clickhouse.external.host`). `external` scales the StatefulSet to zero replicas, without deleting it or its claim, and points the front end at the failover host. In both modes the pod template runs the server under an owner guard and wrapper (the `river-next-clickhouse-failover` ConfigMap) that refuse to start while the failover host owns the data directory, so a manual scale-up during a failover still meets the guard. Any other value fails rendering. |
| clickhouse.backgroundPoolSize | int | `16` | `background_pool_size` (threads for merges and mutations) |
| clickhouse.dataSubPath | string | `"repo/dp2_prep/u/mjuric/river-next/clickhouse"` | Path within the storage class's filesystem mounted at `/var/lib/clickhouse` (the server's data directory) |
| clickhouse.external.host | string | `"sdfiana032.sdf.slac.stanford.edu"` | Fully qualified name of the failover host. In `external` mode the front end connects to it on port 8123; in `pod` mode the owner guard refuses to start while it answers `/ping`. Its first label is the name the owner file and heartbeat use for that side. Required. |
| clickhouse.image.digest | string | `"sha256:bca86231e6f8e8969f442135843e44105d54fa61babd84b71f6f7c146f207a8e"` | Digest the tag is pinned to, so the image cannot change under the tag |
| clickhouse.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the ClickHouse image |
| clickhouse.image.repository | string | `"clickhouse/clickhouse-server"` | ClickHouse server image |
| clickhouse.image.tag | string | `"26.8.16.41"` | Tag of the ClickHouse image. 26.8 is an LTS line. Once this server has written data, moving to an older release is not possible. |
| clickhouse.livenessProbe.check | string | `"data"` | What the liveness probe checks: `ping` (HTTP `GET /ping`) or `data` (reads the `status` file ClickHouse writes in its data directory at startup, and pings), so a lost data mount fails the probe |
| clickhouse.livenessProbe.enabled | bool | `true` | Whether the ClickHouse container has a liveness probe at all |
| clickhouse.livenessProbe.failureThreshold | int | `5` | Consecutive liveness failures before the container is restarted |
| clickhouse.livenessProbe.periodSeconds | int | `30` | Seconds between liveness probes |
| clickhouse.livenessProbe.timeoutSeconds | int | `10` | Seconds before a liveness probe counts as failed |
| clickhouse.loadBalancerIP | string | `""` | IP address to pin the LoadBalancer service to, from the `sdf-rubin-ingest` MetalLB pool. Leave empty for the first deployment, then set it to the address MetalLB assigned so it survives the service being recreated. |
| clickhouse.markCacheSize | int | `5368709120` | `mark_cache_size`, in bytes (5 GiB) |
| clickhouse.maxServerMemoryUsageRatio | float | `0.9` | Fraction of the memory limit ClickHouse may use, rendered in bytes as `max_server_memory_usage` |
| clickhouse.maxThreads | int | The integer part of `clickhouse.resources.limits.cpu` | `max_threads` for the default settings profile. Must be set explicitly rather than left to ClickHouse, because the container sees every host core while its cgroup allows far fewer. If set, a positive integer; unset or 0 uses the default. |
| clickhouse.nodeSelector | object | `{"edu.stanford.slac.sdf.project/rsp":"true"}` | Node selector rules for the ClickHouse pod |
| clickhouse.pdb.enabled | bool | `true` | Whether to create a PodDisruptionBudget (`minAvailable: 1`) for the ClickHouse pod, which blocks voluntary evictions such as node drains |
| clickhouse.podAnnotations | object | `{}` | Annotations for the ClickHouse pod |
| clickhouse.podSecurityContext | object | `{"runAsGroup":1126,"runAsNonRoot":true,"runAsUser":18728}` | Pod security context. The pod runs as the uid and gid that own the data directory on the host filesystem. Never add `fsGroup`: the volume is a hostPath holding existing data, which must not be chowned (rendering fails on `fsGroup` or `fsGroupChangePolicy`). `runAsUser` and `runAsNonRoot: true` are required. |
| clickhouse.resources | object | `{"limits":{"cpu":"64","memory":"384Gi"},"requests":{"cpu":"64","memory":"384Gi"}}` | Resource requests and limits for the ClickHouse pod. Requests must equal limits (rendering fails otherwise). `max_server_memory_usage` and the default `max_threads` are derived from the limits. |
| clickhouse.startupProbe.failureThreshold | int | `180` | Startup probe failures allowed before the container is restarted. With the default period this allows 30 minutes for metadata loading. |
| clickhouse.startupProbe.periodSeconds | int | `10` | Seconds between startup probes |
| clickhouse.storageClassName | string | `"sdf-data-rubin"` | Storage class of the claim holding the data and staging directories. Its volumes are a hostPath on the whole `/sdf/data/rubin` filesystem with a `Delete` reclaim policy: patch the bound PV to `Retain` before anything may delete the claim. |
| clickhouse.terminationGracePeriodSeconds | int | `300` | Seconds the server is given to shut down cleanly before it is killed |
| clickhouse.tolerations | list | `[{"effect":"NoSchedule","key":"edu.stanford.slac.sdf.project/rsp","operator":"Equal","value":"true"}]` | Tolerations for the ClickHouse pod |
| clickhouse.uncompressedCacheSize | int | `8589934592` | `uncompressed_cache_size`, in bytes (8 GiB) |
| clickhouse.userFilesSubPath | string | `"repo/dp2_prep/u/mjuric/river-next/user-files"` | Path within the storage class's filesystem mounted at `/var/lib/clickhouse-user-files` (`user_files_path`, where ingest stages files for `file()`) |
| command | list | `["mppdb","up"]` | Command to run in the container. `mppdb up` starts and supervises the service stack, which is what the container image's start script does. |
| config.advertiseRequestBase | bool | `true` | Whether the service advertises the URL a client actually reached it on (True) or pins the configured `baseUrl` for every generated URL (False). Behind a TLS-terminating proxy the pod sees plain http, so leaving this True mints `http://` job/redirect URLs the https console then blocks; set it False so async job and result URLs are pinned to the external https `baseUrl`. TOML-only (no env var), so it is rendered into the mppdb.toml ConfigMap. |
| config.authProvider | string | `"apikey"` | Identity provider, supplied as `MPPDB_AUTH_PROVIDER`. `apikey` validates the service's own API keys and is what the initial smoke deployment uses; this flips to `gafaelfawr` once the service can consume the identity headers injected by the ingress. |
| config.baseUrl | string | `global.baseUrl` plus `ingress.pathPrefix` | Public base URL the service advertises in generated URLs, supplied as `MPPDB_BASE_URL`. Leave empty so it follows `ingress.pathPrefix`. |
| config.branding | object | `{}` | Display branding, rendered into the `[branding]` table of the generated `mppdb.toml` as string keys. Empty omits the table, leaving the image's built-in branding. If the table is non-empty and has no `public_url`, the chart adds one equal to the service's base URL, so it follows `ingress.pathPrefix`. |
| config.clickhouse.host | string | `"river-next-clickhouse.river-next.svc.cluster.local"` | Host name of the ClickHouse server, supplied as `MPPDB_CLICKHOUSE_HOST`. The chart runs its own ClickHouse server, so this is that server's in-cluster Service name. |
| config.clickhouse.port | int | `8123` | HTTP port of the ClickHouse server, supplied as `MPPDB_CLICKHOUSE_PORT` |
| config.configPath | string | `"/etc/mppdb/mppdb.toml"` | Container path the generated `mppdb.toml` is mounted at, supplied as `MPPDB_CONFIG` |
| config.dataDir | string | `"/data"` | Container path of the persistent data directory, supplied as `MPPDB_DATA_DIR`. The state database, spool, lake, and manifests all live beneath it, and it is where the PVC is mounted. |
| config.databases | object | `dp2`, `ppdb`, and `ssp`; see `values.yaml` | Databases to serve, rendered into the `[databases]` tables of the generated `mppdb.toml`. This block is the authorization boundary: a database absent here is not served, whatever the catalog store holds. `chDatabase` is the physical ClickHouse database. `manifestsDir` and `lakeDir` are set only for databases that have a Parquet lake and snapshot pointer; static ClickHouse-only imports leave them out. A `registry` key is also accepted, resolved against `config.registryDir`, but it is **ignored under `MPPDB_ENGINE=clickhouse`**, which this deployment uses: the catalog comes from `TAP_SCHEMA.registries` in the store. Do not set it here. |
| config.defaultDatabase | string | `""` | Database that unqualified ADQL table names resolve to, written to `default_database` in the TOML configuration. **Empty on purpose**: with no default, every table reference must be qualified as `database.table`, which is what we want now that the obsolete `mppdb` database is gone and no single database is the natural home for a bare name. Setting this omits the TOML key entirely; it must name one of the `databases` entries if set at all. |
| config.engine | string | `"clickhouse"` | Query engine, supplied as `MPPDB_ENGINE`. `clickhouse` runs ADQL against a ClickHouse server over HTTP rather than against a local DuckDB. |
| config.extraEnv | object | `{}` | Additional environment variables for the container, as a mapping of name to value. Use this for `MPPDB_*` settings that have no dedicated value above. Never put credentials here; they come from the `river-next` secret. |
| config.host | string | `"0.0.0.0"` | Address the service binds to, supplied as `MPPDB_HOST`. The service defaults this to loopback, which would make the pod unreachable. |
| config.manifestsDir | string | `"/data/manifests"` | Directory holding the snapshot manifests, supplied as `MPPDB_MANIFESTS_DIR`. Must be set explicitly: leaving it unset silently yields an empty snapshot. |
| config.metricsAddr | string | `"0.0.0.0"` | Address the metrics server binds to, supplied as `MPPDB_METRICS_ADDR`. The service defaults this to loopback, which would make the metrics port unreachable from outside the pod. |
| config.metricsPort | int | `9100` | Port the Prometheus metrics server listens on, supplied as `MPPDB_METRICS_PORT` |
| config.port | int | `8080` | Port the service listens on, supplied as `MPPDB_PORT` |
| config.registryDir | string | `"/opt/mppdb/deploy/usdf"` | Directory **inside the image** holding the registry YAML files that the `[databases]` entries below refer to. **PLACEHOLDER**: confirm this against the published image at integration time; nothing in this chart can verify it. |
| config.scsDatabase | string | `"dp2"` | Database that Simple Cone Search resolves its table against. Independent of `defaultDatabase` -- SCS targets exactly one database, and with no default it would otherwise refuse every request. Must be a `databases` entry. |
| config.scsDefaultTable | string | `"DiaObject"` | Bare table name SCS uses when the request omits one. Must exist in `scsDatabase`; note `dp2` has `DiaObject` and no `DiaObjectLast`. |
| config.spoolDir | string | `"/spool"` | Container path the spool claim is mounted at, supplied as `MPPDB_SPOOL_DIR`. Separate volume; see `persistence.spoolSize`. |
| config.spoolWatermarkBytes | string | `"1924145348608"` | Byte ceiling above which new async jobs are refused with 503 + Retry-After, written to `MPPDB_SPOOL_WATERMARK_BYTES`. The image default is 1 TiB, which on a 2 TiB spool would strand half the volume; but the watermark must also stay far enough below capacity that the results already in flight when it trips can still finish, or it fires only once the disk is already full — which is the ENOSPC this whole arrangement exists to prevent. Headroom is therefore sized from the worst case: `max_result_bytes` is 16 GiB and the heavy tier allows 16 concurrent jobs, so 256 GiB can legitimately be mid-write. 2 TiB - 256 GiB = 1.75 TiB, or 87.5% of the volume usable. Quoted: unquoted, YAML reads 13 digits as a float and Helm renders it as 1.924145348608e+12, which the service's integer parser rejects. |
| config.tmpDir | string | `"/data/tmp"` | Directory used for temporary spill files, supplied as `TMPDIR`. Kept on the persistent volume rather than in `/tmp`, which is a small in-memory emptyDir. |
| config.tokenFile | string | `"~/.river.token"` | Path the console's PyVO and TOPCAT recipes (and the .ipynb export) tell users to keep their token in, written to `MPPDB_TOKEN_FILE`. A top-level service setting, NOT branding: it is a path, not a display string. Must differ from other front-ends' — the accounts deployment keeps `~/.mppdb.token`, so a user of both does not have them collide in one file. |
| config.tokenPageUrl | string | `""` | URL of the identity provider's token-creation page, supplied as `MPPDB_TOKEN_PAGE_URL`. Shown by the console's token guidance in `gafaelfawr` auth mode; empty hides the link and tells the user to ask the operator. |
| config.useVaultSecret | bool | `false` | Whether to create a `VaultSecret` for the `river-next` secret. When false, the secret is expected to have been created by hand, which is how the initial smoke deployment works. |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the image. Use `Always` where the tag is mutable, such as a branch name. |
| image.pullSecrets | list | `[]` | Names of image pull secrets in the app's namespace, for a private registry. `ghcr.io/mjuric/mppdb` is private (the image bakes the source of a private repository), so pulling it requires one; at usdfdev this is the hand-created `river-next-pull` docker-registry secret (a `read:packages` GitHub PAT), managed the same way as the `river-next` secret until Vault access exists. |
| image.repository | string | `"ghcr.io/mjuric/mppdb"` | Image to run, built by the `mppdb` repository |
| image.tag | string | `"sha-PLACEHOLDER"` | Tag of the image to run. **PLACEHOLDER**: no image has been published yet, so this must be replaced with a real tag (and pinned per environment) before the chart is deployed. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| ingress.authType | string | `"basic"` | Authentication challenge Gafaelfawr issues on a 401. `basic` matches the other TAP services, and lets VO clients that only speak HTTP basic send a token as the password. |
| ingress.pathPrefix | string | `"/river-next"` | URL path the service is served under. The service itself serves at the root, so the ingress rewrites this prefix away. `/river-next` while this deployment is being validated; it becomes `/river` at cutover. This is the only place the path is set: the ingresses, the advertised base URL and the branding's public URL are all derived from it. |
| ingress.scope | string | `"read:tap"` | Gafaelfawr scope required to reach the service. `read:tap` is the scope every other TAP service in Phalanx requires. |
| ingress.timeout | int | `1800` | Timeout for proxied requests, in seconds. Synchronous ADQL queries can run for a long time, and the nginx default of 60s would cut them off. |
| ingress.useAuthorization | bool | `false` | Whether Gafaelfawr should replace the client's `Authorization` header with the delegated internal token. Must stay false while `config.authProvider` is `apikey`, because the service validates that header itself. |
| nodeSelector | object | `{}` | Node selector rules for the pod |
| persistence.size | string | `"20Gi"` | Size of the claim for `config.dataDir` |
| persistence.spoolSize | string | `"2Ti"` | Size of the separate spool claim, which holds async query results. Sized far above the data claim because a single result can be tens of GiB and results are retained for 7 days; the per-user `spool_quota_bytes` only means anything if the volume is larger than the quota. |
| persistence.storageClassName | string | `"wekafs--sdf-k8s01"` | Storage class backing the claim. `wekafs--sdf-k8s01` is the Weka-backed dynamic provisioner used by every other USDF application that needs a read-write-once volume. Omit to use the cluster default. |
| podAnnotations | object | `{}` | Annotations for the pod |
| podSecurityContext | object | `{"fsGroup":1000,"runAsGroup":1000,"runAsNonRoot":true,"runAsUser":1000}` | Security context for the pod. `fsGroup` is what makes the persistent volume writable by the unprivileged service user, so it must match the uid and gid the image runs as. |
| resources | object | `{"limits":{"cpu":"4","memory":"8Gi"},"requests":{"cpu":"2","memory":"4Gi"}}` | Resource requests and limits. **Guess**: this is a query front end, not the database, so it is sized for request handling and result spooling rather than for scans. Revisit once real query load has been measured. |
| tolerations | list | `[]` | Tolerations for the pod |
