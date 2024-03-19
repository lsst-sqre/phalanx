##########################
Values injected by Argo CD
##########################

The behavior of a Helm chart is customized by _values_, which are settings injected from either files or command-line flags when Helm is invoked to create Kubernetes resources.
For Phalanx applications, those values come from three sources, configured in the Argo CD ``Application`` resource for the application.
Sources later on this list override values from earlier sources.

#. The :file:`values.yaml` file for the application.
#. The :file:`values-{environment}.yaml` file for that application and the current environment.
#. Values injected by Argo CD directly from the ``Application`` resource.

The ``Application`` resources are found in :file:`environments/templates/applications`.
Unlike the :file:`values.yaml` file for the application, they have access to environment-wide configuration set by the :file:`environments/values-{environment}.yaml` files.

This page describes that third group of values injected by Argo CD.

Always-injected values
======================

Injected values must be explicitly listed in the ``Application`` resource template for that application, and therefore a given application may not have any injected values.
However, by convention and via :command:`phalanx application create`, Phalanx applications always get the following injected values, all of which provide information about the Phalanx environment in which the application is being deployed.

``global.host``
    The default hostname used by this Phalanx environment.
    This corresponds to the hostname in the public URLs for the services in this environment.

``global.baseUrl``
    The base URL for applications deployed in this Phalanx environment.
    This always uses the ``https://`` schema.

``global.vaultSecretsPath``
    The base path in Vault for secrets for this environment.
    The Vault path for a secret for a given application can be formed by appending :samp:`/{application}` to this value.
    The pull secret for the environment, if there is one, will be this value with ``/pull-secret`` appended.

.. _dev-injected-optional:

Optional injected values
========================

The following additional values are not normally injected by the default ``Application`` template but can be added if needed by adding a new entry to the ``spec.source.helm.parameters`` key of the ``Application`` resource template.

``global.butlerRepositoryIndex``
    The URI for the Butler index for this environment, used by services that connect directly to the Butler database without using the Butler server.

``global.butlerServerRepositories``
    A mapping from Butler repository labels to URIs that is used by applications that talk to the Butler server.
    Since this is a complex data structure, it has to be injected as a base64-encoded value to prevent Helm from misinterpreting it:

    .. code-block:: yaml

       - name: "global.butlerServerRepositories"
         value: {{ .Values.butlerServerRepositories | toJson | b64enc }}

    When using this value in an application template, you will then need to undo the base64 encoding.
    For example, here is a fragment of a template used to set an environment variable to the JSON encoding of this mapping:

    .. code-block:: yaml

       - name: "DAF_BUTLER_REPOSITORIES"
         value: {{ .Values.global.butlerServerRepositories | b64dec | quote }}

``global.controlSystem.*``
    Settings that begin with ``global.controlSystem`` are specific to the telescope control system applications and correspond to the ``controlSystem.*`` settings in :file:`environments/values.yaml`.
    These should only be used for the telescope control system, the details of which are outside of the scope of this documentation.

If you use any of these optional injected values, do not forget to document them in the :file:`values.yaml` file for your application.

Adding new injected values
==========================

In theory, any value that can be determined only from information present in the :file:`environments/values.yaml` and :file:`environments/values-{environment}.yaml` files can be injected into an application.
However, if you add any values not present in the above list, you will have to change the source code for the :command:`phalanx` command-line tool to inject the same values when linting and templating charts.

Use the following process when injecting new values:

#. Make sure that you need to inject a new value.
   Each new injected value adds additional complexity that Phalanx developers have to keep track of.
   Only use injected values for information that is global to a given environment **and** is needed by multiple applications.

#. Ensure that all the information that you are injecting is available from the environment configuration defined in :file:`environments/values.yaml`.
   If it is not, you may have to extend the environment configuration by updating the model in :file:`src/phalanx/models/environments.py`.
   New settings should be defined in `~phalanx.models.environments.EnvironmentBaseConfig`.
   You will also need to regenerate the JSON schema for environments with :command:`phalanx environment schema`, replacing :file:`docs/extras/schemas/environment.json`.

#. Add the new injected values to the ``Application`` resource template for the appropriate applications.
   Injected values go through multiple layers of parsing and interpretation, so only string values will work reliably.
   If you need to inject more complex information, you will have to JSON-encode and base64-encode the values and decode them again in the application template.

#. Add the new injected values to the ``_build_injected_values`` method of `~phalanx.services.application.ApplicationService`.
   This will make them available for :command:`phalanx application lint` and :command:`phalanx application template`.
   If you did any encoding of the value in the ``Application`` resource templates, you will need to do the same encoding here.

#. Document the injected values in the :file:`values.yaml` files of every application that uses them.

#. Use the injected values in the templates of the applications that need them.
   Often this will involve setting an environment variable for the application deployment to the injected value.

#. Document the new injected values in this file, under :ref:`dev-injected-optional`.
