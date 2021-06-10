###########################
rancher-external-ip-webhook
###########################

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/rancher-external-ip-webhook <https://github.com/lsst-sqre/phalanx/tree/master/services/rancher-external-ip-webhook>`__
   * - Type
     - Helm_
   * - Namespace
     - ``rancher-external-ip-webhook``

.. rubric:: Overview

The ``rancher-external-ip-webhook`` application is a validating webhook that protects against CVE-2020-8554 in Kubernetes.
It needs to be deployed on any Kubernetes cluster where untrusted users may be able to spawn pods with control over the pod configuration.

Kubernetes allows anyone with pod creation permissions to claim an IP address via externalIP configuration.
If they do this, Kubernetes will route all traffic for that IP address to that pod, even if the IP would otherwise be routed to the Internet.
This allows a malicious pod to claim addresses like 8.8.8.8 and run a rogue DNS server, or intercept other traffic from other pods.
This application defeats this attack by adding a validating webhook that rejects any pod that specifies an external IP address.
(We use ingresses instead.)

Kubernetes provides the `validating webhook <https://github.com/kubernetes-sigs/externalip-webhook>`__, and the Rancher project provides a `Helm chart <https://github.com/rancher/externalip-webhook/tree/master/chart>`__ to install it.
The Helm chart requires ``cert-manager`` to generate a self-signed certificate (it's not entirely clear why), so we only deploy it on platforms where we're also installing ``cert-manager``.

.. rubric:: Testing

The following commands can be used to test whether this application is performing as expected:

.. code-block:: console

   $ kubectl run nginx --image nginx:latest --port 80
   pod/nginx created
   $ cat <<EOF | kubectl apply -f -
   apiVersion: v1
   kind: Service
   metadata:
     name: my-evil-service
   spec:
     selector:
       run: nginx
     type: ClusterIP
     ports:
       - name: http
         protocol: TCP
         port: 80
         targetPort: 80
     externalIPs:
       - 23.185.0.3 #cncf.io
   EOF
   Error from server (spec.externalIPs: Invalid value: "23.185.0.3" [...]

Taken from `the relevant Kubernetes issue <https://github.com/kubernetes/kubernetes/issues/97076>`__.
Adjust if the IP address of cncf.io changes.

If this does not produce an error, the validating webhook is not working.
You can then demonstrate the attack with:

.. code-block:: console

   $ kubectl run --rm -i --tty curl --image=curlimages/curl --restart=Never -- curl -I http://cncf.io

and look at the ``Server`` header in the output.
If it's nginx, the attack works (cncf.io uses Varnish).
