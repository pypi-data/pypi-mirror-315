"""Provides functions to do a network scan with ARP packets."""

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


from typing import Optional

from .packets.request import arp_request


def arp_scan(
        target_range: str,
        use_arp_probes: bool = False,
        timeout: int = 2,
        verbose: Optional[int] = None,
) -> None:
    """Performs an ARP scan of the network by sending ARP requests to all the
    IPs in range and waiting for a response.

    Args:
        target_range:
            target IP range in CIDR notation (e.g. 192.168.1.0/24).
        use_arp_probes:
            whether to use ARP probes to scan the network.
        timeout:
            how long to wait for a reply.
        verbose:
            verbosity level.
    """

    arp_request(
        target_ip=target_range,
        arp_psrc='0.0.0.0' if use_arp_probes else None,
        count=1,
        timeout=timeout,
        ignore_unanswered=True,
        verbose=verbose,
    )
