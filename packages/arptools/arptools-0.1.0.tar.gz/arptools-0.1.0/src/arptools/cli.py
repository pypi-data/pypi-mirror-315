"""Command Line Interface entry point."""

# Copyright (C) 2024  Stefano Cuizza

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


from argparse import Namespace

from .arp import (
    arp_announcement,
    arp_probe,
    arp_request,
    arp_pscan,
    arp_scan,
)


def arpa(namespace: Namespace) -> None:
    """Arpa CLI.

    Args:
        namespace:
          Namespace containing the command line arguments.
    """

    arp_announcement(
        mapping=namespace.mapping,
        ethernet_src=namespace.ethernet_src,
        ethernet_dst=namespace.ethernet_dst,
        count=namespace.packet_count,
        interval=namespace.interval,
        verbose=0 if namespace.quiet else None,
    )


def arpr(namespace: Namespace) -> None:
    """Arpr CLI.

    Args:
        namespace:
          Namespace containing the command line arguments.
    """

    arp_request(
        target_ip=namespace.destination,
        ethernet_src=namespace.ethernet_src,
        ethernet_dst=namespace.ethernet_dst,
        arp_hwsrc=namespace.arp_hwsrc,
        arp_psrc=namespace.arp_psrc,
        count=namespace.packet_count,
        interval=namespace.interval,
        quit_on_first_reply=namespace.quit_on_first_reply,
        timeout=namespace.timeout,
        verbose=0 if namespace.quiet else None,
    )


def arprobe(namespace: Namespace) -> None:
    """Arprobe CLI.

    Args:
        namespace:
          Namespace containing the command line arguments.
    """

    arp_probe(
        target_ip=namespace.destination,
        count=namespace.packet_count,
        interval=namespace.interval,
        quit_on_first_reply=namespace.quit_on_first_reply,
        timeout=namespace.timeout,
        verbose=0 if namespace.quiet else None,
    )


def arpscan(namespace: Namespace) -> None:
    """Arpscan CLI.

    Args:
        namespace:
          Namespace containing the command line arguments.
    """

    if namespace.passive:
        arp_pscan(
            target_range=namespace.destination_range,
            ttl=namespace.time_to_live,
        )

        return

    arp_scan(
        target_range=namespace.destination_range,
        use_arp_probes=namespace.use_arp_probes,
        timeout=namespace.timeout,
        verbose=0 if namespace.quiet else None,
    )
