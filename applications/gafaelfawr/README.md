# gafaelfawr

Authentication and identity system

**Homepage:** <https://gafaelfawr.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/gafaelfawr>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the Gafaelfawr frontend pod |
| cloudsql.affinity | object | `{}` | Affinity rules for the standalone Cloud SQL Proxy pod |
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy, used with Cloud SQL databases on Google Cloud. This will be run as a sidecar for the main Gafaelfawr pods, and as a separate service (behind a `NetworkPolicy`) for other, lower-traffic services. |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.tag | string | `"1.37.4"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | None, must be set if Cloud SQL Auth Proxy is enabled | Instance connection name for a Cloud SQL PostgreSQL instance |
| cloudsql.nodeSelector | object | `{}` | Node selection rules for the standalone Cloud SQL Proxy pod |
| cloudsql.podAnnotations | object | `{}` | Annotations for the standalone Cloud SQL Proxy pod |
| cloudsql.resources | object | See `values.yaml` | Resource limits and requests for the Cloud SQL Proxy container |
| cloudsql.serviceAccount | string | None, must be set if Cloud SQL Auth Proxy is enabled | The Google service account that has an IAM binding to the `gafaelfawr` Kubernetes service account and has the `cloudsql.client` role |
| cloudsql.tolerations | list | `[]` | Tolerations for the standalone Cloud SQL Proxy pod |
| config.afterLogoutUrl | string | Top-level page of this Phalanx environment | Where to send the user after they log out |
| config.baseInternalUrl | string | FQDN under `svc.cluster.local` | URL for direct connections to the Gafaelfawr service, bypassing the Ingress. Must use a service name of `gafaelfawr` and port 8080. |
| config.cilogon.clientId | string | `nil` | CILogon client ID. One and only one of this, `config.github.clientId`, or `config.oidc.clientId` must be set. |
| config.cilogon.enrollmentUrl | string | Login fails with an error | Where to send the user if their username cannot be found in LDAP |
| config.cilogon.loginParams | object | `{"skin":"LSST"}` | Additional parameters to add |
| config.cilogon.test | bool | `false` | Whether to use the test instance of CILogon |
| config.cilogon.usernameClaim | string | `"username"` | Claim from which to get the username |
| config.databaseUrl | string | None, must be set if neither `cloudsql.enabled` nor | URL for the PostgreSQL database `config.internalDatabase` are true |
| config.enableSentry | bool | `false` | Whether to send trace and telemetry information to Sentry. This traces every call and therefore should only be enabled in non-production environments. |
| config.errorFooter | string | `nil` | HTML footer to add to any login error page (will be enclosed in a <p> tag). |
| config.firestore.project | string | Firestore support is disabled | If set, assign UIDs and GIDs using Google Firestore in the given project. Cloud SQL must be enabled and the Cloud SQL service account must have read/write access to that Firestore instance. |
| config.github.clientId | string | `nil` | GitHub client ID. One and only one of this, `config.cilogon.clientId`, or `config.oidc.clientId` must be set. |
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
| config.ldap.groupSearchByDn | bool | `true` | Whether to search for group membership by user DN. Most LDAP servers list group members by full DNs, but if yours uses bare usernames, set this to false. |
| config.ldap.kerberosConfig | string | Use anonymous binds | Enable GSSAPI (Kerberos) binds to LDAP using this `krb5.conf` file. If set, `ldap-keytab` must be set in the Gafaelfawr Vault secret. Set either this or `userDn`, not both. |
| config.ldap.nameAttr | string | `"displayName"` | Attribute containing the user's full name |
| config.ldap.uidAttr | string | Get UID from upstream authentication provider | Attribute containing the user's UID number (set to `uidNumber` for most LDAP servers) |
| config.ldap.url | string | Do not use LDAP | LDAP server URL from which to retrieve user group information |
| config.ldap.userBaseDn | string | None, must be set | Base DN for the LDAP search to find a user's entry |
| config.ldap.userDn | string | Use anonymous binds | Bind DN for simple bind authentication. If set, `ldap-secret` must be set in the Gafaelfawr Vault secret. Set this or `kerberosConfig`, not both. |
| config.ldap.userSearchAttr | string | `"uid"` | Search attribute containing the user's username |
| config.logLevel | string | `"INFO"` | Choose from the text form of Python logging levels |
| config.metrics.application | string | `"gafaelfawr"` | Name under which to log metrics. Generally there is no reason to change this. |
| config.metrics.enabled | bool | `false` | Whether to enable sending metrics |
| config.metrics.events.topicPrefix | string | `"lsst.square.metrics.events"` | Topic prefix for events. It may sometimes be useful to change this in development environments. |
| config.metrics.schemaManager.registryUrl | string | Sasquatch in the local cluster | URL of the Confluent-compatible schema registry server |
| config.metrics.schemaManager.suffix | string | `""` | Suffix to add to all registered subjects. This is sometimes useful for experimentation during development. |
| config.oidc.audience | string | Same as `clientId` | Audience (`aud` claim) to expect in ID tokens. |
| config.oidc.clientId | string | `nil` | Client ID for generic OpenID Connect support. One and only one of this, `config.cilogon.clientId`, or `config.github.clientId` must be set. |
| config.oidc.enrollmentUrl | string | Login fails with an error | Where to send the user if their username cannot be found in LDAP |
| config.oidc.issuer | string | None, must be set | Issuer for the JWT token |
| config.oidc.loginParams | object | `{}` | Additional parameters to add to the login request |
| config.oidc.loginUrl | string | None, must be set | URL to which to redirect the user for authorization |
| config.oidc.scopes | list | `["openid"]` | Scopes to request from the OpenID Connect provider. The `openid` scope will always be included. |
| config.oidc.tokenUrl | string | None, must be set | URL from which to retrieve the token for the user |
| config.oidc.usernameClaim | string | `"uid"` | Claim from which to get the username |
| config.oidcServer.dataRightsMapping | object | `{}` | Mapping of group names to data release keywords, indicating membership in that group grants access to that data release. Used to construct the `data_rights` claim, which can be requested by asking for the `rubin` scope. |
| config.oidcServer.enabled | bool | `false` | Whether to support OpenID Connect clients |
| config.oidcServer.issuer | string | Base URL of this Phalanx environment | Issuer (`iss` claim) of generated ID tokens |
| config.oidcServer.keyId | string | `"gafaelfawr"` | Key ID (`kid` claim) of generated ID tokens, and the key ID served with the OAuth key metadata |
| config.proxies | list | [`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`] | List of netblocks used for internal Kubernetes IP addresses, used to determine the true client IP for logging |
| config.quota | object | `{}` | Quota settings (see [Quotas](https://gafaelfawr.lsst.io/user-guide/helm.html#quotas)). |
| config.realm | string | Hostname of this Phalanx environment | Authentication realm for HTTP `WWW-Authenticate` headers. |
| config.slackAlerts | bool | `false` | Whether to send certain serious alerts to Slack. If `true`, the `slack-webhook` secret must also be set. |
| config.tokenLifetime | string | `"30d"` | Session lifetime. Use `w`, `d`, `h`, `m`, and `s` for time intervals. For example, `1d6h23m` is one day, six hours, 23 minutes. |
| config.updateSchema | bool | `false` | Whether to automatically update the Gafaelfawr database schema |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the Gafaelfawr image |
| image.repository | string | `"ghcr.io/lsst-sqre/gafaelfawr"` | Gafaelfawr image to use |
| image.tag | string | The appVersion of the chart | Tag of Gafaelfawr image to use |
| ingress.additionalHosts | list | `[]` | Defines additional FQDNs for Gafaelfawr.  This doesn't work for cookie or browser authentication, but for token-based services like git-lfs or the webdav server it does. |
| maintenance.affinity | object | `{}` | Affinity rules for Gafaelfawr maintenance and audit pods |
| maintenance.auditSchedule | string | `"30 3 * * *"` | Cron schedule string for Gafaelfawr data consistency audit (in UTC) |
| maintenance.cleanupSeconds | int | 86400 (1 day) | How long to keep old jobs around before deleting them |
| maintenance.deadlineSeconds | int | 300 (5 minutes) | How long the job is allowed to run before it will be terminated |
| maintenance.maintenanceSchedule | string | `"5 * * * *"` | Cron schedule string for Gafaelfawr periodic maintenance (in UTC) |
| maintenance.nodeSelector | object | `{}` | Node selection rules for Gafaelfawr maintenance and audit pods |
| maintenance.podAnnotations | object | `{}` | Annotations for Gafaelfawr maintenance and audit pods |
| maintenance.resources | object | See `values.yaml` | Resource limits and requests for Gafaelfawr maintenance and audit pods |
| maintenance.tolerations | list | `[]` | Tolerations for Gafaelfawr maintenance and audit pods |
| nodeSelector | object | `{}` | Node selector rules for the Gafaelfawr frontend pod |
| operator.affinity | object | `{}` | Affinity rules for the token management pod |
| operator.nodeSelector | object | `{}` | Node selection rules for the token management pod |
| operator.podAnnotations | object | `{}` | Annotations for the token management pod |
| operator.resources | object | See `values.yaml` | Resource limits and requests for the Gafaelfawr Kubernetes operator. The limits are artificially higher since the operator pod is also where we manually run `gafaelfawr audit --fix`, which requires more CPU and memory. |
| operator.tolerations | list | `[]` | Tolerations for the token management pod |
| podAnnotations | object | `{}` | Annotations for the Gafaelfawr frontend pod |
| redis-ephemeral.affinity | object | `{}` | Affinity rules for the ephemeral Redis pod |
| redis-ephemeral.config.secretKey | string | `"redis-password"` | Key inside secret from which to get the Redis password (do not change) |
| redis-ephemeral.config.secretName | string | `"gafaelfawr"` | Name of secret containing Redis password (do not change) |
| redis-ephemeral.nodeSelector | object | `{}` | Node selection rules for the ephemeral Redis pod |
| redis-ephemeral.persistence.enabled | bool | `false` | Whether to persist Redis storage of ephemeral data. This should always be false. |
| redis-ephemeral.podAnnotations | object | `{}` | Pod annotations for the ephemeral Redis pod |
| redis-ephemeral.resources | object | See `values.yaml` | Resource limits and requests for the ephemeral Redis pod |
| redis-ephemeral.tolerations | list | `[]` | Tolerations for the ephemeral Redis pod |
| redis.affinity | object | `{}` | Affinity rules for the persistent Redis pod |
| redis.config.secretKey | string | `"redis-password"` | Key inside secret from which to get the Redis password (do not change) |
| redis.config.secretName | string | `"gafaelfawr"` | Name of secret containing Redis password (do not change) |
| redis.nodeSelector | object | `{}` | Node selection rules for the persistent Redis pod |
| redis.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode of storage to request |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage and thus tokens. Setting this to false will use `emptyDir` and reset all tokens on every restart. Only use this for a test deployment. |
| redis.persistence.size | string | `"1Gi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `""` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `""` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.podAnnotations | object | `{}` | Pod annotations for the persistent Redis pod |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the persistent Redis pod |
| redis.tolerations | list | `[]` | Tolerations for the persistent Redis pod |
| replicaCount | int | `1` | Number of web frontend pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the Gafaelfawr frontend pod |
| tolerations | list | `[]` | Tolerations for the Gafaelfawr frontend pod |
