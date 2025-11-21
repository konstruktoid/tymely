#!/usr/bin/env python3
# ruff: noqa: T201
"""tymely fetches HTTP-date over HTTPS and sets the system time."""

import argparse
import asyncio
import datetime
import secrets
import shutil
import ssl
import subprocess  # nosec B404,S404
import sys
from pathlib import Path
from typing import Any

import aiohttp
import certifi
import yaml
from aiohttp.typedefs import LooseHeaders

__version__ = "0.2.0"


def arguments() -> argparse.Namespace:
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        description="tymely fetches HTTP-date over HTTPS and sets the system time",
        epilog="version: " + __version__,
    )
    parser.add_argument(
        "-c",
        "--config",
        help="specifies a configuration file",
        type=str,
    )
    parser.add_argument(
        "-t",
        "--test",
        help="don't set the system time, just print the date",
        action="store_true",
    )
    return parser.parse_args()


def config(args: argparse.Namespace) -> dict[str, Any]:
    """Load and parse the configuration file."""
    try:
        if args.config:
            config_path = Path(args.config)
            if not config_path.is_file():
                print(args.config, "can't be found.")
                sys.exit(1)
            with config_path.open(encoding="utf-8") as args_file:
                conf: dict[str, Any] = yaml.safe_load(args_file)
        else:
            conf = {"verbose": 0}

        if conf.get("verbose", 0):
            print("Verbose mode enabled", file=sys.stdout)
            print("Configuration file:", args.config, file=sys.stdout)
            print(conf, file=sys.stdout)

    except (KeyError, UnboundLocalError) as exception_string:
        print("Exception:", str(exception_string), file=sys.stderr)
        sys.exit(1)

    return conf


def get_site_and_agent(conf: dict[str, Any]) -> tuple[str, str]:
    """Select a random site and user-agent string."""
    if conf.get("sites"):
        url: str = secrets.choice(conf["sites"])
    else:
        url = "duckduckgo.com"

    tymely_agent = "tymely/" + __version__
    user_agent_default: str = conf.get("user_agents", tymely_agent)

    if user_agent_default != tymely_agent:
        user_agent: str = secrets.choice(conf["user_agents"])
    else:
        user_agent = tymely_agent

    if conf.get("verbose", 0):
        print("URL:", url, file=sys.stdout)
        print("User agent:", user_agent, file=sys.stdout)

    return url, user_agent


async def fetch_head(
    url: str,
    user_agent: str,
    verbose: int,
) -> tuple[int, LooseHeaders]:
    """Send an request and return the status and response headers."""
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    async with aiohttp.ClientSession() as session:
        try:
            async with session.head(
                "https://" + url,
                headers={"User-Agent": user_agent},
                ssl=ssl_context,
                allow_redirects=True,
                timeout=aiohttp.ClientTimeout(total=1.0),
            ) as response:
                if verbose:
                    print("Response headers:", dict(response.headers), file=sys.stdout)

                # response.headers is a CIMultiDict (compatible with LooseHeaders)
                return response.status, response.headers

        except aiohttp.ClientError:
            print("Connection failed to", url, file=sys.stderr)
            sys.exit(1)


async def main_async() -> None:
    """Fetch current time and optionally set the system clock."""
    args: argparse.Namespace = arguments()
    conf: dict[str, Any] = config(args)
    url, user_agent = get_site_and_agent(conf)

    status, headers = await fetch_head(url, user_agent, conf.get("verbose", 0))
    status_ok = 200

    if status != status_ok:
        print("Response code", status, "from", url, file=sys.stderr)
        sys.exit(1)

    try:
        date_str = headers["Date"]  # ty: ignore

        # Validate format
        datetime.datetime.strptime(
            date_str,
            "%a, %d %b %Y %H:%M:%S GMT",
        ).astimezone().timestamp()

        # Test mode: don't change system time
        if args.test:
            print(f"{date_str} from {url} returned but not set", file=sys.stdout)
            return

        date_cmd: str | None = shutil.which("date")
        subprocess.run(  # noqa: S603, ASYNC221
            [date_cmd, "-s", date_str],
            shell=False,
            check=True,
        )

    except KeyError:
        print("No Date header returned", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError:
        sys.exit(1)


def main() -> None:
    """Entry point."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
