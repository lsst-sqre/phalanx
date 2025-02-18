# mobu

Continuous integration testing

**Homepage:** <https://mobu.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/mobu>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the mobu frontend pod |
| config.autostart | list | `[]` | Autostart specification. Must be a list of mobu flock specifications. Each flock listed will be automatically started when mobu is started. |
| config.availableServices | list | `[]` | Which applications (tap, butler, etc.) are available in this environment. Notebooks can specify a `mobu.required_services` list in their metadata, and mobu will only run them if all services in that list are in this `availableServices` list. See [the Mobu documentation](https://mobu.lsst.io/user_guide/in_repo_config.html#service-specific-notebooks) |
| config.githubCiApp | string | disabled. | Configuration for the GitHub CI app integration. See [the Mobu documentation](https://mobu.lsst.io/operations/github_ci_app.html#add-phalanx-configuration) |
| config.githubRefreshApp | string | disabled. | Configuration for the GitHub refresh app integration. See [the Mobu documentation](https://mobu.lsst.io/operations/github_refresh_app.html#add-phalanx-configuration) |
| config.logLevel | string | `"INFO"` | Log level. Set to 'DEBUG' to include the output from all flocks in the main mobu log. |
| config.metrics.application | string | `"mobu"` | Name under which to log metrics. Generally there is no reason to change this. |
| config.metrics.enabled | bool | `false` | Whether to enable sending metrics |
| config.metrics.events.topicPrefix | string | `"lsst.square.metrics.events"` | Topic prefix for events. It may sometimes be useful to change this in development environments. |
| config.metrics.schemaManager.registryUrl | string | Sasquatch in the local cluster | URL of the Confluent-compatible schema registry server |
| config.metrics.schemaManager.suffix | string | `""` | Suffix to add to all registered subjects. This is sometimes useful for experimentation during development. |
| config.pathPrefix | string | `"/mobu"` | Prefix for mobu's API routes. |
| config.profile | string | `"production"` | One of 'production' or 'development'. 'production' configures structured JSON logging, and 'development' configures unstructured human readable logging. |
| config.sentryEnvironment | string | `nil` | The environment to report to Sentry |
| config.sentryTracesSampleConfig | float | `0` | Sentry tracing config: a float to specify a percentage, or "errors" to send all transactions with errors. |
| config.slackAlerts | bool | `true` | Whether to send alerts and status to Slack. |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the mobu image |
| image.repository | string | `"ghcr.io/lsst-sqre/mobu"` | mobu image to use |
| image.tag | string | The appVersion of the chart | Tag of mobu image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| nodeSelector | object | `{}` | Node selector rules for the mobu frontend pod |
| podAnnotations | object | `{}` | Annotations for the mobu frontend pod |
| resources | object | See `values.yaml` | Resource limits and requests for the mobu frontend pod |
| terminationGracePeriodSeconds | string | Use the Kubernetes default | Number of seconds for Kubernetes to send SIGKILL after sending SIGTERM |
| tolerations | list | `[]` | Tolerations for the mobu frontend pod |
