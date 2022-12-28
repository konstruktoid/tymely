# tymely

## T-Y-M-E-L-Y with Y because, why not

[In a timely manner ; at the right time](https://en.wiktionary.org/wiki/tymely)
and for no apparent reason inspired by
[Doom Patrol](https://www.imdb.com/title/tt11591458/).

## Description

`tymely` is a simple type [Python](https://www.python.org/) application used to
set system date and time with `date -s "%s"` using the `HTTP-date` fetched from
one or more defined websites over HTTPS.

Written as a test after a discussion about [security implications when
using NTP](https://github.com/konstruktoid/hardening/issues/80).

## System configuration

Uninstall `ntpd`, `chrony` and other applications using NTP.

In order to disable `sntp` functionality in `systemd`, run
`sudo timedatectl set-ntp 0` and verify with
`sudo systemctl status systemd-timesyncd.service`.

Use `cron` or systemd timers to execute `tymely`.

## Usage

```sh
usage: tymely.py [-h] [-c CONFIG] [-t]

tymely fetches HTTP-date over HTTPS and sets the system time

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        specifies a CONFiguration file
  -t, --test            don't set the system time, just print the date

version: 0.0.1
```

If no configuration file is used,`tymely` will use `https://duckduckgo.com`
as the site to fetch the `HTTP-date` from, use `tymely/<version>` as user agent,
and set the system date to the returned `HTTP-date`.

## Configuration file options

The configuration file should be in valid `YAML` format.

`verbose: (0|1)` show verbose information.

`sites:` a list of sites to fetch the HTTP-date header from.

`user_agents:` a list of user agents.

### Example configuration

```yaml
---
verbose: 1
sites:
  - "cloudflare.com"
  - "duckduckgo.com"
  - "github.com"
  - "proton.me"
  - "stackoverflow.com"
  - "xkcd.com"
user_agents:
  - "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
  - "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
  - "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"
  - "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.2.599 Yowser/2.5 Safari/537.36"
  - "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
  - "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
  - "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
  - "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
  - "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"
```

The above configuration will make `tymely` randomly choose a site and user agent
from the lists presented in the file, and verbosely return any information.

```sh
$ ./tymely.py -c tymely.yaml -t
Verbose mode enabled
Configuration file: tymely.yaml
{'verbose': 1, 'sites': ['cloudflare.com', 'duckduckgo.com', 'github.com', 'proton.me', 'stackoverflow.com', 'xkcd.com'], 'user_agents': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.2.599 Yowser/2.5 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0']}
URL: proton.me
User agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0
Response headers: {'date': 'Wed, 28 Dec 2022 15:38:52 GMT', 'set-cookie': 'Session-Id=Y6xjDCybqTYU-tqqBvhDmwAAABo; Domain=proton.me; Path=/; HttpOnly; Secure; Max-Age=7776000, Tag=default; Path=/; Secure; Max-Age=7776000', 'last-modified': 'Wed, 28 Dec 2022 10:24:00 GMT', 'accept-ranges': 'bytes', 'cache-control': 'max-age=0, no-cache, no-store, must-revalidate', 'expires': 'Wed, 11 Jan 1984 05:00:00 GMT', 'vary': 'Accept-Encoding', 'content-encoding': 'gzip', 'pragma': 'no-cache', 'content-length': '21937', 'content-type': 'text/html; charset=utf-8', 'content-security-policy-report-only': "default-src 'self'; media-src https://static.zdassets.com; connect-src 'self' wss: https://protonmail.zendesk.com https://ekr.zdassets.com blob: https://account.proton.me https://reports.proton.me https://*.algolia.net https://*.algolianet.com; script-src 'self' blob: 'unsafe-eval' 'unsafe-inline'  https://static.zdassets.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https:; object-src 'self' data: blob:; frame-src 'self' data: blob: https://www.youtube-nocookie.com; child-src 'self' data: blob:; report-uri https://reports.proton.me/reports/csp; frame-ancestors 'self';", 'strict-transport-security': 'max-age=31536000; includeSubDomains; preload', 'expect-ct': 'max-age=2592000, enforce, report-uri="https://reports.protonmail.com/reports/tls"', 'public-key-pins-report-only': 'pin-sha256="CT56BhOTmj5ZIPgb/xD5mH8rY3BLo/MlhP7oPyJUEDo="; report-uri="https://reports.protonmail.com/reports/tls"', 'x-frame-options': 'sameorigin', 'x-content-type-options': 'nosniff', 'x-xss-protection': '0', 'referrer-policy': 'strict-origin-when-cross-origin', 'x-permitted-cross-domain-policies': 'none', 'onion-location': 'https://protonmailrmez3lotccipshtkleegetolb73fuirgj7r4o4vfu7ozyd.onion/'}
Wed, 28 Dec 2022 15:38:52 GMT from proton.me returned but not set
```

### Related documentation

<https://tools.ietf.org/html/rfc7231#section-7.1.1.2>

<https://www.whonix.org/wiki/Time_Attacks>

<https://gitlab.com/madaidan/secure-time-sync>

<https://github.com/ioerror/tlsdate>
