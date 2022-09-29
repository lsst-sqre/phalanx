####
mobu
####

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/mobu <https://github.com/lsst-sqre/phalanx/tree/master/services/mobu>`__
   * - Type
     - Helm_
   * - Namespace
     - ``mobu``

.. rubric:: Overview

mobu is the continuous integration testing framework for the Rubin Science Platform.
It runs some number of "monkeys" that simulate a random user of the Science Platform.
Those monkeys are organized into "flocks" that share a single configuration across all of the monkeys.
Failures are reported to Slack using a Slack incoming webhook.

mobu is maintained on `GitHub <https://github.com/lsst-sqre/mobu>`__.

.. rubric:: Guides

.. toctree::

   configuring
