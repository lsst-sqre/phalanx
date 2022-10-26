.. px-app-upgrade:: vault-secrets-operator

################################
Upgrading vault-secrets-operator
################################

Upgrading to newer upstream releases of the Helm chart is normally simple and straightforward.
We have no significant local customization.

After upgrading, check that Vault Secrets Operator is still working properly by finding a ``VaultSecret`` and ``Secret`` resource pair in the Argo CD dashboard and deleting the ``Secret`` resource.
It should be nearly immediately re-created from the ``VaultSecret`` resource by Vault Secrets Operator.
The Gafaelfawr secret is a good one to use for this purpose since it is only read during Gafaelfawr start-up.
