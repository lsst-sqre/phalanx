##############################################
Updating the recommended Notebook Aspect image
##############################################

The ``recommended`` tag for JupyterLab images is usually a recent weekly image.
The image tagged ``recommended`` is guaranteed by SQuaRE to be compatible with other services and materials, such as tutorial or system testing notebooks, that we make available on RSP deployments.

Because this process requires quite a bit of checking and sign-off from multiple stakeholders, it is possible that approving a new recommended version may take more than the two weeks (for most deployments) it takes for a weekly image to roll off the default list of images to pull.
This can cause the RSP JupyterHub options form to display empty parentheses rather than the correct target version when a user requests a lab container.

This document explains the process for moving the ``recommended`` tag, and how to circumvent that display bug by changing nublado's ``values-<instance>.yaml`` for the appropriate instance when moving the ``recommended`` tag.

Tagging a new container version
--------------------------------

When a new version is to be approved (after passing through its prior QA and sign-off gates), the ``recommended`` tag must be updated to point to the new version.

To do this, run the GitHub retag workflow for the `sciplat-lab <https://github.com/lsst-sqre/sciplat-lab>`__ repository, as follows:

#. Go to `the retag workflow page <https://github.com/lsst-sqre/sciplat-lab/actions/workflows/retag.yaml>`__.
#. Click on :guilabel:`Run workflow`.
#. Enter the tag of the image to promote to recommended under :guilabel:`Docker tag of input container`.
   This will be a tag like ``w_2022_40``.
#. Enter ``recommended`` under :guilabel:`Additional value to tag container with`.
#. Click on the :guilabel:`Run workflow` submit button.

Don't change the URIs.

.. _prepull-recommended:

Changing the recommended image to some tag other than "recommended"
-------------------------------------------------------------------

Because tags are global per repository, it is quite often the case that Telescope and Site, in particular, want the recommended image for a given instance to be different per instance, because the instances may not be running the same XML cycle.

Inside the JupyterLab Controller configuration for a given instance, you should find the key ``controller.config.images.recommendedTag``.  If you do not find it, then that instance is currently running ``recommended``.

Set this tag to whatever string represents the correct image for that instance.
Once this change is merged, sync the nublado application (using Argo CD) in the affected environments.

You do not have to wait for a maintenance window to do this, since the change is low risk, although it will result in a very brief outage for Notebook Aspect lab spawning while the JupyterLab Controller is restarted.

It may take a few minutes for the image pulling to complete, but after that interval, the menu will be correct again.

