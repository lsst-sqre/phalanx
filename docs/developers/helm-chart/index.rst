#####################################
Write a Helm chart for an application
#####################################

Argo CD manages applications in the Rubin Science Platform through a set of Helm charts.
Which Helm charts to deploy in a given environment is controlled by the :file:`values.yaml` and :file:`values-{environment}.yaml` files in `/environments <https://github.com/lsst-sqre/phalanx/tree/main/environments/>`__.

The `applications <https://github.com/lsst-sqre/phalanx/tree/main/applications/>`__ directory defines templates in its :file:`templates` directory and values to resolve those templates in :file:`values.yaml` and :file:`values-{environment}.yaml` files to customize the application for each environment.
For first-party charts, the :file:`templates` directory is generally richly populated.

Phalanx extends Helm charts with additional files, annotations, and injected values.
Even if you are already familiar with writing Helm charts, there are some Phalanx-specific details.

.. seealso::

   These pages focus on writing your own Helm chart.
   If you are deploying a third-party application that already has a Helm chart, see :doc:`/developers/add-external-chart`.

   In some cases where there is a lot of internal duplication between multiple Phalanx applications, those applications should share a subchart that encapsulates that duplication.
   See :doc:`/developers/shared-charts` if you think that may be the case for your application.

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Basics
   :name: dev-helm-basics-toc

   create-new-chart
   chart-yaml
   templates
   values-yaml
   define-secrets
   check-chart
   add-application

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Common patterns

   container-tmp
   pull-secrets
   workload-identity
   cloud-sql

Examples
========

Existing Helm charts that are good examples to read or copy are:

- `mobu <https://github.com/lsst-sqre/phalanx/tree/main/applications/mobu>`__ (fairly simple)
- `hips <https://github.com/lsst-sqre/phalanx/tree/main/applications/hips>`__ (simple but with workload identity)
- `gafaelfawr <https://github.com/lsst-sqre/phalanx/tree/main/applications/gafaelfawr>`__ (complex, including CRDs, multiple pods, and Cloud SQL)
