.. px-app:: cachemachine

#########################################
cachemachine — JupyterLab image prepuller
#########################################

The Docker images used for lab pods run by the Notebook Aspect are quite large, since they contain the full Rubin Observatory software stack.
If the image is not already cached on a Kubernetes node, starting a lab pod can take as long as five minutes and may exceed the timeout allowed by JupyterHub.

Cachemachine is an image prepulling service designed to avoid this problem by ensuring every node in the Science Platform Kubernetes cluster has the most frequently used lab images cached.
It is also responsible for reporting the available images to :doc:`Nublado <../nublado2/index>`, used to generate the menu of images when the user creates a new lab pod.

.. jinja:: cachemachine
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::

   bootstrap
   pruning
   updating-recommended
   gar
   values
