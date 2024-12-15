"""Provides functions to do a network scan with ARP packets."""
import sys
from collections import defaultdict
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


from datetime import datetime
from functools import partial
from ipaddress import ip_address, ip_network
from queue import SimpleQueue
from threading import Thread, Event


from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import ManagedScreen, Screen
from asciimatics.widgets import Frame
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import sniff

from ..modules.ansi import Cursor, echo_ansi, fg_rgb, Fore
from ..modules.ascii.animation import Animation
from ..modules.utils import ExpirableDict
from ..network import get_local_gateway, get_local_ip


class MappingModel:
    """Data model that holds the MAC/IP associations extracted from sniffed ARP packets."""

    class StoppableThread(Thread):
        """Thread class with a stop() method.

        The thread itself has to check regularly for the stopped() condition.
        """

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._stop_event = Event()

        def stop(self):
            """Stops the thread."""

            self._stop_event.set()

        def stopped(self):
            """Whether the thread has been stopped or not."""

            return self._stop_event.is_set()

    def __init__(self, target_range: str, ttl: int):
        """Args:
            target_range:
                the target IP range, in CIDR notation.
            ttl:
                initial time to live for a new mapping, in seconds.
        """

        self._target_range, self._ttl = target_range, ttl
        self._db, self._queue = ExpirableDict(delta=ttl), SimpleQueue()
        self._total_requests: int = 0

        self._sniff_thread: MappingModel.StoppableThread | None = None

    def start_gatherer(self) -> None:
        """Starts the ARP sniffer as a background thread."""

        self._init_sniffer()
        self._sniff_thread.start()

    def stop_gatherer(self) -> None:
        """Stops the ARP sniffer."""

        self._sniff_thread.stop()
        self._sniff_thread.join()

    @property
    def is_gatherer_alive(self) -> bool:
        """Whether the ARP sniffer thread is alive."""

        if self._sniff_thread:
            return self._sniff_thread.is_alive()

        return False

    @property
    def ttl(self) -> int:
        """The time to live for every ARP request."""

        return self._ttl

    @property
    def requests(self) -> int:
        """The total number of sniffed ARP requests (excluding probes)."""

        return self._total_requests

    @property
    def db(self) -> ExpirableDict:
        """The internal mapping database."""

        return self._db

    def _init_sniffer(self) -> None:
        self._sniff_thread = MappingModel.StoppableThread(target=sniff, kwargs={
            'filter': 'arp',
            'prn': partial(self._arp_monitor_callback, ip_range=self._target_range),
            'stop_filter': lambda p: self._sniff_thread.stopped(),
            'store': 0,
        })
        self._total_requests = 0

    def _arp_monitor_callback(self, pkt, ip_range: str) -> None:
        if ARP in pkt and pkt[ARP].op not in (1,):
            return

        if ip_address(pkt[ARP].psrc) not in ip_network(ip_range, strict=False):
            return

        if pkt[ARP].psrc in ('0.0.0.0',):
            return

        self._total_requests += 1
        self._db[pkt[Ether].hwsrc] = pkt[ARP].psrc


