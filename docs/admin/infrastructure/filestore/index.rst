#########
Filestore
#########

Filestore is not an RSP application, nor does it (generally) run in Kubernetes.
All current filestore implementations are simply implementations of NFS that are mounted into RSP Pods_ (both JupyterLab user Pods_ and application Pods_) by ``Volume`` and ``VolumeMount`` definitions.

.. note::

   There is nothing in the filestore that mandates NFS.
   What is required is simply something that can present some storage to user and application Pods_ as a POSIX filesystem.
   To this point, NFS has been the most convenient way to accomplish that, but it is certainly not fundamental to the concept.

.. toctree::
   :caption: Guides
   :titlesonly:

   privileged-access
