######################
Updating "recommended"
######################

The "recommended" tag for JupyterLab images is generally a weekly image, and generally it is not too far out of date.

Tagging a new container version
--------------------------------

When a new version is to be blessed, the "recommended" tag must be updated to point to the new version.

This really is as simple as pulling the new target version, tagging it as recommended, and pushing it again.
This is, sadly, necessary--there is no way to tag an image on Docker Hub without pulling and re-pushing it.
However, the push will be a no-op, since all the layers are, by definition, already there, so while the pull may be slow, the push will be fast.

The procedure is as follows:

.. code-block:: sh

   docker pull registry.hub.docker.com/lsstsqre/sciplat-lab:w_2021_33  # or whatever tag
   docker tag registry.hub.docker.com/lsstsqre/sciplat-lab:w_2021_33 registry.hub.docker.com/lsstsqre:recommended
   docker login  # This may require interaction, depending on how you've set up your docker credentials
   docker push registry.hub.docker.com/lsstsqre/sciplat-lab:recommended

Updating Phalanx to ensure the "recommended" target is pre-pulled
-----------------------------------------------------------------

However, in most environments, cachemachine only ensures pulling of the latest two weekly images, and it is not at all unusual for more than two weeks to go by before blessing a new version.

Usually this doesn't matter: the image cache on a node is Least Recently Used, and the great majority of users spawn "recommended," so it's not going to be purged.
However, there is a display bug in the nublado2 options form that can occur.

If a new node has come online after the recommended weekly has rolled out of the weekly list, then, although the new node will pre-pull "recommended", it will not pre-pull the corresponding weekly by the weekly tag, and thus cachemachine, and therefore the options form, will fail to resolve "recommended" to a particular weekly, which means the description in parentheses after the image name will be empty.

Fortunately, this is easy to fix.

In cachemachine's ``values.yaml`` file for the affected environment, go towards the bottom and look in ``repomen``.
If you only see one entry in that list, of type ``RubinRepoMan``, then you should add a second entry, which should look like:

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

(replace the tag and description with the correct ones, obviously).

If there already is such a ``SimpleRepoMan`` entry, but it has an older tag or name, replace those with the correct versions.

Then synchronize cachemachine (using ArgoCD) in the correct environment.
The deployment will automatically restart, and that will kick off any required pulls.
Since these pulls will just be pulling "recommended" under a different name, the image will almost certainly already be cached, and therefore the pull will be near-instant.
After a minute of runtime plus the termination time for each pod, the nublado2 options form will again show the correct data.
