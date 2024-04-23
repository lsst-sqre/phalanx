################################
Audit secrets for an environment
################################

To check that all of the necessary secrets for an environment named ``<environment>`` are in Vault and appear to have the proper form, run:

.. prompt:: bash

   phalanx secrets audit <environment>

Add the ``--secrets`` command-line option or set ``OP_CONNECT_TOKEN`` if needed for your choice of a :ref:`static secrets source <admin-static-secrets>`.
For SQuaRE-managed deployments, the 1Password token for ``OP_CONNECT_TOKEN`` comes from the ``Phalanx 1Password tokens`` item in the SQuaRE 1Password vault.

If you did not store the Vault write token for your environment with the static secrets, the ``VAULT_TOKEN`` environment variable must be set to the Vault write token for this environment (or a read token; this command will not make any changes).
For SQuaRE-managed environments, you can get the write token from the ``Phalanx Vault write tokens`` item in the SQuaRE 1Password vault.

The output of the command will be a report of any inconsistencies or problems found in the Vault secrets for this environment.
No output indicates no problems.
