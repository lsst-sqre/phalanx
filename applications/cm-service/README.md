# cm-service

Campaign Management for Rubin Data Release Production

## Source Code

* <https://github.com/lsst-dm/cm-service>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.databaseEcho | bool | `false` | Whether to echo SQLAlchemy generated SQL to the log |
| config.logLevel | string | `"INFO"` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`) |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.outputVolume.storage | string | `"1Gi"` | Minimum storage requested in service output area PVC |
| config.outputVolume.storageClassName | string | `nil` | If specified, name of storage class requested in service output area PVC |
| config.outputVolume.subPath | string | `nil` | If specified, sub-path within bound PV to be mounted at service output area |
| config.pathPrefix | string | `"/cm-service/v1"` | URL path prefix |
| frontend.affinity | object | `{}` | Affinity rules for the frontend pods |
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
| redis.config.secretKey | string | `"password"` | Key inside secret from which to get the Redis password (do not change) |
| redis.config.secretName | string | `"redis-secret"` | Name of secret containing Redis password |
| worker.affinity | object | `{}` | Affinity rules for the worker pods |
| worker.htcondor.config.contents | string | `nil` | If specified, contents of htcondor config file to be injected into worker containers |
| worker.htcondor.config.mountPath | string | `nil` | If specified, location for htcondor config file to be injected into worker containers |
| worker.htcondor.fsRemoteDir.storage | string | `"1Gi"` | Minimum storage requested in the condor remote area PVC |
| worker.htcondor.fsRemoteDir.storageClassName | string | `nil` | If specified, name of storage class requested in condor remote area PVC |
| worker.htcondor.fsRemoteDir.subPath | string | `nil` | If specified, sub-path within bound PV to be mounted as condor remote area |
| worker.htcondor.scheddAddress.contents | string | `nil` | If specified, location for htcondor schedd address file to be injected into worker pods |
| worker.htcondor.scheddAddress.mountPath | string | `nil` | If specified, contents of htcondor schedd address file to be injected into worker pods |
| worker.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the worker image |
| worker.image.repository | string | `"ghcr.io/lsst-dm/cm-service-worker"` | Image to use for worker containers |
| worker.image.tag | string | The appVersion of the chart | Tag of worker image to use |
| worker.nodeSelector | object | `{}` | Node selection rules for the worker pods |
| worker.podAnnotations | object | `{}` | Annotations for the worker pods |
| worker.replicaCount | int | `1` | Number of worker pods to start |
| worker.resources | object | See `values.yaml` | Resource limits and requests for the worker pods |
| worker.tolerations | list | `[]` | Tolerations for the worker pods |
