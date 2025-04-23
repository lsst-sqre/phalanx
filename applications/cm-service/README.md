# cm-service

Campaign Management for Rubin Data Release Production

## Source Code

* <https://github.com/lsst-dm/cm-service>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.aws.credentialsFileSecretKey | string | `"aws-credentials-file"` | Key within the AWS secret with the contents of an AWS credentials file |
| config.aws.defaultAccessKeyIdSecretKey | string | `"aws-access-key-id"` | Key within the AWS secret with the ACCESS_KEY_ID for the default profile |
| config.aws.defaultSecretAccessKeySecretKey | string | `"aws-secret-access-key"` | Key within the AWS secret with the SECRET_ACCESS_KEY for the default profile |
| config.aws.profiles | object | `{}` | Named profiles to include in service's AWS config file |
| config.aws.s3EndpointUrl | string | `nil` | URL to use as an S3 (Object Store) Endpoint |
| config.aws.secretName | string | `"cm-service"` | Name of a secret with AWS authn details |
| config.butler.dbAuth.secretKey | string | `""` | The keyname within the secret data dictionary with the dbAuth payload |
| config.butler.dbAuth.secretName | string | `""` | The name of a secret with Butler a dbAuth payload |
| config.butler.repositories | object | `{}` | A mapping of butler repository names to their URIs that will be known to the service. |
| config.butler.storage | string | `"1Gi"` | Minimum storage requested in the butler remote area PVC |
| config.butler.storageClassName | string | `nil` | If specified, name of storage class requested in butler remote area PVC |
| config.butler.subPath | string | `nil` | If specified, sub-path within bound PV to be mounted as butler remote area |
| config.db.echo | bool | `false` | Whether to echo SQLAlchemy generated SQL to the log |
| config.db.hostname | string | `""` | Name of the database host |
| config.db.name | string | `"cmservice"` | Name of the database to use for the application |
| config.db.port | int | `5432` | Port number of the database host |
| config.db.secretKey | string | `"internalDatabasePassword"` | Key within db authn secret with db password |
| config.db.secretName | string | `"cm-service"` | Name of a secret with db authn details |
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
| config.panda.behindLb | string | `"0"` | PanDA host behind load balancer |
| config.panda.idTokenSecretKey | string | `"panda-id-token"` | Secret key for PanDA id-token value |
| config.panda.monitorUrl | string | `nil` | URL of a panda monitor host |
| config.panda.refreshTokenSecretKey | string | `"panda-refresh-token"` | Secret key for PanDA refresh-token value |
| config.panda.secretName | string | `"cm-service"` | Name of Secret with PanDA secrets |
| config.panda.url | string | `nil` | URL of a panda host, used for base, tls, and cache URLs |
| config.panda.useNativeHttplib | string | `"1"` | PanDA Use Native HTTPLib instead of Curl |
| config.panda.verifyHost | string | `"1"` | PanDA host TLS verification |
| config.panda.virtualOrganization | string | `"Rubin"` | PanDA Virtual Organization Name for oidc |
| config.pathPrefix | string | `"/cm-service"` | URL path prefix |
| config.slack.secretName | string | `"cm-service"` | Name of Secret with Slack secrets |
| config.slack.webhookUrlSecretKey | string | `"slack-webhook-url"` | Secret key for Slack webhook URL |
| daemon.affinity | object | `{}` | Affinity rules for the daemon pods |
| daemon.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the daemon image |
| daemon.image.repository | string | `"ghcr.io/lsst-dm/cm-daemon"` | Image to use for daemon containers |
| daemon.image.tag | string | The appVersion of the chart | Tag of daemon image to use |
| daemon.nodeSelector | object | `{}` | Node selection rules for the daemon pods |
| daemon.podAnnotations | object | `{}` | Annotations for the daemon pods |
| daemon.replicaCount | int | `1` | Number of daemon pods to start |
| daemon.resources | object | See `values.yaml` | Resource limits and requests for the daemon pods |
| daemon.security.gid | int | `0` | Effective GID for daemon user |
| daemon.security.uid | int | `0` | Effective UID for daemon user |
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
