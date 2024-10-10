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

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        specifies a configuration file
  -t, --test            don't set the system time, just print the date

version: 0.1.0
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
  - "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"
  - "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"
  - "Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Mobile Safari/537.36"
  - "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
  - "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"
  - "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.6; rv:92.0) Gecko/20100101 Firefox/92.0"
  - "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
  - "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
  - "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
  - "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1"
```

The above configuration will make `tymely` randomly choose a site and user agent
from the lists presented in the file, and verbosely return any information.

```sh
$ ./tymely.py -c tymely.yaml -t
Verbose mode enabled
Configuration file: tymely.yaml
{'verbose': 1, 'sites': ['cloudflare.com', 'duckduckgo.com', 'github.com', 'proton.me', 'stackoverflow.com', 'xkcd.com'], 'user_agents': ['Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Mobile Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.6; rv:92.0) Gecko/20100101 Firefox/92.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1']}
URL: duckduckgo.com
User agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1
Response headers: {'Server': 'nginx', 'Date': 'Thu, 10 Oct 2024 19:05:43 GMT', 'Content-Type': 'text/html; charset=UTF-8', 'Content-Length': '11191', 'Connection': 'keep-alive', 'Vary': 'Accept-Encoding', 'ETag': '"6706e8f7-2bb7"', 'Content-Encoding': 'gzip', 'Strict-Transport-Security': 'max-age=31536000', 'Permissions-Policy': 'interest-cohort=()', 'Content-Security-Policy': "default-src 'none' ; connect-src  https://duckduckgo.com https://*.duckduckgo.com https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/ https://spreadprivacy.com ; manifest-src  https://duckduckgo.com https://*.duckduckgo.com https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/ https://spreadprivacy.com ; media-src  https://duckduckgo.com https://*.duckduckgo.com https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/ https://spreadprivacy.com ; script-src blob:  https://duckduckgo.com https://*.duckduckgo.com https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/ https://spreadprivacy.com 'unsafe-inline' 'unsafe-eval' ; font-src data:  https://duckduckgo.com https://*.duckduckgo.com https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/ https://spreadprivacy.com ; img-src data:  https://duckduckgo.com https://*.duckduckgo.com https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/ https://spreadprivacy.com ; style-src  https://duckduckgo.com https://*.duckduckgo.com https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/ https://spreadprivacy.com 'unsafe-inline' ; object-src 'none' ; worker-src blob: ; child-src blob:  https://duckduckgo.com https://*.duckduckgo.com https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/ https://spreadprivacy.com ; frame-src blob:  https://duckduckgo.com https://*.duckduckgo.com https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/ https://spreadprivacy.com ; form-action  https://duckduckgo.com https://*.duckduckgo.com https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/ https://spreadprivacy.com ; frame-ancestors 'self' https://html.duckduckgo.com; base-uri 'self' ; block-all-mixed-content ;", 'X-Frame-Options': 'SAMEORIGIN', 'X-XSS-Protection': '1;mode=block', 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'origin', 'Expect-CT': 'max-age=0', 'Expires': 'Thu, 10 Oct 2024 19:05:42 GMT', 'Cache-Control': 'no-cache'}
Thu, 10 Oct 2024 19:05:43 GMT from duckduckgo.com returned but not set
```

### Related documentation

<https://tools.ietf.org/html/rfc7231#section-7.1.1.2>

<https://www.whonix.org/wiki/Time_Attacks>

<https://gitlab.com/madaidan/secure-time-sync>

<https://github.com/ioerror/tlsdate>
