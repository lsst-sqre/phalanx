.. px-app-bootstrap:: onepassword-connect

###############################
Bootstrapping 1Password Connect
###############################

When :ref:`installing a new environment <bootstrapping-toc>`, one of the steps is to :doc:`synchronize secrets for that environment </admin/secrets-setup>`.
However, when 1Password is used as the source for static secrets, this requires a running 1Password Connect server and a token to connect to that server.
Bootstrapping an environment with this property therefore a different process to break this cycle.

The recommended process of bootstrapping this type of environment is:

#. In :file:`environment/values-{environment}.yaml`, enable only the minimum required applications plus ``onepassword-connect``.
   Leave everything else disabled to start.

#. Follow the normal secrets setup for the environment using :ref:`a YAML file for static secrets <admin-secrets-yaml>`.
   Fill in the ``onepassword-connect`` secret with the base64-encoded credentials file obtained from :doc:`add-new-connect-server`.

#. Install the environment using the :doc:`normal instructions </admin/installation>`.

#. Now that you have a running 1Password Connect server, take the secrets from your static secrets YAML file and :ref:`populate your 1Password vault with those secrets <admin-secrets-onepassword>`.

#. Set the ``OP_CONNECT_TOKEN`` environment variable to the token for this environment and :doc:`sync secrets again </admin/sync-secrets>` using 1Password.

#. Now, enable the rest of the applications you want to run in this environment and finish :doc:`secrets setup </admin/secrets-setup>` and :doc:`installation </admin/installation>`.
