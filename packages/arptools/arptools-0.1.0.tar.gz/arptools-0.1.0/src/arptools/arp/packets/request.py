"""Provides functions to send ARP requests."""

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


from collections.abc import Callable
from typing import Optional

from scapy.layers.l2 import ARP, Ether
from scapy.packet import Packet
from scapy.plist import PacketList, QueryAnswer, SndRcvList
from scapy.sendrecv import srp, srploop

from . import _prn, _prn_qofr, _prnfail


def arp_request(
        target_ip: str,
        ethernet_src: Optional[str] = None,
        ethernet_dst: Optional[str] = None,
        arp_hwsrc: Optional[str] = None,
        arp_psrc: Optional[str] = None,
        count: int = 0,
        interval: float = 1.0,
        quit_on_first_reply: bool = False,
        timeout: Optional[int] = None,
        ignore_unanswered: bool = False,
        verbose: Optional[int] = None,
        prn: Callable[[QueryAnswer], str | None] = _prn,
        prn_qofr: Callable[[QueryAnswer], None] = _prn_qofr,
        prnfail: Callable[[Packet | PacketList | SndRcvList], str | None] = _prnfail,
) -> None:
    """Sends an ARP request packet.

    Args:
        target_ip:
            the target IP of the ARP request.
        ethernet_src:
            the source MAC address of the Ethernet frame.
        ethernet_dst:
            the destination MAC address of the Ethernet frame.
        arp_hwsrc:
            the hardware source address of the ARP packet.
        arp_psrc:
            the protocol source address of the ARP packet.
        count:
            how many packet to send.
        interval:
            time interval between packets (only used when count is 0).
        quit_on_first_reply:
            sends packets until it gets a reply.
        timeout:
            how long to wait for a reply.
        ignore_unanswered:
            whether to print unanswered packets.
        verbose:
            verbosity level.
        prn:
            function used to print packets that have received an answer.
        prn_qofr:
            function used to print packets that have received an answer
            when quit_on_first_reply is True.
        prnfail:
            function used to print packets that have not received an answer.
    """

    pkt = (
            Ether(dst=ethernet_dst, src=ethernet_src) /
            ARP(op='who-has', hwsrc=arp_hwsrc, psrc=arp_psrc, pdst=target_ip)
    )

    if count:
        if quit_on_first_reply:
            for _ in range(count):
                results, unanswered = srp(
                    pkt,
                    timeout=timeout if timeout else 1,
                    verbose=0,
                )

                if verbose != 0:
                    if prn_results := prnfail(results):
                        print('', prn_results, sep='\n', end='')

                    if (prn_unanswered := prnfail(unanswered)) and not ignore_unanswered:
                        print(prn_unanswered, end='')
        else:
            results, unanswered = srp(
                pkt if count == 1 else tuple(pkt for _ in range(count)),
                timeout=timeout,
                verbose=verbose,
            )

            if verbose != 0:
                if prn_results := prnfail(results):
                    print('', prn_results, sep='\n')

                if (prn_unanswered := prnfail(unanswered)) and not ignore_unanswered:
                    print(prn_unanswered)

        return

    srploop(
        pkt,
        inter=interval,
        prn=prn_qofr if quit_on_first_reply else prn,
        prnfail=prnfail if not ignore_unanswered else lambda i: ...,
        timeout=timeout,
        verbose=verbose,
    )
