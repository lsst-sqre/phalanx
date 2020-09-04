# infrastructure

This configurable Argo CD application installs the infrastructure services that other Rubin Science Platform services depend upon.
It has been separated from the `science-platform` application to aid with sequencing when deploying a new cluster.
The `infrastructure` application is synced first, then the `science-platform` application, so services under the `science-platform` application can depend on custom resource definitions and other infrastructure deployed by the `infrastructure` application.

Unfortunately, this does not capture all of the required sequencing.
The `vault-secrets-operator` application must be deployed first, before the rest of the `infrastructure` application.
Generally this is done by syncing that application alone, and then creating and syncing the `infrastructure` application, which will then take over parentage of `vault-secrets-operator`.
