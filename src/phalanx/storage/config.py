"""Parsing and analysis of Phalanx configuration."""

from __future__ import annotations

import re
from collections import defaultdict
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self
from urllib.parse import urlparse

import yaml
from git import Diff
from git.repo import Repo
from pydantic import ValidationError

from ..constants import HELM_DOCLINK_ANNOTATION
from ..exceptions import (
    ApplicationExistsError,
    GitRemoteError,
    InvalidApplicationConfigError,
    InvalidSecretConfigError,
    UnknownEnvironmentError,
)
from ..models.applications import (
    Application,
    ApplicationConfig,
    ApplicationInstance,
    DocLink,
    Project,
)
from ..models.environments import (
    ArgoCDDetails,
    ArgoCDRBAC,
    Environment,
    EnvironmentConfig,
    EnvironmentDetails,
    GafaelfawrDetails,
    GafaelfawrScope,
    IdentityProvider,
    PhalanxConfig,
)
from ..models.helm import HelmStarter
from ..models.secrets import ConditionalSecretConfig, Secret

__all__ = ["ConfigStorage"]


def _merge_overrides(
    base: dict[str, Any], overrides: dict[str, Any]
) -> dict[str, Any]:
    """Merge values settings with overrides.

    Parameters
    ----------
    base
        Base settings.
    overrides
        Overrides that should take precedence.

    Returns
    -------
    dict
        Merged dictionary.
    """
    new = base.copy()
    for key, value in overrides.items():
        if key in new:
            if isinstance(new[key], dict) and isinstance(value, dict):
                new[key] = _merge_overrides(new[key], value)
            else:
                new[key] = value
        else:
            new[key] = value
    return new


@dataclass
class _ApplicationChange:
    """Holds the analysis of a diff affecting a Phalanx application chart."""

    application: str
    """Name of the affected application."""

    path: str
    """Path of changed file relative to the top of the chart."""

    is_delete: bool
    """Whether this change is a file deletion."""

    @classmethod
    def from_diff(cls, diff: Diff) -> Self:
        """Create a change based on a Git diff.

        Parameters
        ----------
        diff
            One Git diff affecting a single file.

        Returns
        -------
        _ApplicationChange
            Corresponding parsed change.

        Raises
        ------
        ValueError
            Raised if this is not a change to an application chart.
        """
        full_path = diff.b_path or diff.a_path
        if not full_path:
            raise ValueError("Not a change to an application")
        m = re.match("applications/([^/]+)/(.+)", full_path)
        if not m:
            raise ValueError("Not a change to an application")
        return cls(
            application=m.group(1),
            path=m.group(2),
            is_delete=diff.change_type == "D",
        )

    @property
    def affects_all_envs(self) -> bool:
        """Whether this change may affect any environment."""
        if self.path in ("Chart.yaml", "values.yaml"):
            return True
        return self.path.startswith(("crds/", "templates/"))


