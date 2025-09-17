.. px-app:: butler-writer-service

##############################################################################
butler-writer-service — Proxy service for concurrent writes to a shared Butler
##############################################################################

The Butler writer service takes concurrent write requests from Prompt Processing and forwards them at a sustainable pace to the repository.

.. jinja:: butler-writer-service
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
