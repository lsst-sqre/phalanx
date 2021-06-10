###############
Syncing Argo CD
###############

To access the Argo CD UI, go to the ``/argo-cd`` URL under the domain name of that deployment of the Rubin Science Platform.
Depending on the environment, you will need to authenticate with either GitHub or with Google OAuth (or you can use the ``admin`` account and password, stored in 1Password for deployments managed by SQuaRE, in case of an emergency).

When deploying an update, it should normally follow this sequence (skipping environments that aren't relevant to that update).

* data-dev.lsst.cloud
* data-int.lsst.cloud
* lsst-lsp-int.ncsa.illinois.edu
* tucson-teststand.lsst.codes
* lsst-nts-k8s.ncsa.illinois.edu
* data.lsst.cloud
* lsst-lsp-stable.ncsa.illinois.edu
* base-lsp.lsst.codes
* summit-lsp.lsst.codes

Some of these environments have maintenance windows, in which case, in the absence of an emergency, updates should only be synced during the maintenance window.
See `SQR-056`_ for more information.

.. _SQR-056: https://sqr-056.lsst.io/

Out-of-date applications will show as yellow in Argo CD.
(If the update was made recently, you may have to click :guilabel:`Refresh` first.
If the update was to a chart whose version is not pinned, you may have to use the small arrow next to :guilabel:`Refresh` and select :guilabel:`Hard Refresh`.)
To review the changes before applying them, select :guilabel:`App Diff`.

Once your Argo CD says you are green, then you are where you say you want to be.
If something happens to the cluster and its resources, Argo CD will let you know, even the action wasn't taken by Argo CD.
This makes it useful for reverting back to a LKG (Last-Known-Good) state.
