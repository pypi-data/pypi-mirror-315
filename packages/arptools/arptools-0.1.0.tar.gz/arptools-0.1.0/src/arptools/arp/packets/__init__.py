"""Contains primitive functions to send ARP packets."""

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


from contextlib import redirect_stdout
from io import StringIO

from scapy.packet import Packet
from scapy.plist import PacketList, QueryAnswer, SndRcvList


def _fmt_summary(summary: str) -> str | None:
    summary = (
        summary
        .replace('Ether / ', '')
        .replace(' / Padding', '')
        .replace('None', '')
        .rstrip()
    )

    if summary:
        return ''.join(('\r', summary))

    return None


def _prn(answer: QueryAnswer) -> str | None:
    with redirect_stdout(stream := StringIO()):
        SndRcvList([answer]).summary()

    return _fmt_summary(stream.getvalue())


def _prn_qofr(answer: QueryAnswer) -> None:
    print(_prn(answer))

    raise KeyboardInterrupt


def _prnfail(unanswered: Packet | PacketList | SndRcvList) -> str | None:
    with redirect_stdout(stream := StringIO()):
        PacketList([unanswered]).summary()

    return _fmt_summary(stream.getvalue())
