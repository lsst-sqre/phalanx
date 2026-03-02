.. px-app:: octavius

##############################################################
octavius — Object classification tool for postage stamp images
##############################################################

This application has a non-embargoed data version running at
the University of Sussex.

https://xcs-host.phys.sussex.ac.uk/xcs_portal/


This application is a multi-band object classification tool
which will primarily be used for analysing SL and galaxy clusters in
LSST embargoed data. This service provides 3 pods:

- The first is the frontend or UI which is a react-app-rewired application
   provides stateful tools and simple user authentication to access rubin
   images (via the users own auth) for classification purposes.
- Theres is an API layer which parses inputs from the UI back to the mongodb
   for storing user classifications, interactions, comments and allowing
   addition of new surveys/classification sets.
- There's a mongodb backend for providing the initial catalog of objects, as
   as well as storing all types of classifications and user current browser
   state outside of cookies.

Please contact the XCS Research Group @ University of Sussex for more information.

.. jinja:: octavius
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values