#!/usr/bin/env python3

import argparse
import certifi
import datetime
import os
import random
import ssl
import sys
import urllib3
import yaml


def defaults():
    global __minimal__, __url__, __version__

    __minimal__ = "{'verbose': 0}"
    __url__ = "duckduckgo.com"
    __version__ = "0.0.1"


def arguments():
    global args

    parser = argparse.ArgumentParser(
        description="tymely fetches HTTP-date over HTTPS and sets the system time",
        epilog="version: " + __version__,
    )
    parser.add_argument(
        "-c", "--config", help="specifies a configuration file", type=str
    )
    parser.add_argument(
        "-t",
        "--test",
        help="don't set the system time, just print the date",
        action="store_true",
    )

    args = parser.parse_args()


def config():
    global conf

    try:
        if args.config and os.path.isfile(args.config):
            with open(args.config, "r") as f:
                conf = yaml.safe_load(f)
                conf_file = args.config
        else:
            conf = yaml.safe_load(__minimal__)
            conf_file = "None"

        if conf.get("verbose", 0):
            print("Verbose mode enabled", file=sys.stdout)
            print("Configuration file:", conf_file, file=sys.stdout)
            print(conf, file=sys.stdout)

    except Exception as e:
        print("Exception:", str(e), file=sys.stderr)
        raise
        sys.exit(1)

    return conf


def sites():
    global url

    try:
        system_random = random.SystemRandom()
        url = conf.get("sites", False)
        if url:
            url = system_random.choice(conf["sites"])
        else:
            url = __url__

    except Exception as e:
        print("Exception:", str(e), file=sys.stderr)
        raise
        sys.exit(1)

    if conf.get("verbose", 0):
        print("URL:", url, file=sys.stdout)

    return url


def user_agents():
    global user_agent

    try:
        system_random = random.SystemRandom()

        try:
            tymely_version = __version__
            tymely_agent = "tymely/" + tymely_version

            user_agent = conf.get("user_agents", tymely_agent)
            if user_agent != tymely_agent:
                user_agent = system_random.choice(conf["user_agents"])

        except Exception as e:
            print("Exception:", str(e), file=sys.stderr)
            raise
            sys.exit(1)

    except Exception as e:
        print("Exception:", str(e), file=sys.stderr)
        raise
        sys.exit(1)

    if conf.get("verbose", 0):
        print("User agent:", user_agent, file=sys.stdout)

    return user_agent


def connection():
    global response

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
        response = https.request(
            "HEAD",
            "https://" + url,
            headers={"User-Agent": user_agent},
        )

        if conf.get("verbose", 0):
            print("Response headers:", response.headers, file=sys.stdout)
            print("Verify_mode:", tls_cont.verify_mode)
            print("TLS context options:", tls_cont.options)
            print(tls_cont.get_ciphers())

    except urllib3.exceptions.NewConnectionError:
        print("Connection failed to", url, file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print("Exception:", str(e), file=sys.stderr)
        raise
        sys.exit(1)

    return response


def http_date():
    try:
        if response.status != 200:
            print("Response code", response.status, "from", url, file=sys.stderr)
            sys.exit(1)

        date_str = response.headers["Date"]

        try:
            datetime.datetime.strptime(
                date_str, "%a, %d %b %Y %H:%M:%S GMT"
            ).timestamp()

        except Exception as e:
            print("Exception:", str(e), file=sys.stderr)
            raise
            sys.exit(1)

        if args.test:
            print(date_str + " returned but not set", file=sys.stdout)
        else:
            print(date_str, file=sys.stdout)
            os.system('date -s "%s"' % date_str)  # noqa

    except Exception as e:
        print("Exception:", str(e), file=sys.stderr)
        raise
        sys.exit(1)


if __name__ == "__main__":
    defaults()
    arguments()
    config()
    sites()
    user_agents()
    connection()
    http_date()
