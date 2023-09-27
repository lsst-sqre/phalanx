################################
Audit secrets for an environment
################################

To check that all of the necessary secrets for an environment named ``<environment>`` are in Vault and appear to have the proper form, run:

.. prompt:: bash

   phalanx secrets audit <environment>

The ``VAULT_TOKEN`` environment variable must be set to the Vault write token for this environment (or a read token; this command will not make any changes).

The output of the command will be a report of any inconsistencies or problems found in the Vault secrets for this environment.
No output indicates no problems.
