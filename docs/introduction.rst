######################################
Introduction to Kubernetes and Argo CD
######################################

The Rubin Science Platform runs on `Kubernetes`_
Kubernetes provides a way to coordinate running services on multiple nodes.
Kubernetes runs a set of `Docker`_ containers and sets up the networking, storage, and configuration of those containers.

.. _Kubernetes: https://kubernetes.io/
.. _Docker: https://docker.com/

Git repositories for individual services typically have build pipelines resulting in new Docker container builds when code changes are merged.
For example, our Jenkins build system builds stack and JupyterLab containers, and the `lsst-tap-service repository <https://github.com/lsst-sqre/lsst-tap-service>`__ builds the TAP service containers.

An application deployed on Kubernetes is made up of a number of resources, such as pods, deployments, and services.
These resources must be configured to work together to form a logical service, such as the Portal or Notebook Aspects.
Each logical application is contained in a `Helm`_ chart that uses templates to create each resource with some configuration applied.
The configuration for a Helm chart is called a values file, and is a simple YAML document that contains inputs for the templating of the chart.

But Helm doesn't keep track of the application once it is deployed.
That is, it won't notice when the configuration changes and apply those changes.
`Argo CD`_ fills this need.
Argo CD watches its source repository for new Git commits and will keep track of those changes, either applying them automatically ("syncing" them), or waiting for an operator to press the sync button in the web UI.
Argo CD is the only layer in this stack that has a web UI that can be easily navigated, and it provides many useful features, such as deleting resources and resyncing applications.

The Rubin Science Platform stores its Argo CD configuration in the `phalanx repository <https://github.com/lsst-sqre/phalanx>`__.
This includes the Argo CD application resources, pointers to the Helm charts for all applications that are installed as part of the Science Platform, and values files to configure those applications.
