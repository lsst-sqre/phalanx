#############
Image pruning
#############

If the list of cached images on nodes gets excessively long, K8s may stop updating its list of cached images.  This will manifest as the spawner options form being devoid of prepulled images.

This is a function of Kubernetes, by default, `only showing 50 images on a node <https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/>`__.  You can work around this, if you control the Kubernetes installation, with ``--node-status-max-images`` set to ``-1`` on the kubelet command line, or by setting ``nodeStatusMaxImages`` to ``-1`` in the kubelet configuration file.

Should you encounter this problem, for each node, perform the following actions:

#. Download `purge <https://github.com/lsst-sqre/imagepurger/tree/main/node-script/purge>`__
#. Run it using an account allowed to use the Docker socket (thus, probably in group ``docker``).  You may want to run it with ``-x`` first to see what it's going to do.  If you want output during the actual run, run it with ``-v``.

