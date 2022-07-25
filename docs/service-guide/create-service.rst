####################
Create a new service
####################

This documentation is intended for service administrators who are writing a new service in Python.
If the goal is to instead deploy a third-party service with its own Helm chart in the Rubin Science Platform, see :doc:`add-external-chart`.

To be deployed in the Rubin Science Platform, a service must come in the form of one or more Docker images and a Helm chart (or Kustomize configuration, although no service currently uses that approach) that deploys those images in Kubernetes.

After you have finished the steps here, go to :doc:`add-service`.

Write the service
=================

Rubin-developed services for the Rubin Science Platform should be written in Python unless there's some reason (such as using code developed elsewhere) that forces choice of a different language.
For the common case of a web service (one that exposes an API via HTTP), we recommend using the `FastAPI framework <https://fastapi.tiangolo.com/>`__.

The easiest way to start a new FastAPI service written in Python and intended for the Rubin Science Platform is to create a new project using sqrbot-jr.
On the LSST Slack, send the message ``create project`` to ``@sqrbot-jr``.
Select ``FastAPI application (Safir)`` from the list of project types.
This will create a new GitHub repository with the basic framework of a FastAPI service that will work well inside the Rubin Science Platform.

Any Python service destined for the RSP should regularly update its dependencies to pick up any security fixes.
If your service follows the code layout of the FastAPI service template, using `neophile <https://neophile.lsst.io/>`__ to automatically create PRs to update your dependencies is strongly recommended.
To add your service to the list of repositories that neophile updates, submit a PR to add the repository owner and name to `neophile's configuration <https://github.com/lsst-sqre/roundtable/blob/master/deployments/neophile/values.yaml>`__.

Each release of your service must be tagged.
The tag should use `semantic versioning`_ (for example, ``1.3.2``).
Creating a GitHub release for the tag is optional but recommended, and we recommend setting the title of the release to the name of the tag.
If you are using the FastAPI template, tagging in this fashion is required since it triggers the GitHub Actions workflow to build and publish a Docker image with a tag matching the release version.

Create the Docker image
=======================

The Docker image can be stored in any container registry that is usable by Kubernetes, but for Rubin-developed services, we normally use DockerHub.
(We may switch to the Google Container Registry later, but for now DockerHub is used for all images.)
If your image must be stored in a private container registery, the credentials for that registry must be added to the pull secret.

If you use the FastAPI service template, a ``Dockerfile`` will be created as part of the new repository template, and GitHub Actions will be set up in the new repository to build and push new Docker images for tagged releases.
To enable this workflow, you must create two secrets in your new GitHub repository, ``DOCKER_USERNAME`` and ``DOCKER_TOKEN``.
``DOCKER_USERNAME`` should be set to the DockerHub username of the account that will be pushing the new Docker images.
``DOCKER_TOKEN`` should be set to a secret authentication token for that account.
We recommend creating a separate token for each GitHub repository for which you want to enable automatic image publication, even if they all use the same username.

You may need to have a Docker Pro or similar paid DockerHub account.
Alternately, you can contact SQuaRE to set up Docker image publication using our Docker account.

Create the Helm chart
=====================

To deploy your service in the Rubin Science Platform, it must have either a Helm chart or a Kustomize configuration.
Currently, all services use Helm charts.
Kustomize is theoretically supported but there are no examples of how to make it work with multiple environments.
Using a Helm chart is recommended unless you are strongly motivated to work out the problems with using Kustomize and then document the newly-developed process.

Unfortunately, unlike for the service itself, we do not (yet) have a template for the Helm chart.
However, Helm itself has a starter template that is not awful.
Use ``helm create`` to create a new chart from that template.
**Be sure you are using Helm v3.**
Helm v2 is not supported.

You will need to make at least the following changes to the default Helm chart template:

- All secrets must come from ``VaultSecret`` resources, not Kubernetes ``Secret`` resources.
  You should use a configuration option named ``vaultSecretsPath`` in your ``values.yaml`` to specify the path in Vault for your secret.
  This option will be customized per environment when you add the service to Phalanx (see :doc:`add-service`).
  See :doc:`add-a-onepassword-secret` for more information about secrets.
- Services providing a web API should be protected by Gafaelfawr and require an appropriate scope.
  This normally means adding annotations to the ``Ingress`` resource via ``values.yaml`` similar to:

  .. code-block:: yaml

     ingress:
       annotations:
         nginx.ingress.kubernetes.io/auth-method: "GET"
         nginx.ingress.kubernetes.io/auth-url: "http://gafaelfawr.gafaelfawr.svc.cluster.local:8080/auth?scope=exec:admin"

  For user-facing services you will want a scope other than ``exec:admin``.
  See `the Gafaelfawr documentation <https://gafaelfawr.lsst.io/>`__, specifically `protecting a service <https://gafaelfawr.lsst.io/applications.html#protecting-a-service>`__ for more information.
- If your service exposes Prometheus endpoints, you will want to configure these in the `telegraf service's prometheus_config <https://github.com/lsst-sqre/phalanx/blob/master/services/telegraf/values.yaml#L36>`__.

Documentation
-------------

We have begun using `helm-docs <https://github.com/norwoodj/helm-docs>`__ to generate documentation for our Helm charts.
This produces a nice Markdown README file that documents all the chart options, but it requires special formatting of the ``values.yaml`` file that is not present in the default Helm template.
If you want to do the additional work, this will produce the most nicely-documented Helm chart, but using helm-docs is currently optional.

Publication
-----------

All Rubin-developed Helm charts for the Science Platform are stored in the `charts repository <https://github.com/lsst-sqre/charts/>`__.
This repository automatically handles publication of the Helm chart when a new release is merged to the ``master`` branch, so you will not have to set up your own Helm chart repository.
You should create your new chart as a pull request in this repository, under the ``charts`` subdirectory.

Examples
--------

Existing Helm charts that are good examples to read or copy are:

- `cachemachine <https://github.com/lsst-sqre/charts/tree/master/charts/cachemachine>`__ (fairly simple)
- `mobu <https://github.com/lsst-sqre/charts/tree/master/charts/mobu>`__ (also simple)
- `gafaelfawr <https://github.com/lsst-sqre/charts/tree/master/charts/gafaelfawr>`__ (complex, including CRDs and multiple pods)
