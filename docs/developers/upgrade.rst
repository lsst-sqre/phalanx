########################
Upgrading an application
########################

First, for first-party applications, release a new version of the application by pushing an image with the new version tag to whichever Docker repository is used.
For most applications, this should be done via GitHub Actions when a tag is created by adding a new release.

Then, update Phalanx to install the new version of the application.

- If it is a first-party application such as ``mobu``, with its chart directly in Phalanx, update the ``appVersion`` in :file:`Chart.yaml`.

- If it is a third-party application such as ``cert-manager`` and you are updating to a newer version of the third-party Helm chart, update the ``version`` in the relevant dependency in :file:`Chart.yaml`.
  Normally `Mend Renovate`_ will create PRs to do this automatically.

- If it is a complex application such as ``sasquatch`` that bundles first- and third-party applications, you may need to do both, including making updates to ``appVersion`` or dependency versions in the :file:`charts` subdirectory.
  Tricky cases such as these may require some study before deciding on the best course of action.

Once you have updated the application, Argo CD will notice that the change is pending, but no changes will be applied automatically.
To apply the changes in a given environment, see :doc:`/admin/sync-argo-cd`.