class ConfigStorage:
    """Analyze Phalanx configuration and convert it to models.

    Parameters
    ----------
    path
        Path to the root of the Phalanx configuration.
    """

    def __init__(self, path: Path) -> None:
        self._path = path

    def add_application_setting(self, application: str, setting: str) -> None:
        """Add the setting for a new application to the environments chart.

        Adds a block for a new application to :file:`values.yaml` in the
        environments directory in the correct alphabetical location.

        Parameters
        ----------
        application
            Name of the new application.
        setting
            Setting block for the new application. Indentation will be added.
        """
        key = re.compile(r" +(?P<application>[^:]+): +")
        setting = "\n".join("  " + line for line in setting.split("\n"))

        # Add the new setting in correct alphabetical order. This is the sort
        # of operation that Python is very bad at, so this code is rather
        # tedious and complicated.
        #
        # First, copy the old file to the new file until the start of the
        # applications block is found. Then, capture each block of blank lines
        # and comments leading up to the setting for an application. If that
        # application sorts after the one we're adding, add our setting before
        # that block to the new file, and then add that block and the rest of
        # the file. If it sorts after, add the block to the new file and keep
        # searching. If we fall off the end without finding a setting that
        # sorts alphabetically after ours, add our setting to the end of the
        # file.
        #
        # This makes a lot of assumptions about the structure of the
        # values.yaml file that ideally we wouldn't make, but the alternative
        # requires doing something complicated with ruamel.yaml and inserting
        # a new setting in a specific order. There are no great solutions
        # here if one cares about retaining the alphabetical ordering.
        path = self._path / "environments" / "values.yaml"
        path_new = path.parent / "values.yaml.new"
        old_values = path.read_text().split("\n")
        old_values.reverse()
        with path_new.open("w") as new:
            while old_values:
                line = old_values.pop()
                new.write(line + "\n")
                if line.startswith("applications:"):
                    break
            found = False
            first = True
            block = ""
            while old_values:
                line = old_values.pop()
                m = key.match(line)
                if not m:
                    block += line + "\n"
                    continue
                if m.group("application") == application:
                    raise ApplicationExistsError(application)
                if m.group("application") > application:
                    if first:
                        new.write(setting + "\n\n")
                    else:
                        new.write("\n" + setting + "\n")
                    found = True
                    block += line + "\n"
                    break
                new.write(block + line + "\n")
                block = ""
                first = False
            if block:
                new.write(block)
            if found:
                old_values.reverse()
                new.write("\n".join(old_values))
            else:
                new.write(setting + "\n")
        path_new.rename(path)

    def get_all_dependency_repositories(self) -> set[str]:
        """List the URLs of all referenced third-party Helm repositories.

        Returns
        -------
        set of str
            URLs of third-party Helm repositories referenced by some
            application chart.
        """
        repo_urls = set()
        for app_path in (self._path / "applications").iterdir():
            chart_path = app_path / "Chart.yaml"
            if not chart_path.exists():
                continue
            urls = self.get_dependency_repositories(app_path.name)
            repo_urls.update(urls)
        return repo_urls

    def get_application_chart_path(self, application: str) -> Path:
        """Determine the path to an application Helm chart.

        The application and path may not exist, since this function is also
        used to generate the path to newly-created applications.

        Parameters
        ----------
        application
            Name of the application.

        Returns
        -------
        pathlib.Path
            Path to that application's chart.
        """
        return self._path / "applications" / application

    def get_application_environments(self, application: str) -> list[str]:
        """List all environments for which an application is configured.

        This is based entirely on the presence of
        :file:`values-{environment}.yaml` configuration files in the
        application directory, not on which environments enable the
        application. This is intentional since this is used to constrain which
        environments are linted, and we want to lint applications in
        environments that aren't currently enabled to ensure they've not
        bitrotted.

        Parameters
        ----------
        application
            Name of the application.

        Returns
        -------
        list of str
            List of environment names for which that application is
            configured.
        """
        path = self.get_application_chart_path(application)
        return [
            v.stem.removeprefix("values-")
            for v in sorted(path.glob("values-*.yaml"))
        ]

    def get_dependency_repositories(self, application: str) -> set[str]:
        """Return URLs for dependency Helm repositories for this application.

        Parameters
        ----------
        application
            Name of the application.

        Returns
        -------
        set of str
            URLs of Helm repositories used by dependencies of this
            application's chart.
        """
        path = self.get_application_chart_path(application) / "Chart.yaml"
        chart = yaml.safe_load(path.read_text())
        repo_urls = set()
        for dependency in chart.get("dependencies", []):
            if "repository" in dependency:
                repository = dependency["repository"]
                if not repository.startswith("file:"):
                    repo_urls.add(repository)
        return repo_urls

    def get_environment_chart_path(self) -> Path:
        """Determine the path to the top-level environment chart.

        Returns
        -------
        pathlib.Path
            Path to the top-level environment chart.
        """
        return self._path / "environments"

    def get_git_branch(self) -> str:
        """Get the Git branch of the current repository.

        Returns
        -------
        str
            Branch name.
        """
        return Repo(str(self._path)).active_branch.name

    def get_git_url(self) -> str:
        """Get the Git URL of the current repository.

        Assumes that the current repository is a cloned Git repository with a
        remote named ``origin`` and returns the URL of that origin,
        transformed to an ``https`` URL if necessary. This is used to get the
        URL of the repository for configuring Argo CD during installation of
        an environment.

        Returns
        -------
        str
            URL to the Git repository of the current config tree, suitable
            for Argo CD.

        Raises
        ------
        GitRemoteError
            Raised if the ``origin`` remote does not exist or if its URL is
            not in a recognized format.
        """
        repo = Repo(str(self._path))
        try:
            origin = repo.remote("origin")
        except ValueError as e:
            msg = 'Current repository has no remote named "origin"'
            raise GitRemoteError(msg) from e
        if not origin.url:
            raise GitRemoteError('Remote "origin" has no URL')

        # If the URL is not an https URL, accept a few forms of github.com
        # URLs that can be converted into one.
        parsed_url = urlparse(origin.url)
        if parsed_url.scheme == "ssh" and parsed_url.hostname == "github.com":
            return parsed_url._replace(
                scheme="https", netloc=parsed_url.hostname
            ).geturl()
        elif parsed_url.scheme == "https":
            return origin.url
        elif parsed_url.scheme == "":
            match = re.match(r"git@github\.com:([^:/]+/[^:/]+)$", origin.url)
            if match:
                return "https://github.com/" + match.group(1)

        # If we fell through, we were unable to parse the URL.
        msg = (
            "Cannot determine Argo CD Git URL from origin URL of"
            f' "{origin.url}"'
        )
        raise GitRemoteError(msg)

    def get_modified_applications(self, branch: str) -> dict[str, list[str]]:
        """Get all modified application and environment pairs.

        Application and environment pairs that have been deleted do not count
        as modified, since we don't want to attempt to lint deleted
        configurations.

        Parameters
        ----------
        branch
            Git branch against which to compare to see what modifications
            have been made.

        Returns
        -------
        dict of list of str
            Dictionary of all modified applications to the list of
            environments configured for that application that may have been
            affected.
        """
        result: defaultdict[str, list[str]] = defaultdict(list)
        repo = Repo(str(self._path))
        diffs = repo.head.commit.diff(branch, paths=["applications"], R=True)
        for diff in diffs:
            try:
                change = _ApplicationChange.from_diff(diff)
            except ValueError:
                continue
            if change.affects_all_envs:
                envs = self.get_application_environments(change.application)
                if envs:
                    result[change.application] = envs
            elif not change.is_delete:
                if m := re.match("values-([^.]+).yaml$", change.path):
                    result[change.application].append(m.group(1))
        return result

    def get_starter_path(self, starter: HelmStarter) -> Path:
        """Determine the path to a Helm starter template.

        Parameters
        ----------
        starter
            Name of the Helm starter template.

        Returns
        -------
        pathlib.Path
            Path to that Helm starter template.
        """
        return self._path / "starters" / starter.value

    def list_application_environments(self) -> dict[str, list[str]]:
        """List all available applications and their environments.

        Returns
        -------
        dict of list of str
            Dictionary of all applications to lists of environments for which
            that application has a configuration.
        """
        return {
            a: self.get_application_environments(a)
            for a in self.list_applications()
        }

    def list_applications(self) -> list[str]:
        """List all available applications.

        Returns
        -------
        list of str
            Names of all applications.
        """
        path = self._path / "applications"
        return sorted(v.name for v in path.iterdir() if v.is_dir())

    def list_environments(self) -> list[str]:
        """List all of the available environments.

        Returns
        -------
        list of str
            Names of all available environments.
        """
        path = self._path / "environments"
        return [
            v.stem.removeprefix("values-")
            for v in sorted(path.glob("values-*.yaml"))
        ]

    def list_project_applications(self, project_name: str) -> list[str]:
        """List all project applications.

        Parameters
        ----------
        project_name
            The project to collect applications for.

        Returns
        -------
        list of str
            Names of all project applications.
        """
        path = (
            self._path
            / "environments"
            / "templates"
            / "applications"
            / project_name
        )
        return [v.stem for v in sorted(path.glob("*.yaml"))]

    def load_environment(self, environment_name: str) -> Environment:
        """Load the configuration of a Phalanx environment from disk.

        Parameters
        ----------
        environment_name
            Name of the environment.

        Returns
        -------
        Environment
            Environment configuration.

        Raises
        ------
        UnknownEnvironmentError
            Raised if the named environment has no configuration.
        """
        config = self.load_environment_config(environment_name)
        applications = [
            self._load_application_config(a)
            for a in config.enabled_applications
        ]
        instances = {
            a.name: self._resolve_application(a, environment_name)
            for a in applications
        }
        return Environment(
            **config.model_dump(exclude={"applications"}),
            applications=instances,
        )

    def load_environment_config(
        self, environment_name: str
    ) -> EnvironmentConfig:
        """Load the top-level configuration for a Phalanx environment.

        Unlike `load_environment`, this only loads the top-level environment
        configuration and its list of enabled applications. It does not load
        the configuration for all of the applications themselves.

        Parameters
        ----------
        environment_name
            Name of the environent.

        Returns
        -------
        Environment
            Loaded environment.

        Raises
        ------
        InvalidEnvironmentConfigError
            Raised if the configuration for an environment is invalid.
        UnknownEnvironmentError
            Raised if the named environment has no configuration.
        """
        values_base = self._path / "environments"
        with (values_base / "values.yaml").open() as fh:
            values = yaml.safe_load(fh)
        env_values_path = values_base / f"values-{environment_name}.yaml"
        if not env_values_path.exists():
            raise UnknownEnvironmentError(environment_name)
        with env_values_path.open() as fh:
            env_values = yaml.safe_load(fh)
            values = _merge_overrides(values, env_values)
        return EnvironmentConfig.model_validate(values)

    def load_phalanx_config(self) -> PhalanxConfig:
        """Load the full Phalanx configuration.

        Used primarily for generating docuemntation.

        Returns
        -------
        PhalanxConfig
            Phalanx configuration for all environments.

        Raises
        ------
        InvalidApplicationConfigError
            Raised if the namespace for the application could not be found.
        InvalidEnvironmentConfigError
            Raised if the configuration for an environment is invalid.
        """
        environments = [
            self.load_environment_config(e) for e in self.list_environments()
        ]

        # Load the configurations of all applications.
        all_applications: set[str] = set()
        enabled_for: defaultdict[str, list[str]] = defaultdict(list)
        for environment in environments:
            for name in environment.enabled_applications:
                enabled_for[name].append(environment.name)
            all_applications.update(environment.applications.keys())
        applications = {}
        for name in all_applications:
            application_config = self._load_application_config(name)
            application = Application(
                active_environments=enabled_for[name],
                **application_config.model_dump(),
            )
            applications[name] = application

        # Build the environment details, which augments the environment config
        # with some information from Argo CD and Gafaelfawr configuration for
        # that environment.
        environment_details = []
        for environment in environments:
            name = environment.name
            if environment.applications.get("gafaelfawr", False):
                gafaelfawr = self._resolve_application(
                    applications["gafaelfawr"], name
                )
            else:
                gafaelfawr = None
            details = self._build_environment_details(
                environment,
                [applications[a] for a in environment.enabled_applications],
                self._resolve_application(applications["argocd"], name),
                gafaelfawr,
            )
            environment_details.append(details)

        # Return the resulting configuration.
        return PhalanxConfig(
            environments=environment_details,
            applications=sorted(applications.values(), key=lambda a: a.name),
        )

    def check_telescope_revisions(self, environment: str) -> None:
        """Check on control system applications for app specific revisions.

        Note: The summit configuration for the love application will have app
              specific revisions, but those must be 0 for a new cycle build.

        Parameters
        ----------
        environment
            The name of the environment to check for the revisions.
        """
        for app in self.list_project_applications("telescope"):
            if app in ["argo-workflows", "obsenv-management", "ocps-uws-job"]:
                continue
            app_config = self._load_application_config(app)
            env_config = app_config.environment_values[environment]
            app_list: list[str] = []
            for key, item_config in env_config.items():
                if key.startswith("love"):
                    self._check_love_revisions(
                        item_config, app_list, key, environment
                    )
                if key in ["uws-api-server"]:
                    continue
                if "image" not in item_config:
                    continue
                if "revision" in item_config["image"]:
                    app_list.append(key)

            if app_list:
                print(f"{app} has application specific revisions:")
                for item in set(app_list):
                    print(f"- {item}")

    def update_shared_chart_version(self, chart: str, version: str) -> None:
        """Update the version of a shared chart across all applications.

        Parameters
        ----------
        chart
            The name of the chart for the version change.
        version
            The chart version to update.
        """
        for app in self.list_applications():
            app_config = self._load_application_config(app)
            is_modified = False
            try:
                for item in app_config.chart["dependencies"]:
                    if item["name"] == chart:
                        item["version"] = version
                        is_modified = True
            except KeyError:
                pass
            if is_modified:
                chart_path = self._path / "applications" / app / "Chart.yaml"
                with chart_path.open("w") as fh:
                    yaml.safe_dump(app_config.chart, fh, sort_keys=False)

    def write_application_template(
        self, name: str, project: Project, template: str
    ) -> None:
        """Write the Argo CD application template for a new application.

        Parameters
        ----------
        name
            Name of the application.
        project
            Project of the application.
        template
            Contents of the Argo CD application and namespace Helm template
            for the new application.

        Raises
        ------
        ApplicationExistsError
            Raised if the application being created already exists.
        """
        path = (
            self._path
            / "environments"
            / "templates"
            / "applications"
            / project.value
            / f"{name}.yaml"
        )
        if path.exists():
            raise ApplicationExistsError(name)
        path.write_text(template)

    def _build_environment_details(
        self,
        config: EnvironmentConfig,
        applications: list[Application],
        argocd: ApplicationInstance,
        gafaelfawr: ApplicationInstance | None,
    ) -> EnvironmentDetails:
        """Construct the details of an environment.

        This is the environment configuration enhanced with some configuration
        details from the Argo CD and Gafaelfawr applications.

        Parameters
        ----------
        config
            Configuration for the environment.
        applications
            All enabled applications for that environment.
        argocd
            Argo CD application configuration.
        gafaelfawr
            Gafaelfawr application configuration, if Gafaelfawr is enabled for
            this environment.

        Returns
        -------
        EnvironmentDetails
            Fleshed-out details for that environment.

        Raises
        ------
        InvalidApplicationConfigError
            Raised if the Gafaelfawr or Argo CD configuration is invalid.
        """
        return EnvironmentDetails(
            **config.model_dump(exclude={"applications"}),
            applications=applications,
            gafaelfawr=self._build_gafaelfawr_details(config, gafaelfawr),
            argocd=self._build_argocd_details(argocd),
        )

    def _build_argocd_details(
        self, argocd: ApplicationInstance
    ) -> ArgoCDDetails:
        """Construct the details of an Argo CD configuration.

        Parameters
        ----------
        argocd
            Argo CD application configuration.

        Returns
        -------
        ArgoCDDetails
            Fleshed-out details for that environment.

        Raises
        ------
        InvalidApplicationConfigError
            Raised if the Gafaelfawr or Argo CD configuration is invalid.
        """
        try:
            config = argocd.values["argo-cd"]["configs"]["cm"]
        except KeyError:
            return ArgoCDDetails(provider=IdentityProvider.NONE)

        # Public URL of Argo CD.
        url = config.get("url")

        # Argo CD identity provider.
        provider = IdentityProvider.NONE
        provider_hostname = None
        if "oidc.config" in config:
            provider = IdentityProvider.OIDC
            oidc_config = yaml.safe_load(config["oidc.config"])
            with suppress(KeyError):
                provider_hostname = urlparse(oidc_config["issuer"]).hostname
        elif "dex.config" in config:
            dex_config = yaml.safe_load(config["dex.config"])
            with suppress(KeyError):
                connector = dex_config["connectors"][0]
                if connector["name"] == "GitHub":
                    provider = IdentityProvider.GITHUB
                elif connector["name"] == "Google":
                    provider = IdentityProvider.GOOGLE
                    provider_hostname = connector["config"]["hostedDomains"][0]

        # Argo CD role-based access control configuration.
        argocd_rbac = None
        with suppress(KeyError):
            rbac_config = argocd.values["argo-cd"]["configs"]["rbac"]
            argocd_rbac = ArgoCDRBAC.from_csv(rbac_config["policy.csv"])

        # Return the results.
        return ArgoCDDetails(
            provider=provider,
            provider_hostname=provider_hostname,
            rbac=argocd_rbac,
            url=url,
        )

    def _build_gafaelfawr_details(
        self,
        config: EnvironmentConfig,
        gafaelfawr: ApplicationInstance | None,
    ) -> GafaelfawrDetails:
        """Construct the details of a Gafaelfawr configuration.

        Parameters
        ----------
        config
            Configuration for the environment.
        gafaelfawr
            Gafaelfawr application configuration, if Gafaelfawr is enabled for
            this environment.

        Returns
        -------
        GafaelfawrDetails
            Fleshed-out details for that environment.

        Raises
        ------
        InvalidApplicationConfigError
            Raised if the Gafaelfawr or Argo CD configuration is invalid.
        """
        if not gafaelfawr:
            return GafaelfawrDetails(provider=IdentityProvider.NONE)

        # Determine the upstream identity provider.
        provider_hostname = None
        comanage_hostname = None
        if gafaelfawr:
            if gafaelfawr.values["config"]["cilogon"]["clientId"]:
                provider = IdentityProvider.CILOGON
                cilogon_config = gafaelfawr.values["config"]["cilogon"]
                if cilogon_config["enrollmentUrl"]:
                    url = cilogon_config["enrollmentUrl"]
                    comanage_hostname = urlparse(url).hostname
            elif gafaelfawr.values["config"]["github"]["clientId"]:
                provider = IdentityProvider.GITHUB
            elif gafaelfawr.values["config"]["oidc"]["clientId"]:
                provider = IdentityProvider.OIDC
                url = gafaelfawr.values["config"]["oidc"]["loginUrl"]
                provider_hostname = urlparse(url).hostname
            else:
                raise InvalidApplicationConfigError(
                    "gafaelfawr",
                    "Cannot determine identity provider",
                    environment=config.name,
                )
        else:
            provider = IdentityProvider.NONE

        # Gafaelfawr scopes. Restructure the data to let Pydantic do most of
        # the parsing.
        gafaelfawr_scopes = []
        try:
            group_mapping = gafaelfawr.values["config"]["groupMapping"]
            for scope, groups in group_mapping.items():
                raw = {"scope": scope, "groups": groups}
                gafaelfawr_scope = GafaelfawrScope.model_validate(raw)
                gafaelfawr_scopes.append(gafaelfawr_scope)
        except KeyError as e:
            raise InvalidApplicationConfigError(
                "gafaelfawr", "No config.groupMapping", environment=config.name
            ) from e
        except ValidationError as e:
            raise InvalidApplicationConfigError(
                "gafaelfawr",
                "Invalid config.groupMapping",
                environment=config.name,
            ) from e

        # Return the results.
        return GafaelfawrDetails(
            provider=provider,
            provider_hostname=provider_hostname,
            comanage_hostname=comanage_hostname,
            scopes=sorted(gafaelfawr_scopes, key=lambda s: s.scope),
        )

    def _check_love_revisions(self, c: dict, al: list, k: str, e: str) -> None:
        """Check revisions on LOVE apps.

        Summit apps are set to revision 0 on cycle upgrades, so always have a
        value. The test stands do not have a revision set normally.
        """
        if k == "love-manager":
            blocks = c["manager"]["producers"]
            blocks.append(c["manager"]["frontend"])
        elif k == "love-nginx":
            blocks = list(c["initContainers"].values())
        else:
            if "image" not in c:
                return
            blocks = [c]

        for block in blocks:
            if "revision" in block["image"]:
                if e == "summit":
                    if block["image"]["revision"]:
                        al.append(k)
                else:
                    al.append(k)

    def _find_application_namespace(self, application: str) -> str:
        """Determine what namespace an application will be deployed into.

        This information is present in the Argo CD ``Application`` resource,
        which by convention in Phalanx is named :file:`{app}-application.yaml`
        in the :file:`environments/templates` directory.

        Parameters
        ----------
        application
            Name of the application.

        Returns
        -------
        str
            Namespace into which the application will be deployed.

        Raises
        ------
        InvalidApplicationConfigError
            Raised if the namespace for the application could not be found.
        """
        template_path = self._find_application_resource_path(application)
        template = template_path.read_text()

        # Helm templates are unfortunately not valid YAML, so do this the hard
        # way with a regular expression.
        pattern = (
            r"destination:\n"
            r"\s+namespace:\s*\"?(?P<namespace>[a-zA-Z][\w-]+)\"?\s"
        )
        match = re.search(pattern, template, flags=re.MULTILINE | re.DOTALL)
        if not match:
            msg = f"Namespace not found in {template_path!s}"
            raise InvalidApplicationConfigError(application, msg)
        return match.group("namespace")

    def _find_application_project(self, application: str) -> Project:
        """Determine what Argo CD project an application belongs to.

        Parameters
        ----------
        application
            Name of the application.

        Returns
        -------
        str
            Argo CD project to which the application belongs.

        Raises
        ------
        InvalidApplicationConfigError
            Raised if the project for the application could not be found or
            was set to an invalid value.

        Notes
        -----
        All Argo CD ``Application`` resources are put into subdirectories by
        their Argo CD project, and a Phalanx test ensures that this matches
        the project referenced inside the Helm resource template, so we can
        use the file system path to find this information.

        """
        template_path = self._find_application_resource_path(application)
        return Project(template_path.parent.name)

    def _find_application_resource_path(self, application: str) -> Path:
        """Find the path to the ``Application`` resource for an application.

        Parameters
        ----------
        application
            Name of the application.

        Returns
        -------
        Path
            Path to the ``Application`` resource template.

        Raises
        ------
        InvalidApplicationConfigError
            Raised if the project for the application could not be found or
            was set to an invalid value.
        """
        template_path = (
            self.get_environment_chart_path() / "templates" / "applications"
        )
        application_path = None
        for subdir in template_path.iterdir():
            candidate = subdir / f"{application}.yaml"
            if candidate.exists():
                application_path = candidate
                break
        if not application_path:
            msg = "Cannot find Application resource"
            raise InvalidApplicationConfigError(application, msg)
        return application_path

    def _is_condition_satisfied(
        self, instance: ApplicationInstance, condition: str | None
    ) -> bool:
        """Evaluate a secret condition on an application instance.

        This is a convenience wrapper around
        `ApplicationInstance.is_is_values_setting_true` that also treats a
        `None` condition parameter as true.

        Parameters
        ----------
        instance
            Application instance for a specific environment.
        condition
            Condition, or `None` if there is no condition.

        Returns
        -------
        bool
            `True` if condition is `None` or corresponds to a values setting
            whose value is true, `False` otherwise.
        """
        if not condition:
            return True
        else:
            return instance.is_values_setting_true(condition)

    def _load_application_config(self, name: str) -> ApplicationConfig:
        """Load the configuration for an application from disk.

        Parameters
        ----------
        name
            Name of the application.

        Returns
        -------
        ApplicationConfig
            Application configuration.
        """
        base_path = self._path / "applications" / name
        with (base_path / "Chart.yaml").open("r") as fh:
            chart = yaml.safe_load(fh)

        # Load main values file.
        values_path = base_path / "values.yaml"
        if values_path.exists():
            with values_path.open("r") as fh:
                values = yaml.safe_load(fh) or {}
        else:
            values = {}

        # Load environment-specific values files.
        environment_values = {}
        for path in base_path.glob("values-*.yaml"):
            env_name = path.stem.removeprefix("values-")
            with path.open("r") as fh:
                env_values = yaml.safe_load(fh)
                if env_values:
                    environment_values[env_name] = env_values

        # Load the secrets configuration.
        secrets_path = base_path / "secrets.yaml"
        secrets = {}
        if secrets_path.exists():
            with secrets_path.open("r") as fh:
                raw_secrets = yaml.safe_load(fh)
            secrets = {
                k: ConditionalSecretConfig.model_validate(s)
                for k, s in raw_secrets.items()
            }

        # Load the environment-specific secrets configuration.
        environment_secrets = {}
        for path in base_path.glob("secrets-*.yaml"):
            env_name = path.stem[len("secrets-") :]
            with path.open("r") as fh:
                raw_secrets = yaml.safe_load(fh)
            environment_secrets[env_name] = {
                k: ConditionalSecretConfig.model_validate(s)
                for k, s in raw_secrets.items()
            }

        # Return the resulting application.
        return ApplicationConfig(
            name=name,
            namespace=self._find_application_namespace(name),
            project=self._find_application_project(name),
            chart=chart,
            doc_links=self._parse_doclinks(chart),
            values=values,
            environment_values=environment_values,
            secrets=secrets,
            environment_secrets=environment_secrets,
        )

    def _parse_doclinks(self, chart: dict[str, Any]) -> list[DocLink]:
        """Parse documentation links from Helm chart annotations.

        We use the ``phalanx.lsst.io/docs`` annotation to store documentation
        links in :file:`Chart.yaml`. This method extracts them.

        Parameters
        ----------
        chart
            Parsed :file:`Chart.yaml` for an application's main chart.

        Returns
        -------
        list of DocLink
            Documentation links, if any.
        """
        key = HELM_DOCLINK_ANNOTATION
        if key in chart.get("annotations", {}):
            links = yaml.safe_load(chart["annotations"][key])
            return [DocLink(**link) for link in links]
        else:
            return []

    def _resolve_application(
        self, application: ApplicationConfig, environment_name: str
    ) -> ApplicationInstance:
        """Resolve an application to its environment-specific configuration.

        Parameters
        ----------
        application
            Application to resolve.
        environment_name
            Name of the environment the application should be configured for.

        Returns
        -------
        ApplicationInstance
            Resolved application.

        Raises
        ------
        InvalidSecretConfigError
            Raised if the secret configuration has conflicting rules.
        """
        # Merge values with any environment overrides.
        env_values = application.environment_values.get(environment_name, {})
        values = _merge_overrides(application.values, env_values)

        # Create an initial application instance without secrets so that we
        # can use its class methods.
        instance = ApplicationInstance(
            name=application.name,
            environment=environment_name,
            project=application.project,
            chart=application.chart,
            values=values,
        )

        # Merge secrets with any environment secrets.
        secrets = application.secrets
        if environment_name in application.environment_secrets:
            secrets = application.secrets.copy()
            secrets.update(application.environment_secrets[environment_name])

        # Evaluate the conditions on all of the secrets. Both the top-level
        # condition and any conditions on the copy and generate rules will be
        # resolved, so that any subsequent processing based on the instance no
        # longer needs to worry about conditions.
        required_secrets = []
        for key, config in secrets.items():
            if not self._is_condition_satisfied(instance, config.condition):
                continue
            copy = config.copy_rules
            if copy:
                condition = copy.condition
                if not self._is_condition_satisfied(instance, condition):
                    copy = None
            generate = config.generate
            if generate:
                condition = generate.condition
                if not self._is_condition_satisfied(instance, condition):
                    generate = None
            if copy and generate:
                msg = "Copy and generate rules conflict"
                raise InvalidSecretConfigError(instance.name, key, msg)
            secret = Secret(
                application=application.name,
                key=key,
                description=config.description,
                copy_rules=copy,
                generate=generate,
                onepassword=config.onepassword,
                value=config.value,
            )
            required_secrets.append(secret)

        # Add the secrets to the new instance and return it.
        instance.secrets = {
            s.key: s for s in sorted(required_secrets, key=lambda s: s.key)
        }
        return instance
