"""Collection of ASCII animations."""

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


from itertools import cycle
from math import ceil


class Animation:
    """Represents an ASCII animation.

    This class is just a wrapper around a cyclic iterator containing the animation frames.
    """

    def __init__(self, *args: str):
        """Args:
            *args:
                sequence of strings representing the frames of the animation.
        """

        self._frames = tuple(args)
        self._iterator = cycle(self._frames)

    def frame_from_state(self, state: float) -> str:
        """Returns the animation frame corresponding to a certain state.

        Args:
            state:
                float between 0 and 1 representing the animation state.
        """

        return self.frames[max(ceil(state * self.length) - 1, 0)]

    def __next__(self):
        return next(self._iterator)

    @property
    def frames(self) -> tuple[str, ...]:
        """The animation frames."""

        return self._frames

    @property
    def length(self) -> int:
        """The number of frames."""

        return len(self.frames)
