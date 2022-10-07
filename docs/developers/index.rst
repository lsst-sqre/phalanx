##########
Developers
##########

Developers can deploy their applications on Rubin's Kubernetes environments, such as the Rubin Science Platform, by integrating their service with Phalanx.
In this section of the Phalanx documentation you can learn how to build and integrate your service with Phalanx, and how to test your service's deployment in development Phalanx environments.

For background on Phalanx and how to contribute to the Phalanx repository itself, see the :doc:`/about/index` section.
Individual services are documented in :doc:`/applications/index` section.

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Build

   create-service

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Integration

   service-chart-architecture
   add-service
   add-external-chart
   add-a-onepassword-secret
   update-a-onepassword-secret

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Deploy & maintain

   upgrade
   deploy-from-a-branch
   local-development
