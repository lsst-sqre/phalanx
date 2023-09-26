.. px-app:: onepassword-connect

##########################################
onepassword-connect — 1Password API server
##########################################

1Password Connect provides API access to a 1Password vault.
It is used to provide the API for Phalanx integration with 1Password as a source of static secrets.

Each 1Password Connect server can serve multiple 1Password vaults.
For SQuaRE-managed environments, we run two 1Password Connect servers, one for development environments and one for production environments.
Each environment gets its own 1Password Connect token that can only see secrets in its own 1Password Connect vault.

.. jinja:: onepassword-connect
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   bootstrap
   add-new-environment
   add-new-connect-server
   values
