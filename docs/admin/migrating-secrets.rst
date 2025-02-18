##############################################
Migrating to the new secrets management system
##############################################

We introduced a new command-line-driven secrets management system for Phalanx environments in September of 2023.
This page documents how to migrate to the new system.

These instructions assume that, if you are using 1Password for static secrets, you have already set up a 1Password vault and enabled the :px-app:`1Password Connect server <onepassword-connect>` for this environment.
If you have not yet done this, see :doc:`/applications/onepassword-connect/add-new-environment`.

In all :command:`phalanx` commands listed below, replace ``<environment>`` with the short identifier of your environment.

Change Vault configuration
==========================

Previously, :px-app:`vault-secrets-operator` was configured to use a read token stored in a ``vault-secrets-operator`` ``Secret`` resource.
The new secret management system uses Vault AppRoles instead, which are the recommeded authentication approach for services.

#. Delete the override in the ``vault-secrets-operator`` configuration to use an AppRole by deleting the configuration block in :file:`applications/vault-secrets-operator/values-{environment}.yaml` for your environment.
   If your environment was already using AppRoles, you can skip this step.

   Don't sync the ``vault-secrets-operator`` application yet.
   You will be told below when it's time to do that.

#. If your environment uses the SQuaRE Vault server, change the ``vaultPathPrefix`` setting for your environment in :file:`environments/values-{environment}.yaml` to :samp:`secret/phalanx/{environment}`.
   For example:

   .. code-block:: yaml

      vaultPathPrefix: "secret/phalanx/idfdev"

   Note that the last component of the path now uses the short environment name, not the FQDN of the environment.

   If you are using some other Vault server with its own path conventions, you can skip this step, although it is easier to do the migration if you can set up the new secrets in a new Vault path without having to change the old Vault path.

#. Set the ``VAULT_TOKEN`` environment variable to a token with access to create new AppRoles and tokens and to list token accessors and secret IDs.
   If you are using the SQuaRE Vault server, use the admin token from the ``Phalanx Vault admin credentials`` 1Password item in the SQuaRE 1Password vault.
   This environment variable will be used for multiple following commands.
   You will be told when you can clear it again.

#. Create the Vault AppRole credentials and save them as a secret in the ``vault-secrets-operator`` namespace.

   When running this command, ensure that your default Kubernetes configuration is pointing to the Kubernetes cluster for your environment, since it uses :command:`kubectl` to create resources in the default Kubernetes cluster.

   .. prompt:: bash

      phalanx vault create-read-approle --as-secret vault-credentials <environment> | kubectl apply -f -

   You can instead run the command without the pipeline (``|``) to inspect the ``Secret`` resource first and then pass it to :command:`kubectl apply` yourself.
   Just be aware that every time you run :command:`phalanx vault create-read-approle`, it creates a new AppRole SecretID and invalidates the old one.

   The AppRole RoleID and SecretID aren't saved anywhere other than in the Kubernetes cluster.
   If they are lost, just make a new one.

   If you are using a non-SQuaRE Vault server and don't have admin access, or don't want to use the Phalanx command-line tools to manage your Vault credentials, you should instead manually create a ``Secret`` in the ``vault-secrets-operator`` namespace named ``vault-credentials``.
   For AppRole authentication, it must have at least two keys, ``VAULT_ROLE_ID`` and ``VAULT_SECRET_ID``, which contain the RoleID and SecretID of an AppRole with only read access to the Vault path prefix set in the previous step.
   You may need other settings depending on your environment.
   If you wish, you can use some other authentication method entirely.
   See the `Vault Secrets Operator`_ documentation for full documentation of possible options.

