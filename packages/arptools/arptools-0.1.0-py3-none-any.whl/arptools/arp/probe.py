"""Provides functions to send ARP probes."""

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


def arp_probe(
        target_ip: str,
        count: int = 0,
        interval: float = 1.0,
        quit_on_first_reply: bool = False,
        timeout: Optional[int] = None,
        verbose: Optional[int] = None,
) -> None:
    """Sends an ARP probe to the specified target.

    Args:
        target_ip:
            the destination IP.
        count:
            how many packet to send.
        interval:
            time interval between packets (only used when count is 0).
        quit_on_first_reply:
            sends packets until it gets a reply.
        timeout:
            how long to wait for a reply.
        verbose:
            verbosity level.
    """

    arp_request(
        target_ip=target_ip,
        arp_psrc='0.0.0.0',
        count=count,
        interval=interval,
        quit_on_first_reply=quit_on_first_reply,
        timeout=timeout,
        ignore_unanswered=False,
        verbose=verbose,
    )
