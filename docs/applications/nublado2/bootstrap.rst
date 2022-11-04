.. px-app-bootstrap:: nublado2

#####################
Bootstrapping Nublado
#####################

Nublado and :px-app:`moneypenny` need to know where the NFS server that provides user home space is.
Nublado also requires other persistent storage space.
Ensure the correct definitions are in place in their configuration.

Telescope and Site deployments
==============================

For Telescope and Site deployments that require instrument control, make sure you have any Multus network definitions you need in the ``values-<environment>.yaml``.
This will look something like:

.. code-block:: yaml

    singleuser:
      extraAnnotations:
        k8s.v1.cni.cncf.io/networks: "kube-system/macvlan-conf"
      initContainers:
        - name: "multus-init"
          image: "lsstit/ddsnet4u:latest"
          securityContext:
            privileged: true

It's possible to list multiple Multus network names separated by commas in the annotation string.
Experimentally, it appears that the interfaces will appear in the order specified.

The ``initContainers`` entry should be inserted verbatim.
It creates a privileged container that bridges user pods to the specified networks before releasing control to the user's lab.
