"""ARP request parser module."""

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


from argparse import (
    ArgumentParser, Namespace,
)
from collections.abc import Sequence
import logging
from typing import Optional, override

from . import types
from ..modules.parsing.parsers import MainArgumentParserTemplate
from ..network import get_local_ip, get_mac, mac_dec_to_hex_notation


logger = logging.getLogger(__name__)


def _construct() -> ArgumentParser:
    """Returns an instance of the module's argument parser.

    Invoked by the `argparse` directive in the docs.
    For more information, see https://sphinx-argparse.readthedocs.io/en/stable.
    """

    return Arpr()


class Arpr(MainArgumentParserTemplate):
    """Handles the arguments that get passed to the `arpr` command."""

    @override
    def __init__(self):
        super().__init__(
            prog='arpr',
            description='Lightweight utility to send ARP requests.',
            prefix_chars='-',
        )

    def _extend_arguments(self) -> None:
        default_hardware_source = get_mac()
        if default_hardware_source & 2 ** 40:
            default_hardware_source = None
        else:
            default_hardware_source = mac_dec_to_hex_notation(
                default_hardware_source
            )

        default_hardware_destination = 'ff:ff:ff:ff:ff:ff'
        default_protocol_source = get_local_ip()
        default_interval: float = 1.0
        default_count: int = 0

        self.add_argument(
            'destination',
            action='store',
            help='destination IP address',
            metavar='ip',
            type=types.ipv4_address_type,
        )

        self.add_argument(
            '-H',
            action='store',
            default=default_hardware_source,
            dest='ethernet_src',
            help='ETHERNET source address ' +
                 f'(default: {default_hardware_source})' if default_hardware_source else '',
            metavar='mac',
            required=False,
            type=types.mac_address_type,
        )

        self.add_argument(
            '-D',
            action='store',
            default=default_hardware_destination,
            dest='ethernet_dst',
            help='ETHERNET destination address '
                 f'(default: {default_hardware_destination})',
            metavar='mac',
            required=False,
            type=types.mac_address_type,
        )

        self.add_argument(
            '-S',
            action='store',
            default=default_hardware_source,
            dest='arp_hwsrc',
            help='ARP hardware source address '
                 f'(default: {default_hardware_source})',
            metavar='mac',
            required=False,
            type=types.mac_address_type,
        )

        self.add_argument(
            '-s',
            action='store',
            default=default_protocol_source,
            dest='arp_psrc',
            help='ARP protocol source address '
                 f'(default: {default_protocol_source})',
            metavar='ip',
            required=False,
            type=types.ipv4_address_type,
        )

        rate_group = self.add_mutually_exclusive_group(required=False)

        rate_group.add_argument(
            '-c',
            action='store',
            default=default_count,
            dest='packet_count',
            help=f'how many packets to send '
                 f'(default: {'infinite' if default_count == 0 else default_count})',
            metavar='count',
            type=types.strictly_positive_int_type,
        )

        rate_group.add_argument(
            '-i',
            action='store',
            default=default_interval,
            dest='interval',
            help=(
                f'set interval between packets '
                f'(default: {default_interval} sec)'
            ),
            metavar='sec',
            type=types.positive_float_type,
        )

        self.add_argument(
            '-w',
            action='store',
            dest='timeout',
            help='how long to wait for a reply',
            metavar='sec',
            required=False,
            type=types.positive_float_type,
        )

        self.add_argument(
            '-f',
            action='store_true',
            default=False,
            dest='quit_on_first_reply',
            help='quit on first reply',
            required=False,
        )

    def _extend_subparsers(self) -> None:
        pass

    @override
    def parse_args(
            self,
            args: Optional[Sequence[str]] = None,
            namespace: Optional[Namespace] = None
    ) -> Namespace:

        namespace = super().parse_args(args=args, namespace=namespace)
        # arguments = vars(namespace)

        return namespace
