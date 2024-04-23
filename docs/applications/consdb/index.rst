.. px-app:: consdb

###########################################
consdb — Populate the consolidated database
###########################################

There are two parts to the consolidated database:
  - use the header information from the header service to populate the
    ``visit`` table
  - in USDF sumarise other EFD data into the ``summary`` table per visit


.. jinja:: consdb
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
