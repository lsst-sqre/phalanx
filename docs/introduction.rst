######################################
Introduction to Kubernetes and Argo CD
######################################

The Rubin Science Platform runs on `Kubernetes`_
Kubernetes provides a way to coordinate running services on multiple nodes.
Kubernetes runs a set of `Docker`_ containers and sets up the networking, storage, and configuration of those containers.

Git repositories for individual services typically have build pipelines resulting in new Docker container builds when code changes are merged.
For example, our Jenkins build system builds stack and JupyterLab containers, and the `lsst-tap-service repository <https://github.com/lsst-sqre/lsst-tap-service>`__ builds the TAP service containers.

An service deployed on Kubernetes is made up of a number of resources, such as p
ods, deployments, and configmaps.
These resources must be configured to work together to form a logical service, such as the Portal or Notebook Aspects.
Each logical service is contained in a `Helm`_ chart that uses templates to create each resource with some configuration applied.
The configuration for a Helm chart is called a values file, and is a simple YAML document that contains inputs for the templating of the chart.

Be aware that, confusingly, both "service" and "application" are also names of specific Kubernetes resources that are only one component of a logical service.
In the rest of this documentation, "service" refers to the logical service, not the Kubernetes resource.
Argo CD manages resources via an abstraction called an "application," which tells Argo CD what Helm chart to use to manage the resources.
In the rest of this documentation, "application" will refer to the Argo CD abstraction concept.
In general, each Argo CD application corresponds to a logical service.

But Helm doesn't keep track of the service once it is deployed.
That is, it won't notice when the configuration changes and apply those changes.
`Argo CD`_ fills this need.
Argo CD watches its source repository for new Git commits and will keep track of those changes, either applying them automatically ("syncing" them), or waiting for an operator to press the sync button in the web UI.
Argo CD is the only layer in this stack that has a web UI that can be easily navigated, and it provides many useful features, such as deleting resources and resyncing services.

The Rubin Science Platform stores its Argo CD configuration in the `phalanx repository`_.
This includes the Argo CD application resources, pointers to the Helm charts for all services that are installed as part of the Science Platform, and values files to configure those services.
