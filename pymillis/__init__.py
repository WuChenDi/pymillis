"""
pymillis - Milliseconds conversion utility

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

from .ms import ms, parse, parse_strict, format, MSError
from ._version import __version__

__all__ = ['ms', 'parse', 'parse_strict', 'format', 'MSError', '__version__']
