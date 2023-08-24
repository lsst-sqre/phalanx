##############
Administrators
##############

A Phalanx administrator is someone who is responsible for defining a Phalanx environment, installing Phalanx in that environment, and maintaining the resulting cluster.
Administrators operate infrastructure, manage secrets, and are involved in the deployment, configuration, and Argo CD synchronization of applications.

.. toctree::
   :caption: Initial install
   :maxdepth: 1
   :name: bootstrapping-toc

   requirements
   hostnames
   secrets-setup
   installation

.. toctree::
   :caption: Procedures
   :maxdepth: 1

   upgrade-windows
   sync-argo-cd
   sync-secrets
   audit-secrets
   update-pull-secret

.. toctree::
   :caption: Troubleshooting
   :maxdepth: 2

   troubleshooting

.. toctree::
   :caption: Infrastructure
   :maxdepth: 2

   infrastructure/filestore/index

.. toctree::
   :caption: Reference
   :maxdepth: 1

   cli
