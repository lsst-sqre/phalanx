#######
Nublado
#######

Although Nublado is itself a well-behaved Kubernetes application, in
many environments it requires particular attention to the Kubernetes
configuration settings in order to display the menu of available images
correctly and to keep the prepuller from running continuously.

Prepulled Images
================

The fundamental problem is that the Kubernetes setting
``nodeStatusMaxImages`` is set to 50 by default.  The only way to
retrieve a list of which images are present on a node is to query the
node, and look through its ``status.images`` information.

In general, our implementation relies on the supposition that prepulled
images are the freshest, and that, eventually, people will stop using
old images, and when the disk pressure garbage collection threshold is
exceeded, the images that have not been used in the longest time will be
purged.  When the ephemeral storage is sized such that there is not room
for very many ``sciplat-lab`` images (but enough space to hold at least
the full set that should be prepulled), and when ``sciplat-lab`` is the
most common image found on nodes, this generally just works with no
further attention: the menu stays populated with the current images, and
since they are prepulled, they spawn quickly when selected.  Disk
pressure cleans up outdated images, and everything works as it should.

However, if the node has a large amount of ephemeral storage, and/or
there is much non-Lab application use on the node, this can cause a
problem for the prepuller: it is entirely possible for images that are
indeed present on the node to not be in the first fifty images in the
image list, and therefore not to be found when the prepuller determines
which images need prepulling.

This has two consequences: first, the prepuller will be constantly
scheduling images as it prepulls the ones it wants, because even though
the image is already resident on the node, the prepuller doesn't know
that.  Second, these images, because the prepuller thinks they are not
resident on all nodes, will not be visible in the JupyterHub spawner
menu, although they will be available from the dropdown list.

Fortunately there is a simple fix, provided one has access to kubelet
configuration.  The configuration is described in
https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/
and includes the ``nodeStatusMaxImages`` setting.  The default value of
50 should either be increased to something large enough that it's
implausible that that many images would fit into ephemeral storage, or
set to ``-1`` to remove the cap entirely.  While disabling the cap could
in theory make node status extremely large, in practice, with the size
of nodes we've been running RSP instances on, we have had at most
hundreds, rather than thousands or millions, of container images on any
given node.


