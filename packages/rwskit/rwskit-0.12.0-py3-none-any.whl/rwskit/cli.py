from __future__ import annotations

# Python Modules
import logging

from typing import List, Union

# 3rd Party Modules

# Project Modules


class LogLevel(int):
    """A class for converting logging level string names to their integer counterparts."""
    def __new__(cls, level: Union[str, int]):
        if isinstance(level, int):
            try:
                # noinspection PyUnresolvedReferences,PyProtectedMember
                return super().__new__(cls, level) if logging._levelToName[level] else None
            except KeyError:
                raise TypeError(f"Invalid logging level: {level}")

        # Otherwise we've got a string
        level = level.upper()

        try:
            # noinspection PyUnresolvedReferences,PyProtectedMember
            return super().__new__(cls, logging._nameToLevel[level])
        except KeyError:
            raise TypeError(f"invalid logging level: {level}")

    def __repr__(self):
        # noinspection PyUnresolvedReferences,PyProtectedMember
        return logging._levelToName[self]

    def __str__(self):
        return self.__repr__()

    @classmethod
    def valid_levels(cls) -> List[LogLevel]:
        """
        Returns the list of valid log levels.

        Returns
        -------
        list[LogLevel]
            The list of valid log levels.
        """
        return [LogLevel(name) for name in log_level_choices()]  # noqa
