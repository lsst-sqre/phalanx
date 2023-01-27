.. px-app-notes:: tap

##########################
TAP architecture and notes
##########################

The ``tap`` application consists of the TAP Java web application, a PostgreSQL database used to track user job submissions (the backing store for the UWS_ protocol), and (on development deployments) a mock version of Qserv.

.. diagrams:: notebook-tap.py

.. diagrams:: portal-tap.py
