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

Use `cron` or systemd timers to manually set the date and time.

In order to disable `sntp` functionality in `systemd`:

```
sudo timedatectl set-ntp 0
```

## Usage

```sh
usage: tymely.py [-h] [-c CONFIG] [-t]

tymely fetches HTTP-date over HTTPS and sets the system time

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        specifies a configuration file
  -t, --test            don't set the system time, just print the date
```

If no configuration file is used,`tymely` will use `https://duckduckgo.com`
as the site to fetch the `HTTP-date` from, use `tymely/<version>` as user agent,
and set the system date to the returned `HTTP-date`.

### Configuration file options

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
  - "stackoverflow.com"
  - "xkcd.com"
user_agents:
  - "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
  - "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.2.599 Yowser/2.5 Safari/537.36"
  - "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
  - "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
  - "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"
...
```

The above configuration will make `tymely` randomly choose a site and user agent
from the lists presented in the file, and verbosely return any information.

```sh
$ ./tymely.py -c tymely.yaml -t
Verbose mode enabled
Configuration file: tymely.yaml
{'verbose': 1, 'sites': ['cloudflare.com', 'duckduckgo.com', 'github.com', 'stackoverflow.com', 'xkcd.com'], 'user_agents': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.2.599 Yowser/2.5 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0']}
URL: xkcd.com
User agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.2.599 Yowser/2.5 Safari/537.36
Response headers: HTTPHeaderDict({'Connection': 'keep-alive', 'Content-Length': '6552', 'Server': 'nginx', 'Content-Type': 'text/html; charset=UTF-8', 'Last-Modified': 'Wed, 05 Aug 2020 04:00:03 GMT', 'ETag': '"5f2a2ec3-1998"', 'Expires': 'Wed, 05 Aug 2020 04:05:52 GMT', 'Cache-Control': 'max-age=300', 'Accept-Ranges': 'bytes', 'Date': 'Wed, 05 Aug 2020 20:51:21 GMT', 'Via': '1.1 varnish', 'Age': '229', 'X-Served-By': 'cache-cph20623-CPH', 'X-Cache': 'HIT', 'X-Cache-Hits': '1', 'X-Timer': 'S1596660681.304391,VS0,VE1', 'Vary': 'Accept-Encoding'})
Wed, 05 Aug 2020 20:51:21 GMT
```

### Related documentation

<https://tools.ietf.org/html/rfc7231#section-7.1.1.2>

<https://gitlab.com/madaidan/secure-time-sync>
<https://github.com/ioerror/tlsdate>
