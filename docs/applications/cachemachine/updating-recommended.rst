##############################################
Updating the recommended Notebook Aspect image
##############################################

The ``recommended`` tag for JupyterLab images is usually a recent weekly image.
The image tagged ``recommended`` is guaranteed by SQuaRE to be compatible with other services and materials, such as tutorial or system testing notebooks, that we make available on RSP deployments.

Because this process requires quite a bit of checking and sign-off from multiple stakeholders, it is possible that approving a new recommended version may take more than the two weeks (for most deployments) it takes for a weekly image to roll off the default list of images to pull.
This can cause the RSP JupyterHub options form to display empty parentheses rather than the correct target version when a user requests a lab container.

This document explains the process for moving the ``recommended`` tag, and how to circumvent that display bug by changing cachemachine's ``values-<instance>.yaml`` for the appropriate instance when moving the ``recommended`` tag.

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

Ensure the recommended image is pre-pulled
------------------------------------------

In most environments, cachemachine only prepulls the latest two weekly images.
It is common for more than two weeks to go by before approving a new version of recommended.
While the recommended tag is always prepulled, cachemachine cannot resolve that tag to a regular image tag unless the corresponding image tag is also prepulled.
The result is a display bug where recommended is not resolved to a particular tag, and therefore is missing the information in parentheses after the :guilabel:`Recommended` menu option in the spawner form.

To avoid this, we therefore explicitly prepull the weekly tag corresponding to the ``recommended`` tag.
This ensures that cachemachine can map the ``recommended`` tag to a weekly tag.
This doesn't consume any additional cache space on the nodes, since Kubernetes, when cachemachine tells it to cache that weekly tag, will realize that it already has it cached under another name.

We add this configuration to the IDF environments.
Other Phalanx environments handle recommended images differently and don't need this configuration.

In cachemachine's ``values-<instance>.yaml`` file for the affected environment, go towards the bottom and look in ``repomen``.
The first entry will always be of type ``RubinRepoMan``, and will contain the definitions of how many daily, weekly, and release images to prepull.
Beneath the ``RubinRepoMan`` entry, you should find an entry that looks like:

.. code-block:: json

   {
     "type": "SimpleRepoMan",
     "images": [
       {
         "image_url": "registry.hub.docker.com/lsstsqre/sciplat-lab:w_2021_33",
         "name": "Weekly 2021_33"
       }
     ]
   }

Replace the tag and name with the weekly tag and corresponding name for the weekly image that is also tagged ``recommended``.

Once this change is merged, sync cachemachine (using Argo CD) in the affected environments.
You do not have to wait for a maintenance window to do this, since the change is low risk, although it will result in a very brief outage for Notebook Aspect lab spawning while cachemachine is restarted.

cachemachine will then spawn a ``DaemonSet`` that pulls the weekly tag to every node, which as mentioned above will be fairly quick since Kubernetes will realize it already has the image cached under another name.
Once cachemachine rechecks the cached images on each node, it will have enough information to build the menu correctly, and the spawner menu in the Notebook Aspect should be correct.
