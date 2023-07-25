# gafaelfawr

Authentication and identity system

**Homepage:** <https://gafaelfawr.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/gafaelfawr>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the Gafaelfawr frontend pod |
| cloudsql.affinity | object | `{}` | Affinity rules for the Cloud SQL Proxy pod |
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy, used with CloudSQL databases on Google Cloud. This will be run as a sidecar for the main Gafaelfawr pods, and as a separate service (behind a `NetworkPolicy`) for other, lower-traffic services. |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.tag | string | `"1.33.9"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | None, must be set if Cloud SQL Auth Proxy is enabled | Instance connection name for a CloudSQL PostgreSQL instance |
| cloudsql.nodeSelector | object | `{}` | Node selection rules for the Cloud SQL Proxy pod |
| cloudsql.podAnnotations | object | `{}` | Annotations for the Cloud SQL Proxy pod |
| cloudsql.resources | object | `{}` | Resource limits and requests for the Cloud SQL Proxy pod |
| cloudsql.serviceAccount | string | None, must be set if Cloud SQL Auth Proxy is enabled | The Google service account that has an IAM binding to the `gafaelfawr` Kubernetes service account and has the `cloudsql.client` role |
| cloudsql.tolerations | list | `[]` | Tolerations for the Cloud SQL Proxy pod |
| config.cilogon.clientId | string | `""` | CILogon client ID. One and only one of this, `config.github.clientId`, or `config.oidc.clientId` must be set. |
| config.cilogon.enrollmentUrl | string | Login fails with an error | Where to send the user if their username cannot be found in LDAP |
| config.cilogon.gidClaim | string | Do not set a primary GID | Claim from which to get the primary GID (only used if not retrieved from LDAP or Firestore) |
| config.cilogon.groupsClaim | string | `"isMemberOf"` | Claim from which to get the group membership (only used if not retrieved from LDAP) |
| config.cilogon.loginParams | object | `{"skin":"LSST"}` | Additional parameters to add |
| config.cilogon.test | bool | `false` | Whether to use the test instance of CILogon |
| config.cilogon.uidClaim | string | `"uidNumber"` | Claim from which to get the numeric UID (only used if not retrieved from LDAP or Firestore) |
| config.cilogon.usernameClaim | string | `"uid"` | Claim from which to get the username |
| config.databaseUrl | string | None, must be set if neither `cloudsql.enabled` | URL for the PostgreSQL database nor `config.internalDatabase` are true |
| config.errorFooter | string | `""` | HTML footer to add to any login error page (will be enclosed in a <p> tag). |
| config.firestore.project | string | Firestore support is disabled | If set, assign UIDs and GIDs using Google Firestore in the given project. Cloud SQL must be enabled and the Cloud SQL service account must have read/write access to that Firestore instance. |
| config.forgerock.url | string | ForgeRock Identity Management support is disabled | If set, obtain the GIDs for groups from this ForgeRock Identity Management server. |
| config.forgerock.username | string | None, must be set if `config.forgerock.url` is set | Username to use for HTTP Basic authentication to ForgeRock Identity Managemnt. The corresponding password must be in the `forgerock-passsword` key of the Gafaelfawr Vault secret. |
| config.github.clientId | string | `""` | GitHub client ID. One and only one of this, `config.cilogon.clientId`, or `config.oidc.clientId` must be set. |
| config.groupMapping | object | `{}` | Defines a mapping of scopes to groups that provide that scope. See [DMTN-235](https://dmtn-235.lsst.io/) for more details on scopes. |
| config.initialAdmins | list | `[]` | Usernames to add as administrators when initializing a new database. Used only if there are no administrators. |
| config.internalDatabase | bool | `false` | Whether to use the PostgreSQL server internal to the Kubernetes cluster |
| config.knownScopes | object | See the `values.yaml` file | Names and descriptions of all scopes in use. This is used to populate the new token creation page. Only scopes listed here will be options when creating a new token. See [DMTN-235](https://dmtn-235.lsst.io/). |
| config.ldap.addUserGroup | bool | `false` | Whether to synthesize a user private group for each user with a GID equal to their UID |
| config.ldap.emailAttr | string | `"mail"` | Attribute containing the user's email address |
| config.ldap.gidAttr | string | Use GID of user private group | Attribute containing the user's primary GID (set to `gidNumber` for most LDAP servers) |
| config.ldap.groupBaseDn | string | None, must be set | Base DN for the LDAP search to find a user's groups |
| config.ldap.groupMemberAttr | string | `"member"` | Member attribute of the object class. Values must match the username returned in the token from the OpenID Connect authentication server. |
| config.ldap.groupObjectClass | string | `"posixGroup"` | Object class containing group information |
| config.ldap.kerberosConfig | string | Use anonymous binds | Enable GSSAPI (Kerberos) binds to LDAP using this `krb5.conf` file. If set, `ldap-keytab` must be set in the Gafaelfawr Vault secret. Set either this or `userDn`, not both. |
| config.ldap.nameAttr | string | `"displayName"` | Attribute containing the user's full name |
| config.ldap.uidAttr | string | Get UID from upstream authentication provider | Attribute containing the user's UID number (set to `uidNumber` for most LDAP servers) |
| config.ldap.url | string | Do not use LDAP | LDAP server URL from which to retrieve user group information |
| config.ldap.userBaseDn | string | Get user metadata from the upstream authentication provider | Base DN for the LDAP search to find a user's entry |
| config.ldap.userDn | string | Use anonymous binds | Bind DN for simple bind authentication. If set, `ldap-secret` must be set in the Gafaelfawr Vault secret. Set this or `kerberosConfig`, not both. |
| config.ldap.userSearchAttr | string | `"uid"` | Search attribute containing the user's username |
| config.logLevel | string | `"INFO"` | Choose from the text form of Python logging levels |
| config.oidc.audience | string | Value of `config.oidc.clientId` | Audience for the JWT token |
| config.oidc.clientId | string | `""` | Client ID for generic OpenID Connect support. One and only one of this, `config.cilogon.clientId`, or `config.github.clientId` must be set. |
| config.oidc.enrollmentUrl | string | Login fails with an error | Where to send the user if their username cannot be found in LDAP |
| config.oidc.gidClaim | string | Do not set a primary GID | Claim from which to get the primary GID (only used if not retrieved from LDAP or Firestore) |
| config.oidc.groupsClaim | string | `"isMemberOf"` | Claim from which to get the group membership (only used if not retrieved from LDAP) |
| config.oidc.issuer | string | None, must be set | Issuer for the JWT token |
| config.oidc.loginParams | object | `{}` | Additional parameters to add to the login request |
| config.oidc.loginUrl | string | None, must be set | URL to which to redirect the user for authorization |
| config.oidc.scopes | list | `["openid"]` | Scopes to request from the OpenID Connect provider |
| config.oidc.tokenUrl | string | None, must be set | URL from which to retrieve the token for the user |
| config.oidc.uidClaim | string | `"uidNumber"` | Claim from which to get the numeric UID (only used if not retrieved from LDAP or Firestore) |
| config.oidc.usernameClaim | string | `"sub"` | Claim from which to get the username |
| config.oidcServer.enabled | bool | `false` | Whether to support OpenID Connect clients. If set to true, `oidc-server-secrets` must be set in the Gafaelfawr secret. |
| config.proxies | list | [`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`] | List of netblocks used for internal Kubernetes IP addresses, used to determine the true client IP for logging |
| config.quota | object | `{}` | Quota settings (see [Quotas](https://gafaelfawr.lsst.io/user-guide/helm.html#quotas)). |
| config.slackAlerts | bool | `false` | Whether to send certain serious alerts to Slack. If `true`, the `slack-webhook` secret must also be set. |
| config.tokenLifetimeMinutes | int | `43200` (30 days) | Session length and token expiration (in minutes) |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the Gafaelfawr image |
| image.repository | string | `"ghcr.io/lsst-sqre/gafaelfawr"` | Gafaelfawr image to use |
| image.tag | string | The appVersion of the chart | Tag of Gafaelfawr image to use |
| ingress.additionalHosts | list | `[]` | Defines additional FQDNs for Gafaelfawr.  This doesn't work for cookie or browser authentication, but for token-based services like git-lfs or the webdav server it does. |
| maintenance.affinity | object | `{}` | Affinity rules for Gafaelfawr maintenance and audit pods |
| maintenance.auditSchedule | string | `"30 3 * * *"` | Cron schedule string for Gafaelfawr data consistency audit (in UTC) |
| maintenance.maintenanceSchedule | string | `"5 * * * *"` | Cron schedule string for Gafaelfawr periodic maintenance (in UTC) |
| maintenance.nodeSelector | object | `{}` | Node selection rules for Gafaelfawr maintenance and audit pods |
| maintenance.podAnnotations | object | `{}` | Annotations for Gafaelfawr maintenance and audit pods |
| maintenance.resources | object | `{}` | Resource limits and requests for Gafaelfawr maintenance and audit pods |
| maintenance.tolerations | list | `[]` | Tolerations for Gafaelfawr maintenance and audit pods |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the Gafaelfawr frontend pod |
| operator.affinity | object | `{}` | Affinity rules for the token management pod |
| operator.nodeSelector | object | `{}` | Node selection rules for the token management pod |
| operator.podAnnotations | object | `{}` | Annotations for the token management pod |
| operator.resources | object | `{}` | Resource limits and requests for the Gafaelfawr Kubernetes operator |
| operator.tolerations | list | `[]` | Tolerations for the token management pod |
| podAnnotations | object | `{}` | Annotations for the Gafaelfawr frontend pod |
| redis.affinity | object | `{}` | Affinity rules for the Redis pod |
| redis.config.secretKey | string | `"redis-password"` | Key inside secret from which to get the Redis password (do not change) |
| redis.config.secretName | string | `"gafaelfawr-secret"` | Name of secret containing Redis password (may require changing if fullnameOverride is set) |
| redis.nodeSelector | object | `{}` | Node selection rules for the Redis pod |
| redis.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode of storage to request |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage and thus tokens. Setting this to false will use `emptyDir` and reset all tokens on every restart. Only use this for a test deployment. |
| redis.persistence.size | string | `"1Gi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `""` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `""` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.podAnnotations | object | `{}` | Pod annotations for the Redis pod |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
| replicaCount | int | `1` | Number of web frontend pods to start |
| resources | object | `{}` | Resource limits and requests for the Gafaelfawr frontend pod |
| tolerations | list | `[]` | Tolerations for the Gafaelfawr frontend pod |