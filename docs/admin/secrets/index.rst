##################
Secrets management
##################

Phalanx provides a command-line tool, :command:`phalanx secrets`, to manage the secrets for a Phalanx environment.
Use of this tool is optional; the Phalanx Helm charts only require that the appropriate keys be present in the Vault secret corresponding to an application.
However, its use is strongly recommended since it provides consistency checking and supports use of a separate secret store to hold persistent secrets.

For an overview of how Phalanx uses secrets, see :ref:`secrets`.

.. toctree::
   :caption: Procedures
   :maxdepth: 1

   add-new-secret
   update-a-secret
   sync-secrets
   audit-secrets
   update-pull-secret
   migrating-secrets

.. toctree::
   :caption: Tools
   :maxdepth: 1

   op-run-phalanx-cli
