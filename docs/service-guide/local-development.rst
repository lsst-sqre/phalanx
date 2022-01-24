####################################################
Set up a local development environment with minikube
####################################################

Using `minikube <https://minikube.sigs.k8s.io/docs/>`__ you can quickly set up a local Kubernetes cluster to help you adding a service to Phalanx (see :doc:`add-service`).
There are multiple ways to start a minikube cluster.
Here we document the steps to start minikube on macOS (amd64 or arm64) using the `docker driver <https://minikube.sigs.k8s.io/docs/drivers/docker/>`__.

You may be able to deploy the entire Science Platform, provided that you have enough cpu and memory.
If not, you can enable only the essential services to develop with minikube.


Start minikube
==============

#. `Install minikube <https://minikube.sigs.k8s.io/docs/start/>`__ for your platform.

#. Start a cluster using the docker driver with the minimum recommended resources:

.. code-block:: sh

  minikube start --driver=docker --cpus=4 --memory=8g --disk-size=100g  --kubernetes-version=1.21.5

The ``--kubernetes-version`` option can be used to specify the k8s version to use.


Enable the Ingress controller
-----------------------------

We recommend using the `minikube ingress addon <https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/>`__ to enable ingress on minikube with the NGINX Ingress Controller.

.. code-block:: sh

  minikube addons enable ingress


Deploy the minikube environment
===============================

Requirements
------------

#. Install `kubectl <https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/>`__ and make sure it is configured to access minikube.

#. Install `Argo CD CLI <https://argo-cd.readthedocs.io/en/stable/cli_installation/#mac>`__.

#. Install `Helm 3 <https://helm.sh/docs/intro/install/>`__.

#. Install `Vault <https://learn.hashicorp.com/tutorials/vault/getting-started-install>`__.

#. Clone the `Phalanx repository <https://github.com/lsst-sqre/phalanx.git>`__.

Open Phalanx's ``installer/`` directory:

.. code-block:: sh

  cd installer

Install the Python dependencies (using a virtual environment is ideal):

.. code-block:: sh

  pip install -r requirements.txt

Lastly, set the environment variables for Vault access:

.. code-block:: sh

   export VAULT_ADDR="https://vault.lsst.codes"
   export VAULT_TOKEN="<read key for minikube>"

The Vault read key for minikube is accessible from the ``vault_keys_json`` item in the LSST IT/RSP-Vault 1Password Vault.
The key itself is under the ``k8s_operator/minikube.lsst.codes`` → ``read`` → ``id`` field.
If you do not have Vault access, ask SQuaRE for the minikube Vault read key.
See also :doc:`../arch/secrets`.

Enable essential services
-------------------------

Edit the `minikube environment <https://github.com/lsst-sqre/phalanx/blob/master/science-platform/values-minikube.yaml>`__ file and change the field ``enabled`` to enable or disable each service.

IMPORTANT: ``ingress-nginx`` must be **disabled** since we are already using the minikube addon to deploy the NGINX Ingress Controller.

In addition to your own service, we recommend enabling at least ``vault-secrets-operator`` (to retrieve secrets from Vault) and  ``gafaelfawr`` (for authentication).

Commit and push ``values-minikube.yaml`` to your Phalanx development branch so that the installer can pick up your changes.


Run the installer
------------------

Finally, run the installer for the minikube environment.


.. code-block:: sh

  ./install.sh minikube $VAULT_TOKEN


Access the Argo CD UI
=====================

Add the following line to ``/etc/hosts``.

.. code-block:: sh

  127.0.0.1 minikube.lsst.codes

On a new terminal, use ``minikube tunnel`` to route traffic from the host to the services in minikube.

.. code-block:: sh

  minikube tunnel

Access the Argo CD UI on ``http://minikube.lsst.codes/argo-cd``.
The minikube Argo CD admin password can be retrieved from Vault.

.. code-block:: sh

  VAULT_PATH_PREFIX=`yq -r .vault_path_prefix ../science-platform/values-minikube.yaml`
  vault kv get --field=argocd.admin.plaintext_password $VAULT_PATH_PREFIX/installer

With Argo CD you can sync your service (see :doc:`sync-argo-cd`).
