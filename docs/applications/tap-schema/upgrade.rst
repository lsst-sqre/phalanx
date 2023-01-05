.. px-app-upgrade:: tap-schema

####################
Upgrading tap-schema
####################

Upgrading the tap-schema Argo CD application itself requires no special steps.
Syncing the Argo CD application is all that's required.
The new schema will automatically be picked up by the TAP service.

Releasing a new schema version
==============================

When a new version of the project schema is ready for deployment, use the following procedure:

#. Ensure all PRs to `lsst/sdm_schemas <https://github.com/lsst/sdm_schemas>`__ that should go into the new release have been merged.

#. Make a new GitHub release of sdm_schemas with a new `semantic versioning`_ version number (such as ``1.1.5``).
   (Ignore the other tags in the repository, such as ``w.2022.45``,  created by other Rubin release processes.)
   This will create a tag and run the publishing pipeline GitHub Action.
   That, in turn, will run Felis_ against the YAML schema files in the ``yml`` directory and build the Docker images for the different supported environments.

#. Update the ``appVersion`` field to the version of the new release in `/applications/tap-schema/Chart.yaml <https://github.com/lsst-sqre/phalanx/blob/master/applications/tap-schema/Chart.yaml>`__.

#. Sync the tap-schema Argo CD application on affected environments as normal.
