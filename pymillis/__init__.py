"""pymillis - Milliseconds conversion utility.

Use this package to easily convert various time formats to milliseconds.

Usage:
    >>> from pymillis import ms
    >>> ms('2 days')
    172800000
    >>> ms(172800000)
    '2d'
    >>> ms(172800000, long=True)
    '2 days'
"""

from ._version import __version__
from .ms import ErrorCode, MSError, format, ms, parse, parse_strict, parse_timedelta

__all__ = [
    "ErrorCode",
    "MSError",
    "__version__",
    "format",
    "ms",
    "parse",
    "parse_strict",
    "parse_timedelta",
]
