"""ARP scan parser module."""

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
from ..network import get_mac, mac_dec_to_hex_notation


logger = logging.getLogger(__name__)


def _construct() -> ArgumentParser:
    """Returns an instance of the module's argument parser.

    Invoked by the `argparse` directive in the docs.
    For more information, see https://sphinx-argparse.readthedocs.io/en/stable.
    """

    return Arpa()


class Arpa(MainArgumentParserTemplate):
    """Handles the arguments that get passed to the `arpa` command."""

    @override
    def __init__(self):
        super().__init__(
            prog='arpa',
            description='Send ARP announcements.',
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
        default_interval: float = 1.0
        default_count: int = 0

        self.add_argument(
            'mac',
            action='store',
            help='MAC address to announce',
            metavar='mac',
            type=types.mac_address_type,
        )

        self.add_argument(
            'ip',
            action='store',
            help='IP address to announce',
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

    def _extend_subparsers(self) -> None:
        pass

    @override
    def parse_args(
            self,
            args: Optional[Sequence[str]] = None,
            namespace: Optional[Namespace] = None
    ) -> Namespace:

        namespace = super().parse_args(args=args, namespace=namespace)

        namespace.mapping = (namespace.mac, namespace.ip)
        delattr(namespace, 'mac')
        delattr(namespace, 'ip')

        return namespace
