################################################
Google Cloud Artifact Registry (GAR) integration
################################################

Cachemachine optionally supports using the Google Cloud Artifact Registry (GAR) API to list images rather than the Docker API.

This allows workload identity credentials to be used instead of Docker credentials when the images are stored in GAR.
Docker client authentication with GAR is cumbersome because a JSON token is used for authentication, and that token contains special characters that make it difficult to pass between multiple secret engine layers.

Using the GAR API directly also avoids the need to build a cache of hashes to resolve tags to images.
The Docker API returns a list of images with a single tag, which requires constructing a cache of known hashes to determine which tags are alternate names for images that have already been seen.
The GAR API returns a list of images with all tags for that image, avoiding this problem.

Container Image Streaming
=========================

`Container Image Streaming <https://cloud.google.com/blog/products/containers-kubernetes/introducing-container-image-streaming-in-gke>`__ is used by cachemachine to decrease the time for the image pull time.
It's also used when an image isn't cached, which makes it practical to use uncached images.
With normal Docker image retrieval, using an uncached image can result in a five-minute wait and an almost-certain timeout.

The ``sciplatlab`` images are 4GB.
Image pull time for those images decreased from 4 minutes to 30 seconds using image streaming.

Image streaming is per project by enabling the ``containerfilesystem.googleapis.com`` API.
This was enabled via Terraform for the Interim Data Facility environments.

Workload Identity
=================

`Workload Identity <https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity>`__ is used by Cachemachine to authenticate to the GAR API.
Workload Identity allows Kubernetes service accounts to impersonate Google Cloud Platform (GCP) Service Accounts to authenticate to GCP services.
Workload Identity is enabled on all of the Rubin Science Platform (RSP) Google Kuberentes Engine (GKE) Clusters.

The binding between the Kubernetes and the GCP service account is done through IAM permissions deployed via Terraform.
The following Kubernetes annotation must be added to the Kubernetes ``ServiceAccount`` object as deployed via Phalanx to bind that service account to the GCP service account.

.. code-block:: yaml

   serviceAccount:
     annotations: {
       iam.gke.io/gcp-service-account: cachemachine-wi@science-platform-dev-7696.iam.gserviceaccount.com
     }

To troubleshoot or validate Workload Identity, a test pod can be provisioned using [these instructions](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#verify_the_setup)

Validating operations
=====================

To validate cachemachine is running, check the status page at ``https://data-dev.lsst.cloud/cachemachine/jupyter``.
(Replace ``data-dev`` with the appropriate environment.)
Check the ``common_cache`` key for cached images, and see if ``images_to_cache`` is blank or only showing new images that are in the process of being downloaded.

Future work
===========

- Cachemachine and Nublado both default to configuring an image pull secret when spawning pods.
  This value is not used by GAR.
  In GKE, the nodes default to using the built-in service account to pull images.
  This means we can drop the ``pull-secret`` secret and its configuration when GAR is in use.

- Image streaming is currently a per-region setting.
  If GKE clustes are deployed outside of ``us-central1`` in the future, a GAR repository should be created for that region to stream images.
