##################################
Getting GKE Kubernetes credentials
##################################

To use the standard Kubernetes administrative command :command:`kubectl` or other commands built on the same protocol (such as Helm_ or the Phalanx installer), you must have authentication credentials stored for the target Kubernetes cluster.
Google provides a mechanism to obtain those credentials using the :command:`gcloud` command:

#. Ensure you have a Google account with access to the Google Cloud Platform project where your target Kubernetes cluster is running.
   For Phalanx environments run by SQuaRE, this access must be via an ``lsst.cloud`` Google account that is used only for Rubin activities.
   If you do not already have such an account or permissions and need administrative access to a Phalanx environment maintained by SQuaRE, contact SQuaRE for access.

#. `Install gcloud <https://cloud.google.com/sdk/docs/install>`__ on the system on which you want to run privileged Kubernetes commands.

#. `Initialize gcloud <https://cloud.google.com/sdk/docs/initializing>`__.
   You will need to have access to the Google Cloud Platform project where your target Kubernetes cluster is running.

   If you have access to multiple Google Cloud Platform projects, you will be asked to select one as your default project.
   You may wish to choose the project for the Phalanx environment you use most often.
   You can find the project ID of a Phalanx project hosted on GKE in its :doc:`environments page </environments>`.

#. `Install kubectl and the GKE auth plugin <https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl>`__.
   As part of that installation, you will run the :command:`gcloud` command that obtains credentials usable by :command:`kubectl` and other privileged Kubernetes commands.
   See below for assistance with the precise :command:`gcloud` command to run.

You will only have to follow this process once on each machine from which you want to use Kubernetes.

The final step has an example :command:`gcloud` command, but it assumes that you are getting credentials for your default project.
Rubin uses multiple Google Cloud Platform projects for different environments, so you may have to provide the project ID as well.
For the full command to run, see the bottom of the relevant :doc:`environments page </environments>`.

.. note::

   The Kubernetes control plane credentials eventually expire and have to be rotated.
   If the control plane credentials of the Kubernetes cluster are rotated, you will have to re-run the :command:`gcloud` command to refresh your credentials.
   If you discover that your credentials are no longer working, try that command and see if the problem persists.
