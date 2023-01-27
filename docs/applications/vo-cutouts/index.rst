.. px-app:: vo-cutouts

####################################
vo-cutouts — IVOA SODA image cutouts
####################################

``vo-cutouts`` provides image cutouts via an API complying with the IVOA_ SODA_ specification.
It is returned as part of the DataLink_ record for images found via TAP searches and is used by the Portal Aspect (see :px-app:`portal`) to obtain cutouts.
It can also be used directly by any other IVOA-compatible client.

.. jinja:: vo-cutouts
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
