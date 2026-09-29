##################################
Registering with service discovery
##################################

If your application provides a new API or UI, you will probably want to register it with service discovery.
This allows all clients of your application to locate your application without having to make assumptions about hostnames and paths that may change in the future.
It also documents your application for documentation pages and dynamic indices, such as that provided by Squareone_.

Service discovery in Phalanx is provided by Repertoire_.
It is configured via the :px-app:`repertoire` Phalanx application.
Adding a new application will usually involve adding a rule to ``config.rules`` in :file:`applications/repertoire/values.yaml`.

For details on how to write a rule for your service, see the `Repertoire service rule documentation <https://repertoire.lsst.io/operations/services.html>`__.
