# ephemcache

Nightly ephemerides cache generator for mpsky

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| activeDeadlineSeconds | int | `3600` | Deadline for a single run, in seconds, so a wedged job cannot run forever |
| affinity | object | `{}` | Affinity rules for the pod |
| backoffLimit | int | `0` | Number of retries before the Job is considered failed. Zero, because the next scheduled invocation retries anyway. |
| command | string | `"selftest"` | Entrypoint subcommand. `selftest` checks the image and needs no database credential; `run` builds the cache for the current observing night. |
| database.passwordSecretKey | string | `"usdf_mpc_postgres_password"` | Key in this application's Vault secret holding the database password, supplied to the pod as `PGPASSWORD` |
| database.url | string | `""` | SQLAlchemy DSN for the MPC replica, supplied as `MPCDB`. Empty uses the value baked into the image. Must not contain a username or password: it is passed to `get-mpcorb.py` as a command-line argument. |
| database.userSecretKey | string | `"usdf_mpc_postgres_user"` | Key in this application's Vault secret holding the database username, supplied to the pod as `PGUSER` |
| failedJobsHistoryLimit | int | `3` | Number of failed Jobs to retain |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the image. Use `Always` where the tag is mutable, such as a branch name. |
| image.repository | string | `"ghcr.io/mjuric/lsst-gen-ephemcache"` | Image to run, built by the `lsst-gen-ephemcache` repository |
| image.tag | string | `"u-mjuric-ephemcache"` | Tag of the image to run |
| logToFile | bool | `false` | Whether to also write each run's log to a file under the output directory. Logs always go to stdout; this is a durable second copy that outlives the pod. |
| ncores | string | `""` | Value of `NCORES`, which bounds sorcha's parallelism. Must match `resources.limits.cpu`: the scripts otherwise default it to `nproc`, which reports the node's core count rather than the pod's limit. |
| nodeSelector | object | `{}` | Node selector rules for the pod |
| outputDirMount.claimName | string | `"sdf-group-rubin"` | Name shared by the PVC, its storage class, and the pod volume |
| outputDirMount.enabled | bool | `false` | Whether to mount the shared filesystem that output is published to. When disabled, output goes to an emptyDir and is discarded with the pod. |
| outputDirMount.storageClassName | string | `"sdf-group-rubin"` | Storage class backing the claim |
| outputDirMount.subPath | string | `"web_data/mpsky-data/test"` | Path within that filesystem to expose. Only this subtree is visible to the container, so widening it is a deliberate change. |
| podSecurityContext | object | `{}` | Security context for the pod |
| resources | object | `{"limits":{"cpu":"1","memory":"2Gi"},"requests":{"cpu":"1","memory":"2Gi"}}` | Resource requests and limits. Sized for `selftest`; a real `run` needs far more, and must be raised together with `ncores`. |
| schedule | string | `"0 */3 * * *"` | Cron schedule for the cache build. Runs are idempotent and skip when the cache for the current observing night already exists, so this only has to be frequent enough to catch the night. |
| successfulJobsHistoryLimit | int | `3` | Number of completed Jobs to retain |
| suspend | bool | `true` | Whether to suspend the CronJob |
| tolerations | list | `[]` | Tolerations for the pod |
