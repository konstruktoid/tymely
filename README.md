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
{'verbose': 1, 'sites': ['cloudflare.com', 'duckduckgo.com', 'github.com', 'stackoverflow.com', 'xkcd.com'], 'user_agents': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.
169 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.2.599 Yowser/2.5 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like
Gecko', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0']}
URL: duckduckgo.com
User agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36
Response headers: HTTPHeaderDict({'Server': 'nginx', 'Date': 'Fri, 02 Oct 2020 17:45:11 GMT', 'Content-Type': 'text/html; charset=UTF-8', 'Content-Length': '5763', 'Connection': 'keep-alive', 'Vary': 'Accept-Encoding', 'ETag': '"5
f761b76-1683"', 'Strict-Transport-Security': 'max-age=31536000', 'X-Frame-Options': 'SAMEORIGIN', 'Content-Security-Policy': "default-src https: blob: data: 'unsafe-inline' 'unsafe-eval'; frame-ancestors 'self'", 'X-XSS-Protection
': '1;mode=block', 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'origin', 'Expect-CT': 'max-age=0', 'Expires': 'Fri, 02 Oct 2020 17:45:10 GMT', 'Cache-Control': 'no-cache', 'Accept-Ranges': 'bytes'})
Verify_mode: VerifyMode.CERT_REQUIRED
TLS context options: Options.OP_NO_TLSv1_1|OP_NO_TLSv1|OP_NO_SSLv3|OP_CIPHER_SERVER_PREFERENCE|OP_ENABLE_MIDDLEBOX_COMPAT|OP_NO_COMPRESSION|OP_ALL
[{'id': 50336514, 'name': 'TLS_AES_256_GCM_SHA384', 'protocol': 'TLSv1.3', 'description': 'TLS_AES_256_GCM_SHA384  TLSv1.3 Kx=any      Au=any  Enc=AESGCM(256) Mac=AEAD', 'strength_bits': 256, 'alg_bits': 256, 'aead': True, 'symmetric': 'aes-256-gcm', 'digest': None, 'kea': 'kx-any', 'auth': 'auth-any'},{...}]
Fri, 02 Oct 2020 17:45:11 GMT returned but not set
```

### Related documentation

<https://tools.ietf.org/html/rfc7231#section-7.1.1.2>

<https://www.whonix.org/wiki/Time_Attacks>

<https://gitlab.com/madaidan/secure-time-sync>

<https://github.com/ioerror/tlsdate>
