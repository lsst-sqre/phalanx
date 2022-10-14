########################
Upgrading an application
########################

#. Release a new version of the application by pushing an image with the new version tag to whichever Docker repository is used.
   For more recent applications, this image should be built and pushed as a GitHub action upon release of a new version.

#. There are multiple possibilities that depend on the sort of application you have.
    - If it is a first-party application such as ``cachemachine``, with its chart directly in Phalanx, then it should use the recommended pattern of determining the default Docker tag via the ``appVersion`` chart metadata.  This will only require updating ``appVersion`` in ``Chart.yaml``.
    - If, like ``cert-manager``, it's a third-party application with some extra resources glued in, and you are updating to a newer version of the third-party Helm chart, you will need to update the ``version`` in the dependency.
    - If it is a complex application such as ``sasquatch`` that bundles first- and third-party applications, you may need to do both, or indeed descend into the ``charts`` directory and update the ``appVersion`` of the subcharts therein.  Tricky cases such as these may require some study before deciding on the best course of action.

Once you have updated the application, Argo CD will that the change is pending, but no changes will be applied automatically.
To apply the changes in a given environment, see :doc:`/admin/sync-argo-cd`.
