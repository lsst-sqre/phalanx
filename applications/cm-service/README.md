# cm-service

Campaign Management for Rubin Data Release Production

## Source Code

* <https://github.com/lsst-dm/cm-service>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.db.echo | bool | `false` | Whether to echo SQLAlchemy generated SQL to the log |
| config.db.hostname | string | `""` | Name of the database host |
| config.db.name | string | `"cmservice"` | Name of the database to use for the application |
| config.db.port | int | `5432` | Port number of the database host |
| config.db.username | string | `"cmservice"` | Name of the database user to use for the application |
| config.logLevel | string | `"INFO"` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`) |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.outputVolume.storage | string | `"1Gi"` | Minimum storage requested in service output area PVC |
| config.outputVolume.storageClassName | string | `nil` | If specified, name of storage class requested in service output area PVC |
| config.outputVolume.subPath | string | `nil` | If specified, sub-path within bound PV to be mounted at service output area |
| config.pathPrefix | string | `"/cm-service"` | URL path prefix |
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
| worker.affinity | object | `{}` | Affinity rules for the worker pods |
| worker.htcondor.config.contents | string | `nil` | If specified, contents of htcondor config file to be injected into worker containers |
| worker.htcondor.config.mountPath | string | `nil` | If specified, location for htcondor config file to be injected into worker containers |
| worker.htcondor.fsRemoteDir.storage | string | `"1Gi"` | Minimum storage requested in the condor remote area PVC |
| worker.htcondor.fsRemoteDir.storageClassName | string | `nil` | If specified, name of storage class requested in condor remote area PVC |
| worker.htcondor.fsRemoteDir.subPath | string | `nil` | If specified, sub-path within bound PV to be mounted as condor remote area |
| worker.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the worker image |
| worker.image.repository | string | `"ghcr.io/lsst-dm/cm-worker"` | Image to use for worker containers |
| worker.image.tag | string | The appVersion of the chart | Tag of worker image to use |
| worker.nodeSelector | object | `{}` | Node selection rules for the worker pods |
| worker.podAnnotations | object | `{}` | Annotations for the worker pods |
| worker.replicaCount | int | `1` | Number of worker pods to start |
| worker.resources | object | See `values.yaml` | Resource limits and requests for the worker pods |
| worker.tolerations | list | `[]` | Tolerations for the worker pods |
