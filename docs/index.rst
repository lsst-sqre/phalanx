################################################################
Phalanx: Rubin Observatory Kubernetes Application Configurations
################################################################

Phalanx [#name]_ is a GitOps repository for Rubin Observatory's Kubernetes environments, notably including Rubin Science Platform deployments like https://data.lsst.cloud.
Using Helm_ and `Argo CD`_, Phalanx defines the configurations of applications in each environment.

This documentation is for Rubin team members that are developing applications and administering Kubernetes clusters.
Astronomers and other end-users can visit the `Rubin Documentation Portal <https://www.lsst.io>`__ to learn how to use Rubin Observatory's software, services, and datasets.

Phalanx is on GitHub at https://github.com/lsst-sqre/phalanx.

.. [#name] A phalanx is a SQuaRE deployment (Science Quality and Reliability Engineering, the team responsible for the Rubin Science Platform).
   Phalanx is how we ensure that all of our applications work together as a unit.

.. toctree::
   :maxdepth: 1
   :hidden:

   about/index
   developers/index
   admin/index
   applications/index
   environments/index

.. grid:: 3

   .. grid-item-card:: About
      :link: about/index
      :link-type: doc

      Learn about Phalanx's design and how to contribute.

   .. grid-item-card:: Developers
      :link: developers/index
      :link-type: doc

      Learn how to develop applications that are deployed with Phalanx.

   .. grid-item-card:: Administrators
      :link: admin/index
      :link-type: doc

      Learn how install and operate Phalanx applications, such as the Rubin Science Platform, in your data access center.

.. grid:: 2

   .. grid-item-card:: Applications
      :link: applications/index
      :link-type: doc

      Learn about the individual applications that are configured to deploy with Phalanx.

   .. grid-item-card:: Environments
      :link: environments/index
      :link-type: doc

      Learn about the Kubernetes clusters that are running Phalanx.
