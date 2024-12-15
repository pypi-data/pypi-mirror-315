"""Contains useful ArgumentParser types."""

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


from argparse import ArgumentTypeError
from ipaddress import ip_address, IPv6Address
from random import randint
import re

from ..modules.utils import LazyDict
from ..network import (
    get_local_gateway,
    get_local_ip,
    mac_dec_to_hex_notation,
)


MAC_ADDRESS_PATTERN: re.Pattern[str] = re.compile(
    r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
)


def ipv4_address_type(argument: str) -> str:
    """Parser type matching an IPv4 address.

    Raises:
        ValueError:
            the argument is not a valid IPv4 address.
    """

    # load hosts lazily to avoid crashing if one of them does not resolve.
    host_mapping = LazyDict({
        'all': (lambda i: i, '0.0.0.0',),
        'gateway': (lambda _: get_local_gateway(), None),
        'local': (lambda _: get_local_ip(), None),
        'localhost': (lambda i: i, '127.0.0.1',),
    })
    """Maps common host names to their corresponding ipv4 address."""

    if isinstance(ip := ip_address(host_mapping.get(argument, argument)), IPv6Address):
        raise ArgumentTypeError(
            'the ARP protocol does not support IPv6 addresses'
        )

    return str(ip)


def ipv4_cidr_type(argument: str) -> str:
    """Parser type matching an IPv4 CIDR.

    Raises:
        ValueError:
            the argument is not a valid IPv4 CIDR.
    """

    if '/' in argument:
        ip, subnet = argument.split('/', 1)
        ip = ipv4_address_type(ip)

        if not 0 < (subnet := int(subnet)) <= 24:
            raise ValueError('subnet not in range (0, 24]')

        return '/'.join((ip, str(subnet)))

    return ipv4_address_type(argument)




def mac_address_type(argument: str) -> str:
    """Parser type matching a MAC address.

    Raises:
        ValueError:
            the argument is not a valid MAC address.
    """

    mac_address_mapping: dict[str, str] = {
        '0': '00:00:00:00:00:00',
        'zero': '00:00:00:00:00:00',
        'broadcast': 'ff:ff:ff:ff:ff:ff',
        'random': mac_dec_to_hex_notation(randint(0, 2**48)),
    }
    """Maps common mac names to their corresponding mac address."""

    if argument.isnumeric():
        if (argument := int(argument)) >= 2**48:
            raise ValueError

        return mac_dec_to_hex_notation(argument)

    argument = mac_address_mapping.get(argument, argument)
    if not MAC_ADDRESS_PATTERN.match(argument):
        raise ValueError

    return argument


def strictly_positive_int_type(argument: str) -> int:
    """Parser type matching a strictly positive integer.

    Raises:
        ValueError:
            the argument is not an integer >0.
    """

    try:
        argument = int(argument)
    except ValueError as err:
        raise ValueError from err

    if argument <= 0:
        raise ArgumentTypeError('must be an integer greater then zero')

    return argument


def positive_float_type(argument: str) -> float:
    """Parser type matching a positive float.

    Raises:
        ValueError:
            the argument is not a float >=0.
    """

    try:
        argument = float(argument)
    except ValueError as err:
        raise ValueError from err

    if argument < 0:
        raise ArgumentTypeError('must be a float greater or equal to zero')

    return argument
