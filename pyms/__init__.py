"""
pyms - Milliseconds conversion utility

A Python port of the popular JavaScript ms library.
Convert between milliseconds and human-readable time strings.

Usage:
    >>> from pyms import ms
    >>> ms('2 days')
    172800000
    >>> ms(172800000)
    '2d'
    >>> ms(172800000, long=True)
    '2 days'
"""

from pyms.ms import ms, parse, parse_strict, format, MSError
from pyms._version import __version__

__all__ = ['ms', 'parse', 'parse_strict', 'format', 'MSError', '__version__']
