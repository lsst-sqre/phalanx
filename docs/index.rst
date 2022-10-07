#################################################
Phalanx: Rubin Observatory Kubernetes Deployments
#################################################

Phalanx [#name]_ is a GitOps repository for Rubin Observatory's Kubernetes clusters, notably including the Rubin Science Platform deployments like https://data.lsst.cloud.
Using Helm_ and `Argo CD`_, Phalanx defines the configuration of services in each environment.

This documentation is for Rubin team members that are building services and operating Kubernetes clusters.
Astronomers and other end-users can visit the Rubin Documentation Portal to learn how to use Rubin Observatory's software, services, and datasets.

Phalanx is on GitHub at https://github.com/lsst-sqre/phalanx.

.. [#name] A phalanx is a SQuaRE deployment (Science Quality and Reliability Engineering, the team responsible for the Rubin Science Platform).
   Phalanx is how we ensure that all of our services work together as a unit.

.. toctree::
   :maxdepth: 1
   :hidden:

   overview/index
   service-guide/index
   ops/index
   services/index
   environments/index
