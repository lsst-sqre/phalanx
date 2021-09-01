#############
Image Pruning
#############

If the list of cached images on nodes gets excessively long (we've only seen this at NCSA, where there is lots of disk for images and the nodes have been around forever), K8s may stop updating its list of cached images.  This will manifest as the spawner options form being devoid of prepulled images.

This is a function of Kubernetes, by default, `only showing 50 images on a node<https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/>`__.  You can work around this, if you control the Kubernetes installation, with ``--node-status-max-images`` set to ``-1`` on the kubelet command line, or by setting ``nodeStatusMaxImages`` to ``-1`` in the kubelet configuration file.

Should you encounter this problem, for each node, perform the following actions:

#. ``docker image prune -f`` and ``docker builder prune -f``
#. Remove all the experimental, all but the last 15 daily, and all but the last 78 weekly images.  Remember that a lexigraphic sort will put images of a particular type in order, so a combination of ``grep``, ``sort``, ``awk``, ``tr``, ``wc``, ``xargs``, and some shell arithmetic will do the trick.  This will take a very long time, and if you're only slightly over the limit it's probably easier to just do it image-by-image by hand from the output of ``docker images``.
