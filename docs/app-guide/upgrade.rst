########################
Upgrading an application
########################

#. Release a new version of the application by pushing an image with the new version tag to Docker Hub (or whatever Docker repository is used).
#. Update the chart in the `charts repository <https://github.com/lsst-sqre/charts>`__ to install the current version.
   For charts using the recommended pattern of determining the default Docker tag via the ``appVersion`` chart metadata, this only requires updating ``appVersion`` in ``Chart.yaml``.
   Some charts cannot (or do not) do this, in which case the version has to be changed elsewhere, normally in ``values.yaml``.
   Also update the ``version`` of the chart in ``Chart.yaml`` (which follows `semantic versioning`_).
   When this PR is merged, a new chart will automatically be published.
#. If the chart version is pinned in Phalanx, update the chart version in ``Chart.yaml`` for the appropriate application under `/services <https://github.com/lsst-sqre/phalanx/tree/master/services>`__.
   IF the chart is not pinned, no Phalanx change is required.

.. _semantic versioning: https://semver.org/

This will tell Argo CD that the change is pending, but no changes are applied automatically.
You can now go to the ``/argo-cd`` endpoint in the Rubin Science Platform deployment and sync the application.
You may need to click :guilabel:`Refresh` to see the updated version.
If the version of the chart is not pinned, you will need to use the arrow next to :guilabel:`Refresh` and choose :guilabel:`Hard Refresh`.
(You will need to click directly on the small arrow to see this option.)
