
# 📦 arptools

[![License: GPL v3](https://img.shields.io/badge/License-GPL_v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![Python version: 3.12+](https://img.shields.io/badge/python-3.12+-blue)
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)


## Overview

This package offers a collection of tools to perform network analysis with `ARP` packets.


## Installation

Install the package with `pip`:

```bash
$ pip install arptools
```


## Usage

### arpa

Send `ARP announcements` over the network.

```bash
# advertises the (de:ad:be:ef:00:00, local) mapping to the network.
$ arpa de:ad:be:ef:00:00 local
```


### arprobe

Send `ARP probes` over the network.

```bash
# sends ARP probes to the gateway until it responds.
$ arprobe gateway -f
```


### arpscan

Scans the network with ARP requests.

```bash
# scans the gateway /24 subnet using ARP probes.
$ arpscan gateway/24 -p
```

```bash
# extrapolates MAC/IP pairs from broadcast request packets (passive mode).
$ arpscan gateway/24 -P
```


### arpr

Send `ARP requests` over the network.

```bash
# sends an ARP request to the gateway with a spoofed MAC and IP source address.
$ arpr -S de:ad:be:ef:00:00 -s 192.168.1.20 gateway
```


## Documentation

- [Official Documentation](https://x55xaa.github.io/arptools)
- [CHANGELOG](CHANGELOG.md)
