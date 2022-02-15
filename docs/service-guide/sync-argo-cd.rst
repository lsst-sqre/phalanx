###############
Syncing Argo CD
###############

Go to Argo CD for the environment
=================================

To access the Argo CD UI, go to the ``/argo-cd`` URL under the domain name of that deployment of the Rubin Science Platform.
See `the Phalanx README <https://github.com/lsst-sqre/phalanx/blob/master/README.rst>`__ for the names of all Phalanx environments and direct links to their Argo CD pages.

Depending on the environment, you will need to authenticate with either GitHub or with Google OAuth.
You can use the ``admin`` account and password, stored in 1Password for deployments managed by SQuaRE, in case of an emergency.

When deploying an update, it should normally follow this sequence (skipping environments that aren't relevant to that update).

* data-dev.lsst.cloud
* data-int.lsst.cloud
* lsst-lsp-int.ncsa.illinois.edu
* tucson-teststand.lsst.codes
* data.lsst.cloud
* lsst-lsp-stable.ncsa.illinois.edu
* base-lsp.lsst.codes
* summit-lsp.lsst.codes

Some of these environments have maintenance windows, in which case, in the absence of an emergency, updates should only be synced during the maintenance window.
See `SQR-056`_ for more information.

.. _SQR-056: https://sqr-056.lsst.io/

Sync the application
====================

Out-of-date applications will show as yellow in Argo CD.
Click on the application to see its current resources and more details about its status.

If the update was made recently, you may have to click :guilabel:`Refresh` first.
If the update was to a chart whose version is not pinned, click on the small arrow next to :guilabel:`Refresh` and select :guilabel:`Hard Refresh`.
(You will need to click directly on the small arrow, to the pixel, to see this option.)

To review the changes before applying them, select :guilabel:`App Diff`.

To apply the changes, select :guilabel:`Sync`.

Once your Argo CD says you are green, then you are where you say you want to be.
If something happens to the cluster and its resources, Argo CD will let you know, even the action wasn't taken by Argo CD.

Revert to a previous configuration
==================================

To revert to a previous version of the application configuration, select :guilabel:`History and Rollback`, find the previous configuration to which you want to revert, and then click on the vertical three dots on the right side of the box for that version.
Select :guilabel:`Rollback` from the resulting menu.
