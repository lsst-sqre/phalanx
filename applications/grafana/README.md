# grafana

Grafana observability visualization tooling

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy sidecar, used with Cloud SQL databases on Google Cloud |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.tag | string | `"1.37.10"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | None, must be set if Cloud SQL is used | Instance connection name for a Cloud SQL PostgreSQL instance |
| cloudsql.resources | object | See `values.yaml` | Resource limits and requests for the Cloud SQL Proxy container |
| cloudsql.serviceAccount | string | None, must be set if Cloud SQL Auth Proxy is enabled | The Google service account that has an IAM binding to the `grafana` Kubernetes service account and has the `cloudsql.client` role |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| grafana | object | See values.yaml | Config for the Grafana instance |
| grafana-operator | object | [chart values](https://github.com/grafana/grafana-operator/blob/master/deploy/helm/grafana-operator/values.yaml) | Config for the grafana-operator, which is a dependency of this chart |
| grafana.authProxy | object | `{"enabled":true}` | Whether auth proxy is enabled. We always want to run with this enabled and depend on Gafaelfawr to handle requests. Only once during the configuration of a new instance (when we need to make an auth-proxy user the instance admin) should we ever turn this off. |
| grafana.config | object | `{"admin_user":"grafana-admin","database":{"host":"localhost","name":"grafana","type":"postgres","user":"grafana"},"log":{"level":"info"},"users":{"auto_assign_org":"true","auto_assign_org_role":"Editor"}}` | Config for the Grafana CRD spec config options. [Docs](https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/) |
| grafana.gafaelfawrScopes | object | `{"all":["exec:internal-tools"]}` | Gafaelfawr scopes that can access Grafana See the [Gafaelfawr docs](https://gafaelfawr.lsst.io/user-guide/gafaelfawringress.html#config-section) |
| grafana.ingress | object | `{"annotations":{}}` | Config for the Gafaelfawr ingress |
| grafana.ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| grafana.pathPrefix | string | `"grafana"` | Path prefix for Grafana. |
| grafana.slackAlerts | object | `{"enabled":true}` | Whether the contact point for the general Slack contact point is configured. It will notify to the standard RSP alert Slack channel |
| grafana.spec | object | `{"persistentVolumeClaim":{"spec":{"accessModes":["ReadWriteOnce"],"resources":{"requests":{"storage":"10Gi"}},"storageClassName":null}},"resources":{"limits":{"cpu":"1","memory":"1Gi"},"requests":{"cpu":"100m","memory":"256Mi"}}}` | Config for the Grafana CRD spec. [Docs](https://grafana.github.io/grafana-operator/docs/api/#grafanaspec) |
