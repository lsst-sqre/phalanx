##############################################################################
Overview of Cachemachine integration with Google Cloud Artifact Registry (GAR)
##############################################################################

The existing Cachemachine service was updated to support interfacing with the Google Artifact Registry (GAR) API instead of using the docker client.  This allows for workload identity credentials to be used instead of docker credentials.  Docker client authentication with GAR is cumbersome because a JSON token is used for authentication that contains special characters which makes it difficult to pass between multiple secret engine layers.  The other main advantage of interfacing directly with GAR is that a hash cache does not need to be built.  The GAR API returns a list of images with all tags for that image.   The docker client will return a list of images with a single tag.  The single tag per image approach with the docker client requires that a hash cache is built to group the same images together.  That construct is not used by the GAR instance of cachemachine because the image already has the tags included in the API response.

Container Image Streaming
=========================

[Container Image Streaming](https://cloud.google.com/blog/products/containers-kubernetes/introducing-container-image-streaming-in-gke) is used by uncached images and by cachemachine to decrease the time for the image pull time.  The sciplat lab images are 4 GB and the image pull time decreased from 4 minutes to 30 seconds using image streaming.  Image streaming is per project by enabling the `containerfilesystem.googleapis.com` API.  This was enabled via Terraform.


Workload Identity
=================

[Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity) is used by Cachemachine to authenticate with GAR API.  Workload Identity allows kubernetes service accounts to impersonate Google Cloud Platform (GCP) Service Accounts to authenticate to GCP services.  Workload Identity is enabled on all of the Rubin Science Platform (RSP) Google Kuberentes Engine (GKE) Clusters.  The binding between the Kubernetes and the GCP service account is done through IAM permissions deployed via Terraform.  A kubernetes annotation is deployed via phalanx as detailed below to bind the GCP service account to the Kubernetes service account.

```
serviceAccount:
  annotations: {
    iam.gke.io/gcp-service-account: cachemachine-wi@science-platform-dev-7696.iam.gserviceaccount.com
  }
```
To troubleshoot or validate workload identity a test pod can be provisioned using [these instructions](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#verify_the_setup)


Validating Operations
=====================

To validate cachemachine is running check the status page at this url `https://data-dev.lsst.cloud/cachemachine/jupyter`.  Replace `data-dev` with the appropriate environment.  Check the `common_cache` for new images cached and see if in `images_to_cache` is blank or only showing new images that are in the process of being downloaded.


https://data-dev.lsst.cloud/cachemachine/jupyter

Below are notes from the deployment and considerations for future.

* The kubernetes python client defaults to including an image pull secret.  This value is not used by GAR.  In GKE the nodes default to using the built in service account to pull images.  Noting here to avoid confusion in the future.
* Image streaming is currently a per region setting.  If GKE clustes are deployed outside of us-central1 in the future a GAR repo should be created for that region to stream images.