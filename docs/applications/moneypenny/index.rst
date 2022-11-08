.. px-app:: moneypenny

##############################
moneypenny — User provisioning
##############################

Moneypenny is responsible for provisioning new users of the Notebook Aspect of a Science Platform installation.
It is invoked by :px-app:`nublado2` whenever a user pod is spawned and decides whether provisioning is required.
If so, it does so before the lab spawn, usually by spawning a privileged pod.

A typical example of the type of provisioning it does is creating the user's home directory, with appropriate ownership and permissions, in an NFS file store.

.. jinja:: moneypenny
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
