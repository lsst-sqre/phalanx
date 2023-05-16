import argparse
import pathlib

import yaml

APPS_DIR = "applications"

DIR_MAP = {"csc": "csc", "collector": "csc_collector"}


def shared_chart(appdir: pathlib.Path, shared_dir: str) -> bool:
    """Determine if app directory has templates dir as link.

    Parameters
    ----------
    appdir: `pathlib.Path`
        The application directory to check.
    shared_dir: `str`
        The shared directory to make sure the link resolves to.

    Returns
    -------
    `bool`: True if the link resolves to the requested shared dir.
    """
    try:
        chart_dir = appdir / "charts" / shared_dir
        return (
            chart_dir.is_symlink() and chart_dir.resolve().name == shared_dir
        )
    except OSError:
        return False


def main(opts: argparse.Namespace) -> None:
    print(
        f"Updating {opts.app_type} apps Helm chart "
        f"to version {opts.chart_version}"
    )

    apps = pathlib.PosixPath(APPS_DIR)
    dirlist = list(apps.iterdir())
    for appdir in dirlist:
        if not shared_chart(appdir, DIR_MAP[opts.app_type]):
            continue

        chart = appdir / "Chart.yaml"

        with chart.open() as ifile:
            values = yaml.safe_load(ifile)

        dependencies = values["dependencies"]
        for dependency in dependencies:
            if dependency["name"] == DIR_MAP[opts.app_type]:
                dependency["version"] = opts.chart_version

        # print(appdir, values)

        with chart.open("w") as ofile:
            yaml.dump(values, ofile, sort_keys=False)


def run() -> None:
    description = [
        "Update version for apps using the csc or shared Helm chart"
    ]
    parser = argparse.ArgumentParser(
        description=" ".join(description),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "app_type",
        choices=list(DIR_MAP.keys()),
        help="Specify the application type to set the chart version for.",
    )
    parser.add_argument(
        "chart_version", help="The version of the Helm chart to set."
    )
    args = parser.parse_args()
    main(args)
