# cm-service

Campaign Management for Rubin Data Release Production

## Source Code

* <https://github.com/lsst-dm/cm-service>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.butler.repositories | object | `{}` | A mapping of butler repository names to their URIs that will be known to the service. |
| config.butler.storage | string | `"1Gi"` | Minimum storage requested in the butler remote area PVC |
| config.butler.storageClassName | string | `nil` | If specified, name of storage class requested in butler remote area PVC |
| config.butler.subPath | string | `nil` | If specified, sub-path within bound PV to be mounted as butler remote area |
| config.db.echo | bool | `false` | Whether to echo SQLAlchemy generated SQL to the log |
| config.db.hostname | string | `""` | Name of the database host |
| config.db.name | string | `"cmservice"` | Name of the database to use for the application |
| config.db.port | int | `5432` | Port number of the database host |
| config.db.username | string | `"cmservice"` | Name of the database user to use for the application |
| config.htcondor.collectorHost | string | `nil` | Name of an htcondor collector host |
| config.htcondor.fsRemoteDir.storage | string | `"1Gi"` | Minimum storage requested in the condor fs-remote PVC |
| config.htcondor.fsRemoteDir.storageClassName | string | `nil` | If specified, name of storage class requested for condor fs-remote PVC |
| config.htcondor.fsRemoteDir.subPath | string | `nil` | If specified, sub-path within bound PV to be mounted as condor fs-remote |
| config.htcondor.scheddHost | string | `nil` | If specified, name of an htcondor schedd host |
| config.logLevel | string | `"INFO"` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`) |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.outputVolume.storage | string | `"1Gi"` | Minimum storage requested in service output area PVC |
| config.outputVolume.storageClassName | string | `nil` | If specified, name of storage class requested in service output area PVC |
| config.outputVolume.subPath | string | `nil` | If specified, sub-path within bound PV to be mounted at service output area |
| config.pathPrefix | string | `"/cm-service"` | URL path prefix |
| daemon.affinity | object | `{}` | Affinity rules for the daemon pods |
| daemon.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the daemon image |
| daemon.image.repository | string | `"ghcr.io/lsst-dm/cm-daemon"` | Image to use for daemon containers |
| daemon.image.tag | string | The appVersion of the chart | Tag of daemon image to use |
| daemon.nodeSelector | object | `{}` | Node selection rules for the daemon pods |
| daemon.podAnnotations | object | `{}` | Annotations for the daemon pods |
| daemon.replicaCount | int | `1` | Number of daemon pods to start |
| daemon.resources | object | See `values.yaml` | Resource limits and requests for the daemon pods |
| daemon.tolerations | list | `[]` | Tolerations for the daemon pods |
| frontend.affinity | object | `{}` | Affinity rules for the frontend pods |
| frontend.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the frontend image |
| frontend.image.repository | string | `"ghcr.io/lsst-dm/cm-service"` | Image to use for frontend containers |
| frontend.image.tag | string | The appVersion of the chart | Tag of frontend image to use |
| frontend.nodeSelector | object | `{}` | Node selector rules for the frontend pods |
| frontend.podAnnotations | object | `{}` | Annotations for the frontend pods |
| frontend.replicaCount | int | `1` | Number of frontend pods to start |
| frontend.resources | object | See `values.yaml` | Resource limits and requests for the frontend pods |
| frontend.tolerations | list | `[]` | Tolerations for the frontend pods |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the frontend image |
| image.repository | string | `"ghcr.io/lsst-dm/cm-service"` | Image to use for frontend containers |
| image.tag | string | The appVersion of the chart | Tag of frontend image to use |
| ingress.annotations | object | `{}` | Additional annotations for the frontend ingress rule |
| internalDB | bool | `false` | Whether to use the internal (phalanx) database |
