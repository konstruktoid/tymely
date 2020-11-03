#!/usr/bin/env python3
"""tymely fetches HTTP-date over HTTPS and sets the system time."""

import argparse
import datetime
import os
import random
import shutil
import ssl
import subprocess  # noqa
import sys
import certifi
import urllib3
import yaml

__minimal__ = "{'verbose': 0}"
__url__ = "duckduckgo.com"
__version__ = "0.0.1"

ARGS = None
CONF = None
EXCEPTION_STR = "Exception:"
RESPONSE = None
URL = None
USER_AGENT = None


def arguments():
    """Command line arguments and help information."""
    global ARGS

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

    ARGS = parser.parse_args()


def config():
    """Returns CONF with yaml configuration files or default values."""
    global CONF

    try:
        if ARGS.config:
            if not os.path.isfile(ARGS.config):
                print(ARGS.config, "can't be found.")
                sys.exit(1)
            else:
                with open(ARGS.config, "r") as args_file:
                    CONF = yaml.safe_load(args_file)
                    conf_file = ARGS.config
        else:
            CONF = yaml.safe_load(__minimal__)
            conf_file = "None"

        if CONF.get("verbose", 0):
            print("Verbose mode enabled", file=sys.stdout)
            print("Configuration file:", conf_file, file=sys.stdout)
            print(CONF, file=sys.stdout)

    except IOError as exception_string:
        print(EXCEPTION_STR, str(exception_string), file=sys.stderr)
        sys.exit(1)

    except KeyError as exception_string:
        print(EXCEPTION_STR, str(exception_string), file=sys.stderr)
        sys.exit(1)

    except UnboundLocalError as exception_string:
        print(EXCEPTION_STR, str(exception_string), file=sys.stderr)
        sys.exit(1)

    return CONF


def sites():
    """Get site URLs from configuration file or use default."""
    global URL

    try:
        system_random = random.SystemRandom()
        URL = CONF.get("sites", False)
        if URL:
            URL = system_random.choice(CONF["sites"])
        else:
            URL = __url__

    except UnboundLocalError as exception_string:
        print(EXCEPTION_STR, str(exception_string), file=sys.stderr)
        sys.exit(1)

    if CONF.get("verbose", 0):
        print("URL:", URL, file=sys.stdout)

    return URL


def user_agents():
    """Get user agents from configuration file or use default."""
    global USER_AGENT

    try:
        system_random = random.SystemRandom()

        try:
            tymely_version = __version__
            tymely_agent = "tymely/" + tymely_version

            USER_AGENT = CONF.get("user_agents", tymely_agent)
            if USER_AGENT != tymely_agent:
                USER_AGENT = system_random.choice(CONF["user_agents"])

        except UnboundLocalError as exception_string:
            print(EXCEPTION_STR, str(exception_string), file=sys.stderr)
            sys.exit(1)

    except UnboundLocalError as exception_string:
        print(EXCEPTION_STR, str(exception_string), file=sys.stderr)
        sys.exit(1)

    if CONF.get("verbose", 0):
        print("User agent:", USER_AGENT, file=sys.stdout)

    return USER_AGENT


def connection():
    """Configure TLS and return the response."""
    global RESPONSE

    tls_cont = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_cont.options |= ssl.OP_NO_SSLv2
    tls_cont.options |= ssl.OP_NO_SSLv3
    tls_cont.options |= ssl.OP_NO_TLSv1
    tls_cont.options |= ssl.OP_NO_TLSv1_1

    https = urllib3.PoolManager(
        ssl_context=tls_cont,
        cert_reqs="CERT_REQUIRED",
        ca_certs=certifi.where(),
        retries=False,
        timeout=1.0,
    )

    try:
        RESPONSE = https.request(
            "HEAD",
            "https://" + URL,
            headers={"User-Agent": USER_AGENT},
        )

        if CONF.get("verbose", 0):
            print("Response headers:", RESPONSE.headers, file=sys.stdout)
            print("Verify_mode:", tls_cont.verify_mode)
            print("TLS context options:", tls_cont.options)
            print(tls_cont.get_ciphers())

    except urllib3.exceptions.NewConnectionError:
        print("Connection failed to", URL, file=sys.stderr)
        sys.exit(1)

    except UnboundLocalError as exception_string:
        print(EXCEPTION_STR, str(exception_string), file=sys.stderr)
        sys.exit(1)

    return RESPONSE


def http_date():
    """Return the http-date from URL using USER_AGENT."""
    try:
        if RESPONSE.status != 200:
            print("Response code", RESPONSE.status, "from", URL, file=sys.stderr)
            sys.exit(1)

        date_str = RESPONSE.headers["Date"]

        datetime.datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT").timestamp()

        if ARGS.test:
            print(date_str + " returned but not set", file=sys.stdout)
        else:
            date_cmd = shutil.which("date")
            subprocess.run([date_cmd, "-s", date_str], shell=False, check=True)  # noqa

    except UnboundLocalError as exception_string:
        print(EXCEPTION_STR, str(exception_string), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    arguments()
    config()
    sites()
    user_agents()
    connection()
    http_date()
