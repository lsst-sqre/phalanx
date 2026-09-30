###########################################
Updating the pull secret for an environment
###########################################

To update the pull secret for an environment, follow these steps:

#. Update the pull secret in your static secrets source.
   If you are using a :ref:`YAML file for secrets <admin-secrets-yaml>`, edit the ``pull-secret`` section to add new registries or make any necessary changes.
   If you are using :ref:`1Password <admin-onepassword-pull-secret>`, follow the same instructions as creating the pull secret originally, but change the 1Password item as needed instead of making a new one.

   If you are storing your static secrets directly in Vault, you are on your own.
   You will need to modify the ``.dockerconfigjson`` key of the ``pull-secret`` secret for the environment, maintaining the correct encoding.
   See `Pull an image from a private registry <https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/>`__ in the Kubernetes documentation for more details about the correct format.

#. If you are storing static secrets anywhere other than Vault, synchronize secets for your environment.

   .. tab-set::

      .. tab-item:: General

         .. prompt:: bash

            phalanx secrets sync <environment>

         Replace ``<environment>`` with the short identifier of your environment.

      .. tab-item:: SQuaRE-managed environments (1Password)

         .. prompt:: bash

            op run --env-file="op/<environment>.env" -- phalanx secrets sync <environment>

         Replace ``<environment>`` with the short identifier of your environment.
         See :doc:`op-run-phalanx-cli` for details on using the 1Password CLI to run the phalanx CLI with secrets from 1Password.

   This should update the ``pull-secret`` secret in Vault.

:px-app:`vault-secrets-operator` should then pick up the changes within a minute and update the ``pull-secret`` secret for any application that needs one.
If you want to make that process go faster, restart the vault-secrets-operator pod.
