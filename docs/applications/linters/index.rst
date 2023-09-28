.. px-app:: linters

####################################
linters — Automated chechking of DNS
####################################

Linters provides a way to automatically and repeatedly check things in ops, such as if DNS entries
are pointing to IP addresses that we are using, or are they dangling.  We use the route53 API
as well as the Google API to cross-reference these configuration details and alert on things that
don't look right.

.. jinja:: linters
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
