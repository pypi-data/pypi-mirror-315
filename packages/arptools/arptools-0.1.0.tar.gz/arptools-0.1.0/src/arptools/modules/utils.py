"""A collection of utility functions."""

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


from collections import UserDict
from collections.abc import Mapping
from datetime import datetime, timedelta
from typing import Any


class ExpirableDict(UserDict):
    """Dictionary whose items expire after a set amount of time."""

    def __init__(self, *args, delta: int, **kwargs):
        """Args:
            delta:
                the time to live of an item in seconds.
        """

        super().__init__(*args, **kwargs)

        self._delta = timedelta(seconds=delta)
        self._ttl: dict[Any, datetime] = {}

    def get_expiration_date(self, item) -> datetime:
        """Returns the expiration date of given item."""

        return self._ttl[item] + self._delta

    def prune(self) -> None:
        """Remove expired entries from the dictionary."""

        for key in tuple(self.data):
            try:
                self[key]
            except KeyError:
                pass

    def items(self):
        self.prune()

        return super().items()

    @property
    def delta(self) -> int:
        """Time after a stale entry is deleted."""

        return self.delta

    def __getitem__(self, item):
        value = self.data[item]

        if (datetime.now() - self._ttl[item]) > self._delta:
            del self[item]
            del self._ttl[item]

            raise KeyError(item)

        return value

    def __setitem__(self, key, value):
        self.data[key] = value
        self._ttl[key] = datetime.now()


# Guangyang Li (2017, November 9). Setup dictionary lazily. StackOverflow.
# https://stackoverflow.com/a/47212782.
class LazyDict(Mapping):
    """Dictionary whose values are lazily loaded."""

    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)

    def __getitem__(self, key):
        func, arg = self._dict.__getitem__(key)

        return func(arg)

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)
