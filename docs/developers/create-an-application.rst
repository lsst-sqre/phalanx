##########################
Building a new application
##########################

This page provides general guidance for creating an application in Python that can be deployed through Phalanx.
If the goal is to instead deploy an existing third-party application with its own Helm chart in the Rubin Science Platform, see :doc:`add-external-chart`.

To be deployed in the Rubin Science Platform, an application must come in the form of one or more Docker images and a Helm chart (or Kustomize configuration, although no application currently uses that approach) that deploys those images in Kubernetes.

After you have finished the steps here, add any secrets you need for your application: :doc:`add-a-onepassword-secret`.
Once you have done that, add the application to Phalanx: :doc:`add-application`.

Write the application
=====================

Rubin-developed applications for the Rubin Science Platform should be written in Python unless there's some reason (such as using code developed elsewhere) that forces choice of a different language.
For the common case of a web application (one that exposes an API via HTTP), we recommend using the `FastAPI framework <https://fastapi.tiangolo.com/>`__.

The easiest way to start a new FastAPI_ application written in Python and intended for the Rubin Science Platform is to create a new project using sqrbot-jr.
On the LSSTC Slack, send the message ``create project`` to ``@sqrbot-jr``.
Select ``FastAPI application (Safir)`` from the list of project types.
This will create a new GitHub repository with the basic framework of a FastAPI_ application that will work well inside the Rubin Science Platform.
The template uses Safir_ to simplify and regularize many parts of your FastAPI_ application, from logger to database handling.

Any Python application destined for the RSP should regularly update its dependencies to pick up any security fixes.
If your application follows the code layout of the FastAPI template, use `neophile <https://neophile.lsst.io/>`__ to automatically create PRs to update your dependencies.
To add your application to the list of repositories that neophile updates, submit a PR to add the repository owner and name to `neophile's configuration <https://github.com/lsst-sqre/roundtable/blob/master/deployments/neophile/values.yaml>`__.

Each release of your application must be tagged.
The tag should use `semantic versioning`_ (for example, ``1.3.2``).
Creating a GitHub release for the tag is optional but recommended, and we recommend setting the title of the release to the name of the tag.
If you are using the FastAPI template, tagging in this fashion is required since it triggers the GitHub Actions workflow to build and publish a Docker image with a tag matching the release version.

Create the Docker image
=======================

The Docker image can be stored in any container registry that is usable by Kubernetes, but for Rubin-developed applications using the FastAPI template, we usually push `GitHub Container Registry (ghcr.io) <https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry>`__.
The Google Artifact Registry hosts the Science Platform images and may eventually be used more widely.
If your image must be stored in a private container registry, the credentials for that registry must be added to the pull secret.

If you use the FastAPI application template, a ``Dockerfile`` is be created as part of the new repository template, and a GitHub Actions workflow is set up in the new repository to build and push Docker images for tagged releases.

If you use ``ghcr.io`` as your repository (which is the FastAPI template default) you can use GitHub's built-in ``GITHUB_TOKEN``; you don't need
to create an additional secret.
If you are using Docker Hub you must create two secrets in your new GitHub repository, ``DOCKER_USERNAME`` and ``DOCKER_TOKEN``.
``DOCKER_USERNAME`` should be set to the Docker Hub username of the account that will be pushing the new Docker images.
``DOCKER_TOKEN`` should be set to a secret authentication token for that account.
We recommend creating a separate token for each GitHub repository for which you want to enable automatic image publication, even if they all use the same username.

If using Docker Hub You may need to have a Docker Pro or similar paid Docker Hub account.
Alternately, you can contact SQuaRE to set up Docker image publication using our Docker account.

The next step is to create secrets for your application: :doc:`add-a-onepassword-secret`.

Finally, deploy your application by creating a Helm chart and an Argo CD Application in Phalanx: :doc:`add-application`.
