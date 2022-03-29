Update the ``TAP_SCHEMA`` table
===============================

The ``TAP_SCHEMA`` table stores information about the tables available in a given installation of the Rubin Science Platform.
This table is kept in sync with the felis files using the following process:

#. Make a PR to the `sdm_schemas repository <https://github.com/lsst/sdm_schemas>`__ with a change to a felis YAML file.
#. After this is merged, make a GitHub release of sdm_schemas with a new semver version number.
   (Ignore the weekly tags that are added by other processes.)
   This will create a tag and run a publishing pipeline GitHub Action.
   That publishing pipeline will run the Python felis library against the YAML files in the ``yml`` directory and make different Docker images for the different supported environments.
   It will then push the images to DockerHub.
#. Update the ``appVersion`` version to the version of the new release in the `tap-schema Phalanx service <https://github.com/lsst-sqre/phalanx/blob/master/services/tap-schema/Chart.yaml>`__.
