#############
Image pruning
#############

If the list of cached images on nodes gets excessively long, Kubernetes may stop updating its list of cached images.
The usual symptom is that the Notebook Aspect spawner menu of available images will be empty or missing expected images.

This is a limitation of the Kubernetes node API.
By default, `only 50 images on a node will be shown <https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/>`__.
You can work around this, if you control the Kubernetes installation, by adding ``--node-status-max-images=-1`` on the kubelet command line, or by setting ``nodeStatusMaxImages`` to ``-1`` in the kubelet configuration file.

If you cannot change that setting, you will need to trim the node image cache so that the total number of images is under 50.

#. Download `purge <https://github.com/lsst-sqre/imagepurger/blob/main/node-script/purge>`__.

#. Run it on each node, using an account allowed to use the Docker socket (thus, probably in group ``docker``).
   You may want to run it with ``-x`` first to see what it's going to do.
   If you want output during the actual run, run it with ``-v``.
