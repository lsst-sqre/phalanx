# kubernetes-replicator

Kafka secret replicator

**Homepage:** <https://github.com/mittwald/kubernetes-replicator>

## Source Code

* <https://github.com/mittwald/kubernetes-replicator>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| kubernetes-replicator.podSecurityContext.allowPrivilegeEscalation | bool | `false` |  |
| kubernetes-replicator.podSecurityContext.capabilities.drop[0] | string | `"ALL"` |  |
| kubernetes-replicator.podSecurityContext.readOnlyRootFilesystem | bool | `true` |  |
| kubernetes-replicator.securityContext.runAsGroup | int | `1000` |  |
| kubernetes-replicator.securityContext.runAsNonRoot | bool | `true` |  |
| kubernetes-replicator.securityContext.runAsUser | int | `1000` |  |
| kubernetes-replicator.serviceAccount.annotations | object | `{}` |  |
| kubernetes-replicator.serviceAccount.create | bool | `true` |  |
| kubernetes-replicator.serviceAccount.name | string | `nil` |  |
| kubernetes-replicator.serviceAccount.privileges[0].apiGroups[0] | string | `""` |  |
| kubernetes-replicator.serviceAccount.privileges[0].apiGroups[1] | string | `"apps"` |  |
| kubernetes-replicator.serviceAccount.privileges[0].apiGroups[2] | string | `"extensions"` |  |
| kubernetes-replicator.serviceAccount.privileges[0].resources[0] | string | `"secrets"` |  |
| kubernetes-replicator.serviceAccount.privileges[0].resources[1] | string | `"configmaps"` |  |