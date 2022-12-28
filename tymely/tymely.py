#!/usr/bin/env python3
"""tymely fetches HTTP-date over HTTPS and sets the system time."""

import argparse
import datetime
import os
import random
import subprocess  # nosec B404,S404
import sys
import shutil
import requests
import certifi
import yaml

__version__ = "0.1.0"


def arguments():
    """
    Parse command line arguments using argparse module and return the parsed
    arguments.
    """
    parser = argparse.ArgumentParser(
        description="tymely fetches HTTP-date over HTTPS and sets the system time",
        epilog="version: " + __version__,
    )
    parser.add_argument(
        "-c", "--config", help="specifies a CONFiguration file", type=str
    )
    parser.add_argument(
        "-t",
        "--test",
        help="don't set the system time, just print the date",
        action="store_true",
    )

    return parser.parse_args()


def config(args):
    """
    Read and parse the configuration file specified in the command line arguments.
    Return the configuration as a dictionary.
    """
    try:
        if args.config:
            if not os.path.isfile(args.config):
                print(args.config, "can't be found.")
                sys.exit(1)
            else:
                with open(args.config, "r", encoding="utf-8") as args_file:
                    conf = yaml.safe_load(args_file)
        else:
            conf = {"verbose": 0}

        if conf.get("verbose", 0):
            print("Verbose mode enabled", file=sys.stdout)
            print("Configuration file:", args.config, file=sys.stdout)
            print(conf, file=sys.stdout)
    except KeyError as exception_string:
        print("Exception:", str(exception_string), file=sys.stderr)
        sys.exit(1)
    except UnboundLocalError as exception_string:
        print("Exception:", str(exception_string), file=sys.stderr)
        sys.exit(1)
    return conf


def get_site_and_agent(conf):
    """
    Choose a site and user agent string from the configuration dictionary.
    Return the site URL and user agent string.
    """
    user_agent = None

    if conf.get("sites"):
        url = conf.get("sites", False)
        url = random.SystemRandom().choice(url)
    else:
        url = "duckduckgo.com"

    tymely_agent = "tymely/" + __version__
    user_agent = conf.get("user_agents", tymely_agent)
    if user_agent != tymely_agent:
        user_agent = random.SystemRandom().choice(conf["user_agents"])

    if conf.get("verbose", 0):
        print("URL:", url, file=sys.stdout)
        print("User agent:", user_agent, file=sys.stdout)

    return url, user_agent


def main():
    """
    Main function that fetches the current date over HTTPS, sets the system time
    if not in test mode, and prints the date if in test mode.
    """
    args = arguments()
    conf = config(args)
    url, user_agent = get_site_and_agent(conf)

    try:
        response = requests.head(
            "https://" + url,
            headers={"User-Agent": user_agent},
            verify=certifi.where(),
            allow_redirects=True,
            timeout=1.0,
        )

        if conf.get("verbose", 0):
            print("Response headers:", response.headers, file=sys.stdout)
    except requests.exceptions.ConnectionError:
        print("Connection failed to", url, file=sys.stderr)
        sys.exit(1)

    try:
        if response.status_code != 200:
            print("Response code", response.status_code, "from", url, file=sys.stderr)
            sys.exit(1)

        date_str = response.headers["Date"]

        datetime.datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT").timestamp()

        if args.test:
            print(f"{date_str} from {url} returned but not set", file=sys.stdout)
        else:
            date_cmd = shutil.which("date")
            subprocess.run(
                [date_cmd, "-s", date_str],
                shell=False,  # nosec B603
                check=True,
            )
    except UnboundLocalError as exception_string:
        print("Exception:", str(exception_string), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
