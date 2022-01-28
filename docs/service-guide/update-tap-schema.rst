Update the ``TAP_SCHEMA`` table
===============================

The ``TAP_SCHEMA`` table stores information about the tables available in a given installation of the Rubin Science Platform.
This table is kept in sync with the felis files using the following process:

#. Make a PR to the `sdm_schemas repository <https://github.com/lsst/sdm_schemas>`__ with a change to a felis YAML file.
#. After this is merged, make a GitHub release with a new version number.
   This will create a tag and run a publishing pipeline GitHub Action.
   That publishing pipeline will run the Python felis library against the YAML files in the ``yml`` directory and make different Docker images for the different supported environments.
   It will then push the images to DockerHub.
#. Update the version of the `tap-schema chart <https://github.com/lsst-sqre/charts/tree/master/charts/tap-schema>`__ following the instructions in :doc:`upgrade`.
   The ``appVersion`` in ``Chart.yaml`` should be updated to match the version of the new release, and the ``version`` of the chart increased following normal semver conventions.
#. Sync the ``tap-schema`` application in Argo CD in the relevant environment or environments (see :doc:`sync-argo-cd`).
