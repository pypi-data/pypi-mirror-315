"""Provides functions to send ARP  announcements."""

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

from scapy.layers.l2 import ARP
from scapy.packet import Packet
from scapy.plist import PacketList, SndRcvList

from .packets.request import arp_request


def arp_announcement(
        mapping: tuple[str, str],
        ethernet_src: Optional[str] = None,
        ethernet_dst: Optional[str] = None,
        count: int = 0,
        interval: float = 1.0,
        verbose: Optional[int] = None,
) -> None:
    """Sends and ARP announcement advertising the given MAC/IP mapping.

    Args:
        mapping:
            a MAC/IP pair.
        ethernet_src:
            the source MAC address of the Ethernet frame.
        ethernet_dst:
            the destination MAC address of the Ethernet frame.
        count:
            how many packet to send.
        interval:
            time interval between packets (only used when count is 0).
        verbose:
            verbosity level.
    """

    def _arp_announcement_prnfail(unanswered: Packet | PacketList | SndRcvList) -> str | None:
        return '\n'.join((
            f'\rARP announcement {pkt.pdst} ({pkt.hwsrc})' for pkt in unanswered[ARP]
        ))

    arp_request(
        target_ip=mapping[1],
        ethernet_src=ethernet_src,
        ethernet_dst=ethernet_dst,
        arp_hwsrc=mapping[0],
        arp_psrc=mapping[1],
        count=count,
        interval=interval,
        quit_on_first_reply=False,
        timeout=0,
        ignore_unanswered=False,
        verbose=verbose,
        prnfail=_arp_announcement_prnfail,
    )
