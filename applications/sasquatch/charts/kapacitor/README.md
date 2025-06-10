# kapacitor

InfluxDB's native data processing engine. It can process both stream and batch data from InfluxDB.

## Source Code

* <https://github.com/influxdata/kapacitor>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | None, must be set if you want to control pod affinity | Affinity for pod assignment |
| namespaceOverride | string | `""` | Override the deployment namespace |
| override_config.toml | string | None, must be specified if you want to override default. | If specified, replace pod config with this TOML |
| persistence.accessMode | string | `"ReadWriteOnce"` | Access mode for persistent volume. Usually should be left alone. |
| persistence.existingClaim | string | `""` | If dynamic provisioning is disabled, use this PVC name for storage |
| persistence.storageClass | string | `nil` | If undefined or null, default provisioner (gp2 on AWS, standard on GKE, AWS & OpenStack); "-" disables dynamic provisioning |
| rbac | object | Enabled, cluster-scoped. See kapacitor `values.yaml` | Role based access control |
| service.type | string | `"ClusterIP"` | K8s Service type; expose (if desired) with LoadBalancer or NodePort |
| serviceAccount | object | Enabled. See kapacitor `values.yaml` | Service account |
| sidecar | object | See kapacitor `values.yaml` | Sidecars to collect the configmaps with specified label and mount their data into specified folders |
| tolerations | list | None, must be set if you want tolerations | Tolerations for pod assignment |
