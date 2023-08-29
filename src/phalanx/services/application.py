"""Service for manipulating Phalanx applications."""

from __future__ import annotations

from pathlib import Path

import jinja2
import yaml

from ..exceptions import ApplicationExistsError
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

    def create_application(
        self, name: str, starter: str, description: str
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

        # Replace the description in the chart with the provided one.
        chart = yaml.safe_load((path / "Chart.yaml").read_text())
        chart["description"] = description
        with (path / "Chart.yaml").open("w") as fh:
            yaml.dump(chart, fh)

        # Add the environment configuration.
        self._create_application_template(name)

        # Add the documentation.
        self._create_application_docs(name, description)

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
