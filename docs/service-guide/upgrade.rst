####################
Upgrading an service
####################

#. Release a new version of the service by pushing an image with the new version tag to Docker Hub (or whatever Docker repository is used).

#. Update the chart in the `charts repository <https://github.com/lsst-sqre/charts>`__ to install the current version.
   For charts using the recommended pattern of determining the default Docker tag via the ``appVersion`` chart metadata, this only requires updating ``appVersion`` in ``Chart.yaml``.
   Some charts cannot (or do not) do this, in which case the version has to be changed elsewhere, normally in ``values.yaml``.
   Also update the ``version`` of the chart in ``Chart.yaml`` (which follows `semantic versioning`_).
   When this PR is merged, a new chart will automatically be published.

#. Update the chart version in the Phalanx ``Chart.yaml`` file for the appropriate service under `/services <https://github.com/lsst-sqre/phalanx/tree/master/services>`__.
   If the chart is not pinned (if, in other words, it uses a version range constraint instead of a specific version), no Phalanx change is required.

This will tell Argo CD that the change is pending, but no changes are applied automatically.
To apply the changes in a given environment, see :doc:`sync-argo-cd`.
