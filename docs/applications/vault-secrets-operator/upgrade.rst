.. px-app-upgrade:: vault-secrets-operator

################################
Upgrading vault-secrets-operator
################################

Upgrading to newer upstream releases of the Helm chart is normally simple and straightforward.
We have no significant local customization.

If you want to verify that an upgrade has been successful, or if at any point you want to verify that Vault Secrets Operator is still working, find a ``VaultSecret`` and ``Secret`` resource pair in the Argo CD dashboard and delete the ``Secret`` resource.
It should be nearly immediately re-created from the ``VaultSecret`` resource by Vault Secrets Operator.

The Gafaelfawr secret is a good one to use for this purpose since it is only read during Gafaelfawr start-up, so deleting the ``Secret`` resource won't cause an outage.
