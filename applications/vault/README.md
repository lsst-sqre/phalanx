# vault

Secret Storage

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| vault.global.namespace | string | `"vault"` |  |
| vault.global.tlsDisable | bool | `true` |  |
| vault.injector.enabled | bool | `false` |  |
| vault.server.dataStorage.enabled | bool | `false` |  |
| vault.server.ha.enabled | bool | `true` |  |
| vault.server.ha.replicas | int | `3` |  |
| vault.server.ingress.annotations."cert-manager.io/cluster-issuer" | string | `"letsencrypt-dns"` |  |
| vault.server.ingress.annotations."kubernetes.io/ingress.class" | string | `"nginx"` |  |
| vault.server.ingress.enabled | bool | `true` |  |
| vault.server.ingress.hosts[0].host | string | `"vault.lsst.cloud"` |  |
| vault.server.ingress.hosts[0].paths[0] | string | `"/"` |  |
| vault.server.ingress.tls[0].hosts[0] | string | `"vault.lsst.cloud"` |  |
| vault.server.ingress.tls[0].secretName | string | `"vault-ingress-tls"` |  |
| vault.server.standalone.enabled | bool | `false` |  |
