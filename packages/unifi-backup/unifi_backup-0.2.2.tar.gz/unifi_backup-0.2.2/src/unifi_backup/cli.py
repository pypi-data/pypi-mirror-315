"""Parse the arguments, read the configuration file and fetch the backup
from the UniFi network application
"""

import shutil
import argparse
import re
import warnings
from os import environ, path, scandir, remove, stat
from datetime import datetime as dt
from yaml import safe_load
from schema import Schema, SchemaError, And, Or, Optional, Use

import urllib3
from pyunifi.controller import APIError, Controller
from prometheus_client import Gauge, CollectorRegistry, write_to_textfile

__version__ = "0.2.2"

DEFAULT_CONFIGURATION_FILE = path.join(
    environ["HOME"], ".config", "unifi-backup", "config.yml"
)

SCHEMA = Schema(
    {
        "controller": Schema(
            {
                Optional("host", default="unifi"): And(str, lambda s: len(s) > 0),
                Optional("port", default=8443): Use(int),
                Optional("user", default="admin"): And(str, lambda s: len(s) > 0),
                "password": And(str, lambda s: len(s) > 0),
                Optional("site", default="default"): And(str, lambda s: len(s) > 0),
                Optional("ssl_verify", default=True): Or(
                    bool, And(str, lambda s: len(s) > 0)
                ),
            },
        ),
        Optional(
            "output", default={"directory": ".", "name": "unifi-%Y%m%d%H%M.unf"}
        ): Schema(
            {
                Optional("directory"): And(str, lambda s: len(s) > 0),
                Optional("name", default="unifi-%Y%m%d%H%M.unf"): And(
                    str, lambda s: len(s) > 0
                ),
                Optional("keep"): And(Use(int), lambda x: x > 0),
            },
        ),
        Optional("metrics"): Schema(
            {
                "directory": And(str, lambda s: len(s) > 0),
                Optional("suffix"): And(str, lambda s: len(s) > 0),
            },
        ),
    }
)


def parse_arguments():
    """Parse the arguments

    Returns
    -------
    dict
        parsed arguments
    """

    parser = argparse.ArgumentParser(
        prog="unifi-backup",
        description=f"A tool to fetch backups from the UniFi network application (v{ __version__ })",
    )

    parser.add_argument(
        "-c",
        "--config",
        default=DEFAULT_CONFIGURATION_FILE,
        metavar="FILE",
        type=argparse.FileType("r"),
        help="the configuration file (default: %(default)s)",
    )

    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="the output file (default is specified in the configuration file)",
    )

    return vars(parser.parse_args())


def parse_configuration(stream):
    """Parse the configuration file

    Parameters
    ----------
    stream : io.IOBase | str
        Stream to read the configuration from.

    Returns
    -------
    dict
        Parsed and validated configuration
    """
    config = SCHEMA.validate(safe_load(stream))

    return config


def fetch_backup(controller_config: dict, out_file: str):
    """Fetch the backup from the controller

    Parameters
    ----------
    controller_config : dict
        Controller configuration
    out_file : str
        Path to the output file
    """
    controller = Controller(
        host=controller_config["host"],
        port=controller_config["port"],
        username=controller_config["user"],
        password=controller_config["password"],
        site_id=controller_config["site"],
        ssl_verify=controller_config["ssl_verify"],
    )

    # PR https://github.com/finish06/pyunifi/pull/76 fixing get_backup is not merged yet
    # controller.get_backup(target_file=out_file)
    dl_url = controller._run_command("backup", mgr="backup", params={"days": 0})[0][
        "url"
    ]
    # This is what the web UI does: controller._run_command("async-backup", mgr="backup", params={"days": 0})
    response = controller.session.get(controller.url + dl_url, stream=True)

    if response.status_code != 200:
        raise APIError(f"API backup failed: {response.status_code}")

    with open(out_file, "wb") as _backfh:
        return shutil.copyfileobj(response.raw, _backfh)


def rotate_files(output_config: dict):
    """Rotate the files

    Parameters
    ----------
    output_config : dict
        Configuration
    """
    files = sorted(
        [
            f.name
            for f in scandir(output_config["directory"])
            if f.is_file and re.search(r"\.unf$", f.name)
        ]
    )

    while len(files) > output_config["keep"]:
        remove(path.join(output_config["directory"], files.pop(0)))


def main():
    """Main

    Raises
    ------
    ValueError
        Configuration is invalid
    ValueError
        Output directory does not exist
    """
    arguments = parse_arguments()

    try:
        config = parse_configuration(arguments["config"])
    except SchemaError as ex:
        raise ValueError(
            "configuration invalid\n" + str(ex.with_traceback(None))
        ) from None

    arguments["config"].close()

    if config["controller"]["ssl_verify"] is False:
        urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)

    now = dt.now()

    # If the file was given through an argument, use that and skip the rotation
    # If not, use the configuration to construct the file name and do the rotation
    # if requested and the directory was provided as an absolute path
    if arguments["output"] is not None:
        out_file = arguments["output"]
        rotate = False
    else:
        if not path.isdir(config["output"]["directory"]):
            raise ValueError(
                f"Target directory {config['output']['directory']} does not exist or is not a directory"
            )
        rotate = (
            path.isabs(config["output"]["directory"]) and "keep" in config["output"]
        )
        out_file = path.join(
            config["output"]["directory"], dt.now().strftime(config["output"]["name"])
        )

    fetch_backup(config["controller"], out_file)

    if rotate:
        rotate_files(config["output"])

    if "metrics" in config:
        registry = CollectorRegistry()
        backup_time = Gauge(
            "unifi_backup_timestamp_seconds",
            "Time the backup was started.",
            ["host", "site"],
            registry=registry,
        )
        backup_size = Gauge(
            "unifi_backup_size_bytes",
            "Size of the backup.",
            ["host", "site"],
            registry=registry,
        )

        if not path.isdir(config["metrics"]["directory"]):
            raise ValueError(
                f"Metrics directory {config['metrics']['directory']} does not exist or is not a directory"  # pylint: disable=line-too-long
            )

        metrics_file = path.join(config["metrics"]["directory"], "unifi-backup")
        if "suffix" in config["metrics"]:
            metrics_file += "-" + config["metrics"]["suffix"]

        metrics_file += ".prom"

        backup_time.labels(
            config["controller"]["host"], config["controller"]["site"]
        ).set_to_current_time()
        backup_size.labels(
            config["controller"]["host"], config["controller"]["site"]
        ).set(stat(out_file).st_size)

        write_to_textfile(metrics_file, registry)
