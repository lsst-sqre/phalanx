# repertoire

Service discovery

**Homepage:** <https://repertoire.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/repertoire>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the repertoire deployment pod |
| config.applications | list | Set by Argo CD | List of applications deployed in this Phalanx environment (do not set) |
| config.baseHostname | string | Set by Argo CD | Base hostname of the Phalanx environment (do not set) |
| config.butlerConfigs | object | Set by Argo CD | Butler configuration mapping (do not set) |
| config.datasets | list | `[]` | List of datasets served by this environment. Each member of the list is a dictionary with key `name` (human-readable short name of dataset like `dp1`). |
| config.influxdbDatabases | object | `{}` | Dictionary of InfluxDB database names to connection information for that database, with keys `url`, `database`, `username`, `passwordKey`, and `schemaRegistry`. `passwordKey` must match an entry in `secrets.yaml`. |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/repertoire"` | URL path prefix |
| config.rules | object | See `values.yaml` | Rules for determining the expected URLs of deployed services that use the main hostname. See the [Repertoire documentation](https://repertoire.lsst.io/) for more information. |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
| config.subdomainRules | object | See `values.yaml` | Rules for determining the expected URLs of deployed services that use a subdomain. See the [Repertoire documentation](https://repertoire.lsst.io/) for more information. |
| config.useSubdomains | list | `[]` | List of services that use subdomains instead of the main hostname. See the [Repertoire documentation](https://repertoire.lsst.io/) for more information. |
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
| tolerations | list | `[]` | Tolerations for the repertoire deployment pod |
