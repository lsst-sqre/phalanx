.. px-app:: wobbly

##################################
wobbly — IVOA UWS database storage
##################################

Wobbly is the backing store for all Rubin-developed, Safir-based web applications that use the `IVOA UWS`_ protocol for managing jobs.
It handles job storage, retrieval, and metadata updates, including metrics reporting, for any application that needs a UWS jobs database.
For more information, see `the Safir UWS documentation <https://safir.lsst.io/user-guide/uws/index.html>`__

.. _IVOA UWS: https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html

.. jinja:: wobbly
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
