####################
Create a new service
####################

This documentation is intended for service administrators who are writing a new service in Python.
If the goal is to instead deploy a third-party service with its own Helm chart in the Rubin Science Platform, see :doc:`add-external-chart`.

To be deployed in the Rubin Science Platform, a service must come in the form of one or more Docker images and a Helm chart (or Kustomize configuration, although no service currently uses that approach) that deploys those images in Kubernetes.

After you have finished the steps here, add any secrets you need for your service: :doc:`add-a-onepassword-secret`.  Once you have done that, add the service to ArgoCD: :doc:`add-service`.

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

The Docker image can be stored in any container registry that is usable by Kubernetes, but for Rubin-developed services using the FastAPI template, we usually push both to the `GitHub Container Registry <https://ghcr.io>`__ and Docker Hub.  Google Artifact Registry is in play for Science Platform images and may eventually be used more widely.  We may eventually stop publishing to Docker Hub; our workflow is centered on GitHub and the long-term future of Docker-the-company does not look very secure.
If your image must be stored in a private container registery, the credentials for that registry must be added to the pull secret.

If you use the FastAPI service template, a ``Dockerfile`` will be created as part of the new repository template, and GitHub Actions will be set up in the new repository to build and push new Docker images for tagged releases.

If you use ghcr.io as your repository (which is the FastAPI template
default) you can use GitHub's built-in ``GITHUB_TOKEN``; you don't need
to create an additional secret.
If you are using Docker Hub you must create two secrets in your new GitHub repository, ``DOCKER_USERNAME`` and ``DOCKER_TOKEN``.
``DOCKER_USERNAME`` should be set to the Docker Hub username of the account that will be pushing the new Docker images.
``DOCKER_TOKEN`` should be set to a secret authentication token for that account.
We recommend creating a separate token for each GitHub repository for which you want to enable automatic image publication, even if they all use the same username.

If using Docker Hub You may need to have a Docker Pro or similar paid Docker Hub account.
Alternately, you can contact SQuaRE to set up Docker image publication using our Docker account.

The next step is to create secrets for your application: :doc:`add-a-onepassword-secret`.

Finally, deploy your service by creating a Helm chart and an ArgoCD
Application in Phalanx: :doc:`add-service`.
