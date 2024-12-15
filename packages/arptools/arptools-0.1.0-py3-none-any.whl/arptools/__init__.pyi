# pylint: skip-file

"""..."""

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

from scapy.packet import Packet
from scapy.plist import PacketList, QueryAnswer, SndRcvList

from .arp.packets.request import _prn, _prn_qofr, _prnfail


__author__: str
__version__: str


def arp_announcement(
        mapping: tuple[str, str],
        ethernet_src: Optional[str] = None,
        ethernet_dst: Optional[str] = None,
        count: int = 0,
        interval: float = 1.0,
        verbose: Optional[int] = None,
) -> None: ...

def arp_pscan(
        target_range: str,
        ttl: int = 60 * 5,
) -> None: ...

def arp_probe(
        target_ip: str,
        count: int = 0,
        interval: float = 1.0,
        quit_on_first_reply: bool = False,
        timeout: Optional[int] = None,
        verbose: Optional[int] = None,
) -> None: ...

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
) -> None: ...

def arp_scan(
        target_range: str,
        use_arp_probes: bool = False,
        timeout: int = 2,
        verbose: Optional[int] = None,
) -> None: ...
