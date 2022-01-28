######################
Updating "recommended"
######################

The "recommended" tag for JupyterLab images is usually a recent weekly image.
The image marked "recommended" is guaranteed by SQuaRE to be compatible with other services and materials--such as tutorial or system testing notebooks--that we make available on RSP deployments.
Because this process requires quite a bit of checking and sign-off from multiple stakeholders, it is possible that approving a new version for "recommended" may take more than the two weeks (for most deployments) it takes for a weekly image to roll off the default list of images to pull.
This can cause the RSP JupyterHub options form to display empty parentheses rather than the correct target version when a user requests a lab container.

This document explains how to circumvent that display bug by changing cachemachine's ``values-<instance>.yaml`` for the appropriate instance when moving the "recommended" tag.

Tagging a new container version
--------------------------------

When a new version is to be approved (after passing through its prior QA and sign-off gates), the "recommended" tag must be updated to point to the new version.

This really is as simple as pulling the new target version, tagging it as recommended, and pushing it again.
This is, sadly, necessary — there is no way to tag an image on Docker Hub without pulling and re-pushing it.
However, the push will be a no-op, since all the layers are, by definition, already there, so while the pull may be slow, the push will be fast.

The procedure is as follows:

.. code-block:: sh

   docker pull registry.hub.docker.com/lsstsqre/sciplat-lab:w_2021_33  # or whatever tag
   docker tag registry.hub.docker.com/lsstsqre/sciplat-lab:w_2021_33 registry.hub.docker.com/lsstsqre/sciplat-lab:recommended
   docker login  # This may require interaction, depending on how you've set up your docker credentials
   docker push registry.hub.docker.com/lsstsqre/sciplat-lab:recommended

The DockerHub ``sqreadmin`` user could be used for this; however, when the process is not automated (it currently is not), using personal credentials is acceptible.
The ``sqreadmin`` DockerHub credentials are within the SQuaRE 1Password credential store.

.. _prepull-recommended:

Updating Phalanx to ensure the "recommended" target is pre-pulled
-----------------------------------------------------------------

In most environments, cachemachine only ensures pulling of the latest two weekly images, and it is therefore not at all unusual for more than two weeks to go by before approving a new version.

Usually this doesn't matter: the image cache on a node uses a Least Recently Used replacement strategy, and the great majority of users spawn "recommended," so it's not going to be purged.
However, there is a display bug in the Notebook Aspect spawner form can occur.
If a new node has come online after the recommended weekly has rolled out of the weekly list, then, although the new node will pre-pull "recommended", it will not pre-pull the corresponding weekly by the weekly tag
Cachemachine, and therefore the options form, will fail to resolve "recommended" to a particular weekly, which means the description in parentheses after the image name will be empty.

Fortunately, this is easy to fix.

In cachemachine's ``values-<instance>.yaml`` file for the affected environment, go towards the bottom and look in ``repomen``.
The first entry will always be of type ``RubinRepoMan``, and will contain the definitions of how many daily, weekly, and release images to prepull.

There are currently only four environments in which we care about keeping the "recommended" target pre-pulled:

#. IDF Production (``data.lsst.cloud``)
#. IDF Integration (``data-int.lsst.cloud``)
#. NCSA Stable (``lsst-lsp-stable.ncsa.illinois.edu``)
#. NCSA Integration (``lsst-lsp-int.ncsa.illinois.edu``)

Beneath the ``RubinRepoMan`` entry, you should find an entry that looks like:

.. code-block:: yaml

   {
     "type": "SimpleRepoMan",
     "images": [
       {
         "image_url": "registry.hub.docker.com/lsstsqre/sciplat-lab:w_2021_33",
         "name": "Weekly 2021_33"
       }
     ]
   }

Replace the tag and image name with the current approved versions.

If you are adding these definitions to an instance that does not already ensure that the target image for "recommended" is always prepulled, add an entry to the ``repomen`` list that looks like the above, with current approved versions.

Commit your changes to a git branch, and then create a GitHub pull request to ``services/cachemachine`` in `Phalanx <https://github.com/lsst-sqre/phalanx/tree/master/services/cachemachine/>`__ from that branch.
Request that someone review the PR, and then merge it.

Then synchronize cachemachine (using Argo CD) in the correct environment.
It is not generally required to wait for a maintenance window to do this, since making this change is low-risk.
The cachemachine deployment will automatically restart, and that will kick off any required pulls.
Since these pulls will just be pulling "recommended" under a different name, the image will almost certainly already be cached, and therefore the pull will be near-instant.
Each pod that starts from the pulled image simply sleeps for one minute and then terminates.
After each pod has run and terminated, the Notebook Aspect options form will again show the correct data.
