"""Parse the arguments, read the configuration file and fetch the backup
from the pfSense firewall
"""

import argparse
import re
from os import environ, path, scandir, stat, remove
from datetime import datetime as dt
from urllib.parse import urlparse

import urllib3
from yaml import safe_load
from schema import Schema, SchemaError, And, Or, Optional, Use
from prometheus_client import Gauge, CollectorRegistry, write_to_textfile

import pfbackup

__version__ = "0.2.4"

DEFAULT_CONFIGURATION_FILE = path.join(
    environ["HOME"], ".config", "pfsense-backup", "config.yml"
)

SCHEMA = Schema(
    {
        "pfsense": Schema(
            {
                Optional("url", default="https://pfsense"): And(
                    str, lambda s: len(s) > 0
                ),
                Optional("user", default="admin"): And(str, lambda s: len(s) > 0),
                "password": And(str, lambda s: len(s) > 0),
                Optional("ssl_verify", default=True): Or(
                    bool, And(str, lambda s: len(s) > 0)
                ),
            },
        ),
        Optional(
            "output", default={"directory": ".", "name": "pfsense-%Y%m%d%H%M.xml"}
        ): Schema(
            {
                Optional("directory"): And(str, lambda s: len(s) > 0),
                Optional("name", default="pfsense-%Y%m%d%H%M.xml"): And(
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
        prog="pfsense-backup",
        description=f"A tool to fetch backups from the pfSense firewall (v{ __version__ })",
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


def fetch_backup(pfsense_config: dict, out_file: str):
    """Fetch the backup from the firewall

    Parameters
    ----------
    pfsense_config : dict
        pfSense configuration
    out_file : str
        Path to the output file
    """
    pf_sense = pfbackup.pfSense(
        pfsense_config["url"],
        pfsense_config["user"],
        pfsense_config["password"],
        pfsense_config["ssl_verify"],
    )

    config = pf_sense.get_config()

    with open(out_file, "w", encoding="utf-8") as file:
        file.write(config)


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
            if f.is_file and re.search(r"\.xml$", f.name)
        ]
    )

    while len(files) > output_config["keep"]:
        remove(path.join(output_config["directory"], files.pop(0)))


def main():
    """_summary_

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

    if config["pfsense"]["ssl_verify"] is False:
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
                f"Target directory {config['output']['directory']} does not exist or is not a directory"  # pylint: disable=line-too-long
            )
        rotate = (
            path.isabs(config["output"]["directory"]) and "keep" in config["output"]
        )
        out_file = path.join(
            config["output"]["directory"], now.strftime(config["output"]["name"])
        )

    fetch_backup(config["pfsense"], out_file)

    if rotate:
        rotate_files(config["output"])

    if "metrics" in config:
        registry = CollectorRegistry()
        backup_time = Gauge(
            "pfsense_backup_timestamp_seconds",
            "Time the backup was started.",
            ["host"],
            registry=registry,
        )
        backup_size = Gauge(
            "pfsense_backup_size_bytes",
            "Size of the backup.",
            ["host"],
            registry=registry,
        )

        if not path.isdir(config["metrics"]["directory"]):
            raise ValueError(
                f"Metrics directory {config['metrics']['directory']} does not exist or is not a directory"  # pylint: disable=line-too-long
            )

        metrics_file = path.join(config["metrics"]["directory"], "pfsense-backup")
        if "suffix" in config["metrics"]:
            metrics_file += "-" + config["metrics"]["suffix"]

        metrics_file += ".prom"

        host = urlparse(config["pfsense"]["url"]).hostname
        backup_time.labels(host).set_to_current_time()
        backup_size.labels(host).set(stat(out_file).st_size)

        write_to_textfile(metrics_file, registry)
