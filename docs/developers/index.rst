##########
Developers
##########

Developers can deploy their applications on Rubin's Kubernetes environments, such as the Rubin Science Platform, by integrating into Phalanx.
In this section of the Phalanx documentation you can learn how to build and integrate your application, and how to test your application's deployment in development Phalanx environments.

For background on Phalanx and how to contribute to the Phalanx repository itself, see the :doc:`/about/index` section.
Individual applications are documented in the :doc:`/applications/index` section.

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Build
   :name: dev-build-toc

   create-an-application

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Integration
   :name: dev-int-toc

   write-a-helm-chart
   add-external-chart
   shared-charts
   define-secrets
   add-application

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Deploy & maintain
   :name: dev-deploy-toc

   get-application-logs
   upgrade
   update-a-onepassword-secret
   deploy-from-a-branch
   local-development

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Reference
   :name: dev-reference-toc

   secrets-spec
