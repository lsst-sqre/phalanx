##############
Administrators
##############

A Phalanx administrator is someone who is responsible for defining a Phalanx environment, installing Phalanx in that environment, and maintaining the resulting cluster.
Administrators operate infrastructure, manage secrets, and are involved in the deployment, configuration, and Argo CD synchronization of applications.

.. note::

   If you are maintaining a Phalanx environment, contact SQuaRE to be added as a contributor to the https://github.com/lsst-sqre/phalanx repository.
   Some of the steps below may require pushing your development branches to that repository rather than using a fork.

.. toctree::
   :caption: Initial install
   :maxdepth: 1
   :name: bootstrapping-toc

   requirements
   hostnames
   create-environment
   secrets-setup
   installation

.. toctree::
   :caption: Procedures
   :maxdepth: 1

   upgrade-windows
   sync-argo-cd
   add-new-secret
   update-a-secret
   sync-secrets
   audit-secrets
   update-pull-secret
   migrating-secrets
   set-quotas

.. toctree::
   :caption: Troubleshooting
   :maxdepth: 2

   troubleshooting
   outage-comms

.. toctree::
   :caption: Infrastructure
   :maxdepth: 2

   infrastructure/google/index
   infrastructure/filestore/index
   infrastructure/kubernetes-node-status-max-images

.. toctree::
   :caption: Reference
   :maxdepth: 1

   cli
