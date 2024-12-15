"""A collection of network utility functions."""

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


from functools import lru_cache
import socket
from typing import Literal
from uuid import getnode as get_mac  # noqa: F401

from scapy.config import conf


# UnkwnTech (2008, October 3). Finding local IP addresses using Python's stdlib. StackOverflow.
# https://stackoverflow.com/a/166589.
@lru_cache
def get_local_ip() -> str:
    """Returns the local IP address of the machine."""

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect(('1.1.1.1', 80))

        return sock.getsockname()[0]


@lru_cache
def get_local_gateway() -> str:
    """Returns the local gateway address."""

    return conf.route.route('0.0.0.0')[2]


def mac_dec_to_hex_notation(mac_address: int, separator: Literal[':', '-'] = ':') -> str:
    """Translates a decimal MAC address in its human-readable representation.

    Args:
        mac_address:
            the MAC address to translate.
        separator:
            character to use as a separator.
    """

    mac_hex = f'{mac_address:012x}'
    return separator.join(mac_hex[i:i + 2] for i in range(0, len(mac_hex), 2))
