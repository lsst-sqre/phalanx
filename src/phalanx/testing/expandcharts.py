"""Expand Helm charts for testing.

Discover the list of supported environments, find all charts that have changed
relative to main, and then expand those charts into directories for each
chart and environment pair and a values.yaml file for that environment.

This is a workaround for limitations in the helm/chart-testing tool, which
doesn't understand multi-environment patterns.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from git import DiffIndex, Repo

if TYPE_CHECKING:
    from typing import List, Sequence


def get_changed_charts() -> List[str]:
    """Get a list of charts that have changed relative to main."""
    repo = Repo(str(Path.cwd()))

    charts = []
    for path in (Path.cwd() / "applications").iterdir():
        if (path / "Chart.yaml").exists():
            diff = repo.head.commit.diff("origin/main", paths=[str(path)])
            for change_type in DiffIndex.change_type:
                if any(diff.iter_change_type(change_type)):  # type: ignore
                    print("Found changed chart", path.name)
                    charts.append(path.name)
                    break

    return charts


def get_environments() -> List[str]:
    """Get the list of supported environments."""
    science_platform_path = Path.cwd() / "environments"

    environments = []
    for path in science_platform_path.iterdir():
        name = path.name
        if not name.startswith("values-"):
            continue
        environment = name[len("values-") : -len(".yaml")]
        print("Found environment", environment)
        environments.append(environment)

    return environments


def expand_chart(chart: str, environments: Sequence[str]) -> None:
    """Expand charts from applications into applications-expanded."""
    chart_path = Path.cwd() / "applications" / chart
    expanded_path = Path.cwd() / "applications-expanded"
    expanded_path.mkdir(exist_ok=True)

    if (chart_path / "values.yaml").exists():
        print("Copying simple chart", chart)
        shutil.copytree(chart_path, expanded_path / chart)
    else:
        for environment in environments:
            values_path = chart_path / f"values-{environment}.yaml"
            if not values_path.exists():
                continue
            print("Expanding chart", chart, "for environment", environment)
            chart_expanded_path = expanded_path / f"{chart}-{environment}"
            shutil.copytree(chart_path, chart_expanded_path)
            shutil.copyfile(values_path, chart_expanded_path / "values.yaml")


def main() -> None:
    expanded_path = Path.cwd() / "applications-expanded"
    if expanded_path.exists():
        shutil.rmtree(expanded_path)
    expanded_path.mkdir()

    charts = get_changed_charts()
    environments = get_environments()
    for chart in charts:
        expand_chart(chart, environments)
