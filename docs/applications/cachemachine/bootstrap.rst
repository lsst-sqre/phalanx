.. px-app-bootstrap:: cachemachine

##########################
Bootstrapping cachemachine
##########################

By default, cachemachine doesn't do any prepulling and doesn't provide a useful menu for Notebook Aspect spawning.
As part of bootstrapping a new environment, you will want to configure it to prepull appropriate images.

For deployments on Google Kubernetes Engine, you will want to use Google Artifact Repository (GAR) as the source of images.
See :doc:`gar` for basic information and instructions on how to configure workload identity.
A good starting point for the cachemachine configuration is the `configuration from the IDF environment <https://github.com/lsst-sqre/phalanx/blob/master/applications/cachemachine/values-idfprod.yaml>`__, which sets up GAR as the image source and prepulls a reasonable number of images.

For Telescope and Site deployments that need special images and image cycle configuration, start from the `summit configuration <https://github.com/lsst-sqre/phalanx/blob/master/applications/cachemachine/values-summit.yaml>`__.
Consult with Telescope and Site to determine the correct recommended tag and cycle number.

For other deployments that use the normal Rubin Notebook Aspect images, a reasonable starting configuration for cachemachine is:

.. code-block:: yaml

   autostart:
     jupyter: |
       {
         "name": "jupyter",
         "labels": {},
         "repomen": [
           {
             "type": "RubinRepoMan",
             "registry_url": "registry.hub.docker.com",
             "repo": "lsstsqre/sciplat-lab",
             "recommended_tag": "recommended",
             "num_releases": 1,
             "num_weeklies": 2,
             "num_dailies": 3
           }
         ]
       }

This prepulls the latest release, the latest two weeklies, and the latest three dailies, as well as the image tagged ``recommended``.
However, also see :ref:`prepull-recommended` for information on how to ensure cachemachine knows the correct tag and description for the recommended image.
