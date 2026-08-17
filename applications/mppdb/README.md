# mppdb

TAP query front end for the mppdb catalogs

## Source Code

* <https://github.com/mjuric/mppdb>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the pod |
| command | list | `["mppdb","up"]` | Command to run in the container. `mppdb up` starts and supervises the service stack, which is what the container image's start script does. |
| config.advertiseRequestBase | bool | `true` | Whether the service advertises the URL a client actually reached it on (True) or pins the configured `baseUrl` for every generated URL (False). Behind a TLS-terminating proxy the pod sees plain http, so leaving this True mints `http://` job/redirect URLs the https console then blocks; set it False so async job and result URLs are pinned to the external https `baseUrl`. TOML-only (no env var), so it is rendered into the mppdb.toml ConfigMap. |
| config.authProvider | string | `"apikey"` | Identity provider, supplied as `MPPDB_AUTH_PROVIDER`. `apikey` validates the service's own API keys and is what the initial smoke deployment uses; this flips to `gafaelfawr` once the service can consume the identity headers injected by the ingress. |
| config.baseUrl | string | `global.baseUrl` plus `ingress.pathPrefix` | Public base URL the service advertises in generated URLs, supplied as `MPPDB_BASE_URL`. |
| config.branding | object | `{}` | Display branding, rendered into the `[branding]` table of the generated `mppdb.toml` as string keys. Empty omits the table, leaving the image's built-in branding. |
| config.clickhouse.host | string | `"sdfiana035.sdf.slac.stanford.edu"` | Host name of the ClickHouse server, supplied as `MPPDB_CLICKHOUSE_HOST`. This is **outside** the Kubernetes cluster, so egress from the pod to it must be permitted. |
| config.clickhouse.port | int | `8123` | HTTP port of the ClickHouse server, supplied as `MPPDB_CLICKHOUSE_PORT` |
| config.configPath | string | `"/etc/mppdb/mppdb.toml"` | Container path the generated `mppdb.toml` is mounted at, supplied as `MPPDB_CONFIG` |
| config.dataDir | string | `"/data"` | Container path of the persistent data directory, supplied as `MPPDB_DATA_DIR`. The state database, spool, lake, and manifests all live beneath it, and it is where the PVC is mounted. |
| config.databases | object | `mppdb`, `ppdb`, and `ssp`; see `values.yaml` | Databases to serve, rendered into the `[databases]` tables of the generated `mppdb.toml`. `chDatabase` is the physical ClickHouse database. `registry` is a file name resolved against `config.registryDir`; omitting it loads the registry packaged in the image. `manifestsDir` and `lakeDir` are set only for databases that have a Parquet lake and snapshot pointer; static ClickHouse-only imports leave them out. |
| config.defaultDatabase | string | `"mppdb"` | Database that unqualified ADQL table names resolve to, written to `default_database` in the TOML configuration. Every other database must be addressed as `database.table`. |
| config.engine | string | `"clickhouse"` | Query engine, supplied as `MPPDB_ENGINE`. `clickhouse` runs ADQL against a ClickHouse server over HTTP rather than against a local DuckDB. |
| config.extraEnv | object | `{}` | Additional environment variables for the container, as a mapping of name to value. Use this for `MPPDB_*` settings that have no dedicated value above. Never put credentials here; they come from the `mppdb` secret. |
| config.host | string | `"0.0.0.0"` | Address the service binds to, supplied as `MPPDB_HOST`. The service defaults this to loopback, which would make the pod unreachable. |
| config.manifestsDir | string | `"/data/manifests"` | Directory holding the snapshot manifests, supplied as `MPPDB_MANIFESTS_DIR`. Must be set explicitly: leaving it unset silently yields an empty snapshot. |
| config.metricsAddr | string | `"0.0.0.0"` | Address the metrics server binds to, supplied as `MPPDB_METRICS_ADDR`. The service defaults this to loopback, which would make the metrics port unreachable from outside the pod. |
| config.metricsPort | int | `9100` | Port the Prometheus metrics server listens on, supplied as `MPPDB_METRICS_PORT` |
| config.port | int | `8080` | Port the service listens on, supplied as `MPPDB_PORT` |
| config.registryDir | string | `"/opt/mppdb/deploy/usdf"` | Directory **inside the image** holding the registry YAML files that the `[databases]` entries below refer to. **PLACEHOLDER**: confirm this against the published image at integration time; nothing in this chart can verify it. |
| config.tmpDir | string | `"/data/tmp"` | Directory used for temporary spill files, supplied as `TMPDIR`. Kept on the persistent volume rather than in `/tmp`, which is a small in-memory emptyDir. |
| config.tokenPageUrl | string | `""` | URL of the identity provider's token-creation page, supplied as `MPPDB_TOKEN_PAGE_URL`. Shown by the console's token guidance in `gafaelfawr` auth mode; empty hides the link and tells the user to ask the operator. |
| config.useVaultSecret | bool | `false` | Whether to create a `VaultSecret` for the `mppdb` secret. When false, the secret is expected to have been created by hand, which is how the initial smoke deployment works. |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the image. Use `Always` where the tag is mutable, such as a branch name. |
| image.pullSecrets | list | `[]` | Names of image pull secrets in the app's namespace, for a private registry. `ghcr.io/mjuric/mppdb` is private (the image bakes the source of a private repository), so pulling it requires one; at usdfdev this is the hand-created `mppdb-pull` docker-registry secret (a `read:packages` GitHub PAT), managed the same way as the `mppdb` secret until Vault access exists. |
| image.repository | string | `"ghcr.io/mjuric/mppdb"` | Image to run, built by the `mppdb` repository |
| image.tag | string | `"sha-PLACEHOLDER"` | Tag of the image to run. **PLACEHOLDER**: no image has been published yet, so this must be replaced with a real tag (and pinned per environment) before the chart is deployed. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| ingress.authType | string | `"basic"` | Authentication challenge Gafaelfawr issues on a 401. `basic` matches the other TAP services, and lets VO clients that only speak HTTP basic send a token as the password. |
| ingress.pathPrefix | string | `"/mppdb"` | URL path the service is served under. The service itself serves at the root, so the ingress rewrites this prefix away. |
| ingress.scope | string | `"read:tap"` | Gafaelfawr scope required to reach the service. `read:tap` is the scope every other TAP service in Phalanx requires. |
| ingress.timeout | int | `1800` | Timeout for proxied requests, in seconds. Synchronous ADQL queries can run for a long time, and the nginx default of 60s would cut them off. |
| ingress.useAuthorization | bool | `false` | Whether Gafaelfawr should replace the client's `Authorization` header with the delegated internal token. Must stay false while `config.authProvider` is `apikey`, because the service validates that header itself. |
| nodeSelector | object | `{}` | Node selector rules for the pod |
| persistence.size | string | `"20Gi"` | Size of the claim for `config.dataDir` |
| persistence.storageClassName | string | `"wekafs--sdf-k8s01"` | Storage class backing the claim. `wekafs--sdf-k8s01` is the Weka-backed dynamic provisioner used by every other USDF application that needs a read-write-once volume. Omit to use the cluster default. |
| podAnnotations | object | `{}` | Annotations for the pod |
| podSecurityContext | object | `{"fsGroup":1000,"runAsGroup":1000,"runAsNonRoot":true,"runAsUser":1000}` | Security context for the pod. `fsGroup` is what makes the persistent volume writable by the unprivileged service user, so it must match the uid and gid the image runs as. |
| resources | object | `{"limits":{"cpu":"4","memory":"8Gi"},"requests":{"cpu":"2","memory":"4Gi"}}` | Resource requests and limits. **Guess**: this is a query front end, not the database, so it is sized for request handling and result spooling rather than for scans. Revisit once real query load has been measured. |
| tolerations | list | `[]` | Tolerations for the pod |