#. Create a Vault write token for the new Vault path.
   You will use this token (via the ``VAULT_TOKEN`` environment variable) to authenticate to Vault in later steps (but don't switch to it yet).

   .. prompt:: bash

      phalanx vault create-write-token <environment>

   The new token will be printed to standard output along with some metadata about it.

   For SQuaRE-managed environments, save that token in the ``SQuaRE`` 1Password vault (**not** the vault for the RSP environment) in the item named ``Phalanx Vault write tokens``.
   Add a key for the short environment identifier and set the value to the newly-created write token.
   Don't forget to mark it as a password using the icon on the right.
   Then, add a key under the :guilabel:`Accessors` heading for the environment and set the value to the token accessor.
   Similarly, mark it as a password.

   If you are not in SQuaRE, save this write token wherever you normally save passwords and authentication tokens.
   You will need it for all future Phalanx secrets operations for this environment.

#. (Optional) Check that everything looks good with the new Vault configuration and credentials.

   .. prompt:: bash

      phalanx vault audit <environment>

   This command will print diagnostics if it finds any problems.
   You will still need ``VAULT_TOKEN`` set to a privileged token to run this command.

Update secrets
==============

#. Copy the secrets for this environment from the old path to the new path.
   This step avoids regenerating secrets, which would invalidate user tokens and be more disruptive than necessary.
   It seeds the new Vault path with a copy of the secrets from the old Vault path.

   .. prompt:: bash

      phalanx vault copy-secrets <environment> <old-path>

   Replace ``<old-path>`` with the old path that you just changed in ``vaultPathPrefix`` in the previous step.
   That old path will be something like :samp:`secret/k8s_operator/{fqdn}` for environments that use the SQuaRE Vault server.

#. Set the ``VAULT_TOKEN`` environment variable to the write token for the environment that you created in an earlier step.
   You no longer need to use a highly-privileged token (and indeed should not, to minimize the chances of breaking some other environment).

#. Set the ``VAULT_ADDR`` environment variable to the URL for your Vault server.
   This will be found in the ``vaultUrl`` setting in :file:`environments/values-{environment}.yaml` for your environment.
   This will allow you to use the regular :command:`vault` command-line tool to explore and modify the contents of Vault, which will be useful shortly.

#. Construct the static secrets for your environment.
   Start by generating a template for all static secrets required by the configuration of your environment:

   .. prompt:: bash

      phalanx secrets static-template <environment> > static-secrets.yaml

   You may want to put the output file somewhere outside of your checkout of Phalanx.

   This will create a YAML file listing all applications and their required static secrets, based on their configuration for your environment.

   Then, what you do depends on whether you are using 1Password as a source of static secrets or not.
   See :doc:`add-new-secret` for detailed instructions on how to add static secrets for an application.
   You will need to do this for every application.

   To obtain the current values of static secrets, use the :command:`vault kv get` command to read the current value of the static secret out of Vault (copied to the new path in the previous step).

   For example, to see all the current secrets for the application ``nublado``, run:

   .. prompt:: bash

      vault kv get <vault-path>/nublado

   Replace ``<vault-path>`` with the value of ``vaultPathPrefix`` in :file:`environments/values-{environment}.yaml` for your environment.

#. If you are using 1Password as the source for static secrets, set ``OP_CONNECT_TOKEN`` to the 1Password Connect token for this environment.
   For SQuaRE-managed environments, this can be found in the ``RSP 1Password tokens`` item in the SQuaRE 1Password vault.

   Also, add the :ref:`pull secret <admin-onepassword-pull-secret>` and :ref:`Vault write token <admin-onepassword-vault-token>` to the 1Password vault for this environment if appropriate.

#. Check what secrets are missing or incorrect and fix them.

   .. prompt:: bash

      phalanx secrets audit <environment>

   If you are using a static secrets file, add the ``--secrets`` flag pointing to that file.

   The most likely outcome the first time you run this command is a list of unresolved secrets.
   These are static secrets that are missing from your static secrets source, or secrets that could not be copied from their canonical secret (usually due to some application configuration issue).
   Resolve those problems and run the command again.

   Eventually, you will get a report that contains missing, incorrect, and unknown secrets.
   These are problems that the Phalanx command-line tool believes that it can fix.
   However, in many cases you do not want to let it fix these issues, since that could mean regenerating secrets instead of finding them in an old location or deleting secrets as obsolete when instead what was missing was the configuration telling Phalanx that secret was required.

   Work through each of these one-by-one, resolving them.
   Get the values of unknown secrets with :command:`vault kv get`.
   Use :command:`vault kv patch` to add missing keys to existing secrets, and :command:`vault kv store` to create entirely new secrets (but be warned that the second command will overwrite any existing secret entirely).
   The path for a secret for an application is :samp:`{vault-path-prefix}/{application}` where the Vault path prefix is ``vaultPathPrefix`` in :file:`environments/values-{environment}.yaml` for your environment.

   You can re-run :command:`phalanx secrets audit` as often as you want to check your progress.
   Eventually you will be down to only unknown secrets, and will have confirmed that all of those secrets are no longer needed (such as artifacts from the old secret management system that hold configuration information, or secrets that have been renamed or merged into a relevant application secret).

Switch to the new secrets tree
==============================

#. Once you have resolved all inconsistencies that you think will affect applications, perform an actual secrets sync.

   .. prompt:: bash

      phalanx secrets sync <environment>

   If you are using a static secrets file, add the ``--secrets`` flag pointing to that file.
   This will fix any secrets that are missing or incorrect in Vault.

#. Some Phalanx applications need to know whether the old or new secrets layout is in use.
   On your working branch, add the necessary settings for those applications to their :file:`values-{environment}.yaml` files for your environment.
   Applications to review:

   - :px-app:`nublado` (``secrets.templateSecrets``)
   - :px-app:`obsloctap` (``config.separateSecrets``)
   - :px-app:`plot-navigator` (``config.separateSecrets``)
   - :px-app:`rubintv` (``rubintv.separateSecrets``)

#. You're now ready to test the new secrets tree.
   You can do this on a branch that contains the changes you made above.

   Using Argo CD, switch both the ``vault-secrets-operator`` application and the ``science-platform`` app of apps to point to your branch.
   You will then need to sync nearly every application to switch to the new Vault secrets path.

   Check that Vault Secrets Opeartor is able to find the new secrets by looking at its log, and also find a ``VaultSecret``, delete the corresponding ``Secret`` created based on it, and ensure that Vault Secrets Operator recreates the ``Secret``.
   This checks that Vault authentication is working correctly.

#. Merge your Phalanx changes to change the Vault path prefix and any other changes you made during the secrets migration.

#. When you're confident that the new secrets are working correctly and nothing is missing, sync secrets again, deleting any now-unwanted secrets from Vault.

   .. prompt:: bash

      phalanx secrets sync --delete <environment>

   If you are using a static secrets file, add the ``--secrets`` flag pointing to that file.
