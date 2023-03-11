.. px-app-bootstrap:: nublado

#####################
Bootstrapping Nublado
#####################

The JupyterLab Controller needs to know where the NFS server that provides persistent space (e.g. home directories, scratch, datasets) can be found.  Ensure the correct definitions are in place in the configuration.

Telescope and Site deployments
==============================

For Telescope and Site deployments that require instrument control, make sure you have any Multus network definitions you need in the ``values-<environment>.yaml``.
This will look something like:

.. code-block:: yaml

    singleuser:
      extraAnnotations:
        k8s.v1.cni.cncf.io/networks: "kube-system/dds"

It's possible to list multiple Multus network names separated by commas in the annotation string.
Experimentally, it appears that the interfaces will appear in the order specified.
