#########
Filestore
#########

The thing we're calling ``filestore`` is not an RSP service at all.
Nor does it (generally) run in Kubernetes.

All current ``filestore`` implementations are simply implementations of
NFS that are mounted into RSP pods (both user and service) by Volume and
VolumeMount definitions.

There is nothing in the filestore that mandates NFS.  What is required
is simply something that can present some storage to user and service
pods as a POSIX filesystem.  To this point, NFS has been the most
convenient way to accomplish that, but it is certainly not fundamental
to the concept.

.. rubric:: Guides

.. toctree::

   privileged-access