class MainView(Frame):
    """Main view for the passive scan TUI."""

    _TTL_GRADIENT: tuple[str, ...] = (
        fg_rgb(102, 102, 102),
        fg_rgb(153, 153, 153),
        fg_rgb(204, 204, 204),
        fg_rgb(225, 225, 225),
    )
    _LG_ENTRY_COLOR: str = Fore.LIGHTMAGENTA_EX
    _LI_ENTRY_COLOR: str = Fore.LIGHTGREEN_EX

    _FOOTER: str = '  '.join((
        f'{''.join(f'{c}●' for c in _TTL_GRADIENT)}{Fore.RESET}: ttl',
        f'{_LG_ENTRY_COLOR}●{Fore.RESET}: gateway',
        f'{_LI_ENTRY_COLOR}●{Fore.RESET}: local ip',
        '↑: scroll up',
        '↓: scroll down',
    ))

    def __init__(self, screen, model: MappingModel):
        """Args:
            screen:
                screen instance.
            model:
                data model to hold passive scan data.
        """

        assoc_counter: int = len(model.db)

        super().__init__(
            screen=screen,
            height=screen.height,
            width=screen.width,
            has_border=True,
            title=(
                f'ARP requests{f' | {assoc_counter} / {model.requests}'
                if assoc_counter else ''}'
            ),
        )

        self._model: MappingModel = model
        self._scroll_index: int = 0

        self._frame_update_count: int = 1
        self._ttl_animation = Animation(*self._TTL_GRADIENT)

        self.fix()

        self.palette = defaultdict(
            lambda: (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        )
        for key in ('label',):
            self.palette[key] = (
                Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK
            )

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            match event.key_code:
                case -204:
                    self.scroll_up()
                case -206:
                    self.scroll_down()
    
    def scroll_down(self) -> None:
        """Scrolls down the display window."""

        if self._scroll_index + (self.screen.height - 2) < len(self._model.db):
            self._scroll_index += 1

    def scroll_up(self) -> None:
        """Scrolls up the display window."""

        if self._scroll_index > 0:
            self._scroll_index -= 1

    def _clear_display_window(self) -> None:
        for y in range(2, self.screen.height):
            echo_ansi(Cursor.POS)(3, y)
            print(' ' * (self.screen.width - 5), end='')

    def _update(self, frame_no):
        assoc_counter: int = len(self._model.db)
        self.title = (
            f'ARP requests{f' | {assoc_counter} / {self._model.requests}'
            if assoc_counter else ''}'
        )

        sorted_db = dict(sorted(
            self._model.db.items(),
            key=lambda item: int(ip_address(item[1]))
        ))

        self._clear_display_window()
        for y, (hwsrc, psrc) in zip(
                range(2, self.screen.height),
                tuple(sorted_db.items())[self._scroll_index:],
        ):
            cttl = int((
                self._model.db.get_expiration_date(hwsrc) - datetime.now()
            ).total_seconds())

            line_color = self._ttl_animation.frame_from_state(cttl / self._model.ttl)
            if psrc == get_local_gateway():
                line_color = self._LG_ENTRY_COLOR
            elif psrc == get_local_ip():
                line_color = self._LI_ENTRY_COLOR

            echo_ansi(Cursor.POS)(3, y)
            print(f'{line_color}{hwsrc} <== {psrc}{Fore.RESET}', end='')

        super()._update(frame_no)

        self._render_footer()

    def _render_footer(self) -> None:
        footer_length: int = 66

        if (x_pos := (self.screen.width - footer_length) // 2) >= 0:
            echo_ansi(Cursor.POS)(x_pos + 1, self.screen.height)
            print(f' {self._FOOTER} ', end='')

    @property
    def frame_update_count(self) -> int:
        """The number of frames before this Effect should be updated."""

        # by making frame_update_count refer to an actual class variable, it can
        # be dynamically modified to change the refresh rate of the frame.
        return self._frame_update_count

    @frame_update_count.setter
    def frame_update_count(self, value):
        self._frame_update_count = value


class PassiveScanTUI:
    """Context manager that provides a nice TUI for the passive ARP scanner.

    Typical usage:
        with PassiveScanTUI(model) as tui:
            tui.show()
    """

    def __init__(self, model: MappingModel):
        """Args:
            model:
                data model to hold passive scan data.
        """

        self._model = model

    def show(self, interactive: bool = True) -> None:
        """Starts the TUI."""

        if not self._model.is_gatherer_alive:
            self._model.start_gatherer()

        while True:
            try:
                with ManagedScreen() as screen:
                    scenes = (Scene([MainView(screen, self._model)], -1),)
                    screen.play(scenes, stop_on_resize=True)

            except ResizeScreenError:
                self.show(interactive)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._model.stop_gatherer()


def arp_pscan(target_range: str, ttl: int = 60 * 5) -> None:
    """Performs a passive scan of the network by extracting MAC/IP pairs
    from broadcast ARP requests.

    Args:
        target_range:
            the target IP range, in CIDR notation.
        ttl:
            initial time to live for a new mapping, in seconds.
    """

    model = MappingModel(target_range, ttl)

    try:
        with PassiveScanTUI(model) as tui:
            tui.show()
    except KeyboardInterrupt:
        pass
    finally:
        for hwsrc, psrc in model.db.items():
            print(f'{hwsrc} <== {psrc}')

        sys.exit()
