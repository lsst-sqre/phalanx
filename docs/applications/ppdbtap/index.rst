.. px-app:: ppdbtap

###################################################
ppdbtap — TAP service for the PPDB BigQuery backend
###################################################

This TAP service provides access to the Prompt Products Database (PPDB) data stored in Google BigQuery.
It uses the cadc-tap Helm chart with the BigQuery backend configuration.

.. jinja:: ppdbtap
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::

   values
