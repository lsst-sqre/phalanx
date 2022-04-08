# gafaelfawr

Science Platform authentication and authorization system

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the Gafaelfawr frontend pod |
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy sidecar, used with CloudSQL databases on Google Cloud |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.tag | string | `"1.29.0"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | `""` | Instance connection name for a CloudSQL PostgreSQL instance |
| cloudsql.serviceAccount | string | `""` | The Google service account that has an IAM binding to the `gafaelfawr` and `gafaelfawr-tokens` Kubernetes service accounts and has the `cloudsql.client` role |
| config.cilogon.clientId | string | `""` | CILogon client ID. One and only one of this, `config.github.clientId`, or `config.oidc.clientId` must be set. |
| config.cilogon.loginParams | object | `{"skin":"LSST"}` | Additional parameters to add |
| config.cilogon.redirectUrl | string | `/login` at the value of config.host | Return URL given to CILogon (must match the CILogon configuration) |
| config.cilogon.test | bool | `false` | Whether to use the test instance of CILogon |
| config.databaseUrl | string | None, must be set | URL for the PostgreSQL database |
| config.errorFooter | string | `""` | HTML footer to add to any login error page (inside a <p> tag). |
| config.github.clientId | string | `""` | GitHub client ID. One and only one of this, `config.cilogon.clientId`, or `config.oidc.clientId` must be set. |
| config.groupMapping | object | `{}` | Defines a mapping of scopes to groups that provide that scope. Tokens from an OpenID Connect provider such as CILogon that include groups in an `isMemberOf` claim will be granted scopes based on this mapping. |
| config.influxdb.enabled | bool | `false` | Whether to issue tokens for InfluxDB. If set to true, `influxdb-secret` must be set in the Gafaelfawr secret. |
| config.influxdb.username | string | `""` | If set, force all InfluxDB tokens to have that username instead of the authenticated identity of the user requesting a token |
| config.initialAdmins | list | `[]` | Usernames to add as administrators when initializing a new database. Used only if there are no administrators. |
| config.knownScopes | object | See the `values.yaml` file | Names and descriptions of all scopes in use. This is used to populate the new token creation page. Only scopes listed here will be options when creating a new token. |
| config.ldap.baseDn | string | None, must be set | Base DN for the LDAP search to find a user's groups |
| config.ldap.groupMemberAttr | string | `"member"` | Member attribute of the object class. Values must match the username returned in the token from the OpenID Connect authentication server. |
| config.ldap.groupObjectClass | string | `"posixGroup"` | Object class containing group information |
| config.ldap.uidAttr | string | `"uidNumber"` | Attribute containing the user's UID number (only used if uidBaseDn is set) |
| config.ldap.uidBaseDn | string | Get the UID number from the upstream authentication provider | Base DN for the LDAP search to find a user's UID number |
| config.ldap.url | string | Do not use LDAP | LDAP server URL from which to retrieve user group information |
| config.loglevel | string | `"INFO"` | Choose from the text form of Python logging levels |
| config.oidc.audience | string | Value of `config.oidc.clientId` | Audience for the JWT token |
| config.oidc.clientId | string | `""` | Client ID for generic OpenID Connect support. One and only one of this, `config.cilogon.clientId`, or `config.github.clientId` must be set. |
| config.oidc.issuer | string | None, must be set | Issuer for the JWT token |
| config.oidc.loginParams | object | `{}` | Additional parameters to add to the login request |
| config.oidc.loginUrl | string | None, must be set | URL to which to redirect the user for authorization |
| config.oidc.scopes | list | `["openid"]` | Scopes to request from the OpenID Connect provider |
| config.oidc.tokenUrl | string | None, must be set | URL from which to retrieve the token for the user |
| config.oidcServer.enabled | bool | `false` | Whether to support OpenID Connect clients. If set to true, `oidc-server-secrets` must be set in the Gafaelfawr secret. |
| config.proxies | list | [`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`] | List of netblocks used for internal Kubernetes IP addresses, used to determine the true client IP for logging |
| config.tokenLifetimeMinutes | int | `43200` (30 days) | Session length and token expiration (in minutes) |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the Gafaelfawr image |
| image.repository | string | `"lsstsqre/gafaelfawr"` | Gafaelfawr image to use |
| image.tag | string | The appVersion of the chart | Tag of Gafaelfawr image to use |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the Gafaelfawr frontend pod |
| podAnnotations | object | `{}` | Annotations for the Gafaelfawr frontend pod |
| redis.affinity | object | `{}` | Affinity rules for the Redis pod |
| redis.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the Redis image |
| redis.image.repository | string | `"redis"` | Redis image to use |
| redis.image.tag | string | `"6.2.6"` | Redis image tag to use |
| redis.nodeSelector | object | `{}` | Node selection rules for the Redis pod |
| redis.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode of storage to request |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage and thus tokens. Setting this to false will use `emptyDir` and reset all tokens on every restart. Only use this for a test deployment. |
| redis.persistence.size | string | `"1Gi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `""` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `""` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.podAnnotations | object | `{}` | Pod annotations for the Redis pod |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
| replicaCount | int | `1` | Number of web frontend pods to start |
| resources | object | `{}` | Resource limits and requests for the Gafaelfawr frontend pod |
| tokens.affinity | object | `{}` | Affinity rules for the token management pod |
| tokens.nodeSelector | object | `{}` | Node selection rules for the token management pod |
| tokens.podAnnotations | object | `{}` | Annotations for the token management pod |
| tokens.resources | object | `{}` | Resource limits and requests for the Gafaelfawr token management pod |
| tokens.tolerations | list | `[]` | Tolerations for the token management pod |
| tolerations | list | `[]` | Tolerations for the Gafaelfawr frontend pod |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.5.0](https://github.com/norwoodj/helm-docs/releases/v1.5.0)
