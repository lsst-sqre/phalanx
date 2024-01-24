"""Service for manipulating Phalanx applications."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import jinja2
import yaml

from ..exceptions import ApplicationExistsError
from ..models.environments import Environment
from ..models.helm import HelmStarter
from ..storage.config import ConfigStorage
from ..storage.helm import HelmStorage

__all__ = ["ApplicationService"]


class ApplicationService:
    """Service for manipulating Phalanx applications.

    Parameters
    ----------
    path
        Root path to the Phalanx directory structure.
    config_storage
        Storage object for the Phalanx configuration.
    helm_storage
        Interface to Helm actions.
    """

    def __init__(
        self,
        path: Path,
        config_storage: ConfigStorage,
        helm_storage: HelmStorage,
    ) -> None:
        self._path = path
        self._config = config_storage
        self._helm = helm_storage
        self._templates = jinja2.Environment(
            loader=jinja2.PackageLoader("phalanx", "data"),
            undefined=jinja2.StrictUndefined,
            autoescape=jinja2.select_autoescape(disabled_extensions=["jinja"]),
        )

    def add_helm_repositories(
        self, applications: Iterable[str] | None = None, *, quiet: bool = False
    ) -> bool:
        """Add all Helm repositories used by any application to Helm's cache.

        To perform other Helm operations, such as downloading third-party
        charts in order to run :command:`helm lint`, all third-party Helm
        chart repositories have to be added to Helm's cache. This does that
        for every application in the Phalanx configuration.

        Consistent names for the Helm repositories are used so that this
        command can be run repeatedly.

        Parameters
        ----------
        applications
            If given, only add Helm repositories required by these
            applications.
        quiet
            Whether to suppress Helm's standard output.

        Returns
        -------
        bool
            Whether any Helm repositories were added. If there were none, the
            caller should not call :command:`helm update`, because it fails
            if there are no repositories.
        """
        if applications:
            repo_urls = set()
            for application in applications:
                urls = self._config.get_dependency_repositories(application)
                repo_urls.update(urls)
        else:
            repo_urls = self._config.get_all_dependency_repositories()
        for url in sorted(repo_urls):
            self._helm.repo_add(url, quiet=quiet)
        return bool(repo_urls)

    def create(
        self, name: str, starter: HelmStarter, description: str
    ) -> None:
        """Create configuration for a new application.

        Parameters
        ----------
        name
            Name of the application.
        starter
            Name of the Helm starter to use as the template for the
            application.
        description
            Short description of the application.

        Raises
        ------
        ApplicationExistsError
            Raised if the application being created already exists.
        """
        path = self._config.get_application_chart_path(name)
        if path.exists():
            raise ApplicationExistsError(name)
        self._helm.create(name, starter)

        # Unfortunately, Helm completely ignores the Chart.yaml in a starter
        # so far as I can tell, so we have to load the starter Chart.yaml
        # ourselves and replace the generated Chart.yaml with it, but
        # preserving the substitutions that Helm does make.
        starter_path = self._config.get_starter_path(starter)
        chart = yaml.safe_load((starter_path / "Chart.yaml").read_text())
        helm_chart = yaml.safe_load((path / "Chart.yaml").read_text())
        chart["name"] = helm_chart["name"]
        chart["description"] = description
        if "sources" in chart:
            chart["sources"] = [
                s.replace("<CHARTNAME>", name) for s in chart["sources"]
            ]
        with (path / "Chart.yaml").open("w") as fh:
            yaml.dump(chart, fh)

        # Add the environment configuration.
        self._create_application_template(name)

        # Add the documentation.
        self._create_application_docs(name, description)

    def lint(self, app_names: list[str], env_name: str | None) -> bool:
        """Lint an application with Helm.

        Registers any required Helm repositories, refreshes them, downloads
        dependencies, and runs :command:`helm lint` on the application chart,
        configured for the given environment.

        Parameters
        ----------
        app_names
            Names of the applications to lint.
        env_name
            Name of the environment. If not given, lint all environments for
            which this application has a configuration.

        Returns
        -------
        bool
            Whether linting passed.
        """
        if self.add_helm_repositories(app_names):
            self._helm.repo_update()
        environments: dict[str, Environment] = {}
        if env_name:
            environments[env_name] = self._config.load_environment(env_name)
        success = True
        for app_name in app_names:
            self._helm.dependency_update(app_name)
            if env_name:
                app_envs = [env_name]
            else:
                app_envs = self._config.get_application_environments(app_name)
            for env in app_envs:
                if env not in environments:
                    environments[env] = self._config.load_environment(env)
                environment = environments[env]
                values = self._build_injected_values(app_name, environment)
                success &= self._helm.lint_application(app_name, env, values)
        return success

    def lint_all(self, *, only_changes_from_branch: str | None = None) -> bool:
        """Lint all applications with Helm.

        Registers any required Helm repositories, refreshes them, downloads
        dependencies, and runs :command:`helm lint` on every combination of
        application chart and configured environment.

        Parameters
        ----------
        only_changes_from_branch
            If given, only lint application and environment pairs that may
            have been affected by Git changes relative to the given branch.
            In other words, assume all application chart configurations
            identical to the given branch are uninteresting, and only lint the
            ones that have changed.

        Returns
        -------
        bool
            Whether linting passed.
        """
        if only_changes_from_branch:
            branch = only_changes_from_branch
            to_lint = self._config.get_modified_applications(branch)
        else:
            to_lint = self._config.list_application_environments()
        if self.add_helm_repositories(to_lint.keys()):
            self._helm.repo_update()
        environments: dict[str, Environment] = {}
        success = True
        for app_name, app_envs in sorted(to_lint.items()):
            if not app_envs:
                continue
            self._helm.dependency_update(app_name, quiet=True)
            for env_name in app_envs:
                if env_name in environments:
                    environment = environments[env_name]
                else:
                    environment = self._config.load_environment(env_name)
                    environments[env_name] = environment
                values = self._build_injected_values(app_name, environment)
                success &= self._helm.lint_application(
                    app_name, env_name, values
                )
        return success

    def template(self, app_name: str, env_name: str) -> str:
        """Expand the templates of an application chart.

        Run :command:`helm template` for an application chart, passing in the
        appropriate parameters for that environment.

        Parameters
        ----------
        app_name
            Name of the application.
        env_name
            Name of the environment. If not given, lint all environments for
            which this application has a configuration.

        Returns
        -------
        str
            Output from :command:`helm template`.

        Raises
        ------
        HelmFailedError
            Raised if Helm fails.
        """
        if self.add_helm_repositories([app_name], quiet=True):
            self._helm.repo_update(quiet=True)
        self._helm.dependency_update(app_name, quiet=True)
        environment = self._config.load_environment(env_name)
        values = self._build_injected_values(app_name, environment)
        return self._helm.template_application(app_name, env_name, values)

    def _build_injected_values(
        self, application: str, environment: Environment
    ) -> dict[str, str]:
        """Construct extra injected Helm values.

        To simulate the chart as it will be configured by Argo CD, we have to
        add the values that are injected via the Argo CD application.

        Parameters
        ----------
        application
            Name of the application.
        environment
            Environment whose globals should be injected.

        Returns
        -------
        dict of str
            Dictionary of Helm settings to their (string) values.

        Notes
        -----
        This is a bit of a hack, since it hard-codes the injected values
        rather than reading them out of the ``Application`` object definition.
        It therefore must be updated every time we inject a new type of value
        into charts.

        All globals that would be injected into any chart are injected here,
        even if this chart doesn't use them. That should be harmless, although
        it doesn't exactly simulate what Argo CD does.
        """
        enabled_apps = [a.name for a in environment.all_applications()]
        values = {
            "global.enabledServices": "@" + "@".join(enabled_apps),
            "global.host": environment.fqdn,
            "global.baseUrl": f"https://{environment.fqdn}",
            "global.vaultSecretsPath": environment.vault_path_prefix,
        }
        if environment.gcp:
            values["global.gcpProjectId"] = environment.gcp.project_id
            values["global.gcpRegion"] = environment.gcp.region
        if environment.butler_repository_index:
            butler_index = environment.butler_repository_index
            values["global.butlerRepositoryIndex"] = butler_index

        # vault-secrets-operator gets the Vault host injected into it. Use the
        # existence of its subchart configuration tree as a cue to inject the
        # same thing here.
        if application == "vault-secrets-operator":
            key = "vault-secrets-operator.vault.address"
            values[key] = str(environment.vault_url)

        if environment.control_system:
            extras = {
                "appNamespace": environment.control_system.app_namespace,
                "imageTag": environment.control_system.image_tag,
                "siteTag": environment.control_system.site_tag,
                "topicName": environment.control_system.topic_name,
                "kafkaBrokerAddress": (
                    environment.control_system.kafka_broker_address
                ),
                "kafkaTopicReplicationFactor": (
                    str(
                        environment.control_system.kafka_topic_replication_factor
                    )
                ),
                "schemaRegistryUrl": (
                    environment.control_system.schema_registry_url
                ),
                "s3EndpointUrl": environment.control_system.s3_endpoint_url,
            }
            values.update(
                {
                    f"global.controlSystem.{k}": v
                    for k, v in extras.items()
                    if v is not None
                }
            )

        return values

    def _create_application_template(self, name: str) -> None:
        """Add the ``Application`` template and environment values setting.

        Parameters
        ----------
        name
            Name of the new application.
        """
        # Change the quote characters so that we aren't fighting with Helm
        # templating, which also uses {{ and }}.
        overlay = self._templates.overlay(
            variable_start_string="[[", variable_end_string="]]"
        )
        template = overlay.get_template("application-template.yaml.jinja")
        application = template.render({"name": name})
        self._config.write_application_template(name, application)
        setting = f"# -- Enable the {name} application\n{name}: false"
        self._config.add_application_setting(name, setting)

    def _create_application_docs(self, name: str, description: str) -> None:
        """Add the documentation for a new application.

        This does not add the new documentation to the index page for all
        applications since it doesn't know what category to which to add it.
        This will cause a documentation build failure until the user does this
        manually. This may be fixed later if the Phalanx models learn about
        categorization.

        Parameters
        ----------
        name
            Name of the new application.
        description
            Short description of the new application.

        Raises
        ------
        ApplicationExistsError
            Raised if the application being created already exists.
        """
        docs_path = self._path / "docs" / "applications" / name
        if docs_path.exists():
            raise ApplicationExistsError(name)
        docs_path.mkdir()
        template = self._templates.get_template("application-docs.rst.jinja")
        docs = template.render({"name": name, "description": description})
        (docs_path / "index.rst").write_text(docs)
        template = self._templates.get_template("application-values.md.jinja")
        values = template.render({"name": name})
        (docs_path / "values.md").write_text(values)
