##############################
Bootstrapping a new deployment
##############################

This is (very incomplete) documentation on how to add a new Rubin Science Platform environment.

Checklist
#########

#. Fork the `phalanx repository <https://github.com/lsst-sqre/phalanx>`__ if this work is separate from the SQuaRE-managed environments.
#. Create a new ``values-<environment>.yaml`` file in `/science-platform <https://github.com/lsst-sqre/phalanx/tree/master/science-platform/>`__.
   Start with a template copied from an existing environment that's similar to the new environment.
   Edit it to change the environment name at the top to match ``<environment>`` and choose which services to enable or disable.
#. For each enabled service, create a corresponding ``values-<environment>.yaml`` file in the relevant directory under `/services <https://github.com/lsst-sqre/phalanx/tree/master/services/>`__.
   Customization will vary from service to service, but the most common change required is to set the fully-qualified domain name of the environment to the one that will be used for your new deployment.
   This will be needed in ingress hostnames, NGINX authentication annotations, and the paths to Vault secrets (the part after ``k8s_operator`` should be the same fully-qualified domain name).
#. Generate the secrets for the new environment with `/installer/generate_secrets.py <https://github.com/lsst-sqre/phalanx/tree/master/installer/generate_secrets.py>`__ and store them in Vault with `/installer/push_secrets.sh <https://github.com/lsst-sqre/phalanx/tree/master/installer/push_secrets.sh>`__.
#. Run the installer script at `/installer/install.sh <https://github.co/lsst-sqre/phalanx/tree/master/installer/install.sh>`__.

Application notes
#################

Gafaelfawr
----------

When creating the Gafaelfawr configuration for a new environment, in addition to choosing between OpenID Connect authentication and GitHub authentication, you will need to define a group mapping.
This specifies which scopes a user will receive based on which groups they are a member of in the upstream identity system.
The current default expects the NCSA groups, which will not be accurate unless you're using CILogon with NCSA LDAP as an attribute source.

The most important scopes to configure are:

* ``exec:admin``: provides access to administrative tools (users do not need this)
* ``exec:user``: allows users to create personal tokens
* ``exec:notebook``: allows users to use the Notebook Aspect
* ``exec:portal``: allows users to use the Portal Aspect
* ``read:tap``: allows users to make TAP queries

If you are using OpenID Connect, the group values for each scope should be group names as shown in the ``isMemberOf`` claim.

If you are using GitHub, group membership will be synthesized from all of the teams of which the user is a member.
These must be team memberships, not just organization memberships.
The corresponding group for Gafaelfawr purposes will be ``<organization>-<team>`` where ``<team>`` is the team **slug**, not the team name.
That means the team name will be converted to lowercase and spaces will be replaced with dashes, and other transformations will be done for special characters.
For more information about how Gafaelfawr constructs groups from GitHub teams, see `the Gafaelfawr documentation <https://gafaelfawr.lsst.io/arch/providers.html#github-groups>`__.

For an example of a ``group_mapping`` configuration for GitHub authentication, see `/services/gafaelfawr/values-idfdev.yaml <https://github.com/lsst-sqre/phalanx/tree/master/services/gafaelfawr/values-idfdev.yaml>`__.

If you run into authentication problems, see :doc:`the Gafaelfawr operational documentation <gafaelfawr/index>` for debugging instructions.
