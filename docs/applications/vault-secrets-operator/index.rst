.. px-app:: vault-secrets-operator

############################################
vault-secrets-operator — Vault to Kubernetes
############################################

The ``vault-secrets-operator`` application is an installation of `Vault Secrets Operator`_ to retrieve necessary secrets from Vault and materialize them as Kubernetes secrets for the use of other applications.
It processes ``VaultSecret`` resources defined in the `Phalanx repository`_ and creates corresponding Kubernetes Secret_ resources.

.. jinja:: vault-secrets-operator
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   bootstrap
   upgrade
   values
