# postgres

Postgres RDBMS for LSP

## Source Code

* <https://github.com/lsst-sqre/rsp-postgres>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| debug | string | `""` | Set to non-empty to enable debugging output |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the postgres image |
| image.repository | string | `"lsstsqre/lsp-postgres"` | postgres image to use |
| image.tag | string | The appVersion of the chart | Tag of postgres image to use |
| postgresStorageClass | string | `"standard"` | Storage class for postgres volume.  Set to appropriate value for your deployment: at GKE, "standard" (if you want SSD, "premium-rwo", but if you want a good database maybe it's better to use a cloud database?), on Rubin Observatory Rancher, "rook-ceph-block", elsewhere probably "standard" |
| postgresVolumeSize | string | `"1Gi"` | Volume size for postgres.  It can generally be very small |
| volumeName | string | `""` | Volume name for postgres, if you use an existing volume that isn't automatically created from the PVC by the storage driver. |
