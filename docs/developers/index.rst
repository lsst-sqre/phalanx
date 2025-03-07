##########
Developers
##########

Developers can deploy their applications on Rubin's Kubernetes environments, such as the Rubin Science Platform, by integrating into Phalanx.
In this section of the Phalanx documentation you can learn how to build and integrate your application, and how to test your application's deployment in development Phalanx environments.

For background on Phalanx and how to contribute to the Phalanx repository itself, see the :doc:`/about/index` section.
Individual applications are documented in the :doc:`/applications/index` section.

.. note::

   If you are maintaining Phalanx applications, contact SQuaRE to be added as a contributor to the https://github.com/lsst-sqre/phalanx repository.
   Several of the steps below requiring pushing your development branches to that repository rather than using a fork.

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

   helm-chart/index
   add-external-chart
   shared-charts

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Deploy & maintain
   :name: dev-deploy-toc

   get-application-logs
   upgrade
   update-a-secret
   deploy-from-a-branch
   switch-environment-to-branch
   resource-limits

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Reference
   :name: dev-reference-toc

   secrets-spec
   injected-values

.. seealso::

   SQuaRE ran a bootcamp for Phalanx application developers in May of 2024.
   Rubin affiliates can watch the session recordings and see the slides of those presentations on the `SQuaRE bootcamp Confluence page <https://rubinobs.atlassian.net/wiki/spaces/DM/pages/48836049/SQuaRE+Bootcamp+-+May+6-10+2024>`__.
