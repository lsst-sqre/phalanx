# ppdb-replication

Replicates data from the APDB to the PPDB

## Source Code

* <https://github.com/lsst/dax_ppdb>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the ppdb-replication deployment pod |
| config.additionalS3ProfileName | string | `"embargo"` | S3 profile name for additional S3 profile |
| config.additionalS3ProfileUrl | string | `"https://sdfembs3.sdf.slac.stanford.edu"` | S3 profile URL for additional S3 profile |
| config.apdbConfig | string | `nil` | APDB config file resource |
| config.apdbIndexUri | string | `"/sdf/group/rubin/shared/apdb_config/apdb-index.yaml"` | APDB index URI |
| config.batchSize | int | `1000` | Size of record batches when writing parquet files |
| config.checkInterval | int | `30` | Time to wait before checking for new chunks, if no chunk appears |
| config.dataset | string | `nil` | Target BigQuery dataset |
| config.disableBucketValidation | int | `1` | Disable bucket validation in LSST S3 tools |
| config.gcsBucket | string | `nil` | GCS bucket name |
| config.gcsPrefix | string | `nil` | GCS bucket prefix |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.maxWaitTime | int | `3600` | Maximum time to wait before replicating a chunk after next chunk appears |
| config.minWaitTime | int | `60` | Minimum time to wait before replicating a chunk after next chunk appears |
| config.monLogger | string | `"lsst.dax.ppdb.monitor"` | Name of logger for monitoring |
| config.monRules | string | `nil` | Comma-separated list of monitoring filter rules |
| config.pathPrefix | string | `"/ppdb-replication"` | URL path prefix |
| config.ppdbConfig | string | `nil` | PPDB config file resource |
| config.s3EndpointUrl | string | `"https://s3dfrgw.slac.stanford.edu"` | S3 endpoint URL |
| config.stagingDirectory | string | `nil` | Staging directory for replicated data |
| config.updateExisting | bool | `false` | Allow updates to already replicated data |
| config.uploadInterval | int | `0` | Time to wait between uploader file uploads |
| config.waitInterval | int | `60` | Time to wait between uploader file scans |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"Always"` | Pull policy for the ppdb-replication image |
| image.repository | string | `"ghcr.io/lsst/ppdb-replication"` | Image to use in the ppdb-replication deployment |
| image.tag | string | The appVersion of the chart | Tag of dax_ppdb image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the ppdb-replication deployment pod |
| podAnnotations | object | `{}` | Annotations for the ppdb-replication deployment pod |
| replicaCount | int | `1` | Number of deployment pods to start |
| resources | object | see `values.yaml` | Resource limits and requests for the ppdb-replication deployment pod |
| tolerations | list | `[]` | Tolerations for the ppdb-replication deployment pod |
