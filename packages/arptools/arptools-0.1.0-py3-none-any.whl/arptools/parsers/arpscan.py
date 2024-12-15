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


logger = logging.getLogger(__name__)


def _construct() -> ArgumentParser:
    """Returns an instance of the module's argument parser.

    Invoked by the `argparse` directive in the docs.
    For more information, see https://sphinx-argparse.readthedocs.io/en/stable.
    """

    return Arpscan()


class Arpscan(MainArgumentParserTemplate):
    """Handles the arguments that get passed to the `arprobe` command."""

    @override
    def __init__(self):
        super().__init__(
            prog='arpscan',
            description='Scan the network using ARP requests.',
            prefix_chars='-',
        )

    def _extend_arguments(self) -> None:
        default_time_to_live: int = 60 * 5
        default_timeout: float = 2.0

        self.add_argument(
            'destination_range',
            action='store',
            help='ip address or subnet to scan',
            metavar='ip | cidr',
            type=types.ipv4_cidr_type,
        )

        mode_group = self.add_mutually_exclusive_group(required=False)

        mode_group.add_argument(
            '-p', '--use-probes',
            action='store_true',
            default=False,
            dest='use_arp_probes',
            help='use ARP probes',
            required=False,
        )

        mode_group.add_argument(
            '-P', '--passive',
            action='store_true',
            default=False,
            dest='passive',
            help='extrapolate ARP associations from ARP requests',
            required=False,
        )

        mode_group.add_argument(
            '-t', '--ttl',
            action='store',
            default=default_time_to_live,
            dest='time_to_live',
            help='set a time to live for ARP packets in passive mode.' +
                 f'(default: {default_time_to_live})',
            metavar='sec',
            required=False,
        )

        self.add_argument(
            '-w',
            action='store',
            default=default_timeout,
            dest='timeout',
            help=(
                'how long to wait for a reply '
                f'(default: {default_timeout} sec)'
            ),
            metavar='sec',
            required=False,
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
        # arguments = vars(namespace)

        return namespace
