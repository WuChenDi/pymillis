"""
pyms.ms - Core milliseconds conversion functionality
"""

import re
import math
from typing import Union

__all__ = ['ms', 'parse', 'parse_strict', 'format', 'MSError']

# Time constants in milliseconds
S = 1000
M = S * 60
H = M * 60
D = H * 24
W = D * 7
Y = D * 365.25
MO = Y / 12


class MSError(Exception):
    """Base exception for ms library errors."""
    pass


def ms(value: Union[str, int, float], *, long: bool = False) -> Union[float, str]:
    """
    Parse or format the given value.
    
    Args:
        value: The string or number to convert
        long: Set to True to use verbose formatting. Defaults to False.
        
    Returns:
        If value is a string, returns milliseconds as number (float).
        If value is a number, returns formatted string.
        
    Raises:
        MSError: If value is not a non-empty string or a number
        
    Examples:
        >>> ms('2 days')
        172800000.0
        >>> ms(172800000)
        '2d'
        >>> ms(172800000, long=True)
        '2 days'
    """
    if isinstance(value, str):
        return parse(value)
    elif isinstance(value, (int, float)):
        return format(value, long=long)
    else:
        raise MSError(
            f"Value provided to ms() must be a string or number. value={repr(value)}"
        )


def parse(value: str) -> float:
    """
    Parse the given string and return milliseconds.
    
    Args:
        value: A string to parse to milliseconds
        
    Returns:
        The parsed value in milliseconds, or raises MSError if invalid
        
    Raises:
        MSError: If the string is invalid or cannot be parsed
        
    Examples:
        >>> parse('2d')
        172800000.0
        >>> parse('1.5 hours')
        5400000.0
        >>> parse('1y')
        31557600000.0
    """
    if not isinstance(value, str):
        raise MSError(
            f"Value provided to ms.parse() must be a string. value={repr(value)}"
        )
    
    if len(value) == 0 or len(value) > 100:
        raise MSError(
            f"Value provided to ms.parse() must be a string with length between 1 and 99. value={repr(value)}"
        )
    
    pattern = r'^(?P<value>-?\d*\.?\d+)\s*(?P<unit>milliseconds?|msecs?|ms|seconds?|secs?|s|minutes?|mins?|m|hours?|hrs?|h|days?|d|weeks?|w|months?|mo|years?|yrs?|y)?$'
    match = re.match(pattern, value, re.IGNORECASE)
    
    if not match:
        raise MSError(f"Invalid time string format. value={repr(value)}")
    
    groups = match.groupdict()
    num_value = float(groups['value'])
    unit = (groups['unit'] or 'ms').lower()
    
    # Years
    if unit in ('years', 'year', 'yrs', 'yr', 'y'):
        return num_value * Y
    # Months
    elif unit in ('months', 'month', 'mo'):
        return num_value * MO
    # Weeks
    elif unit in ('weeks', 'week', 'w'):
        return num_value * W
    # Days
    elif unit in ('days', 'day', 'd'):
        return num_value * D
    # Hours
    elif unit in ('hours', 'hour', 'hrs', 'hr', 'h'):
        return num_value * H
    # Minutes
    elif unit in ('minutes', 'minute', 'mins', 'min', 'm'):
        return num_value * M
    # Seconds
    elif unit in ('seconds', 'second', 'secs', 'sec', 's'):
        return num_value * S
    # Milliseconds
    elif unit in ('milliseconds', 'millisecond', 'msecs', 'msec', 'ms'):
        return num_value
    else:
        raise MSError(
            f'Unknown unit "{unit}" provided to ms.parse(). value={repr(value)}'
        )


def parse_strict(value: str) -> float:
    """
    Parse the given string and return milliseconds (strict version).
    
    This is an alias for parse() provided for API compatibility.
    
    Args:
        value: A string to parse to milliseconds
        
    Returns:
        The parsed value in milliseconds
    """
    return parse(value)


def format(ms_value: Union[int, float], *, long: bool = False) -> str:
    """
    Format the given milliseconds as a string.
    
    Args:
        ms_value: Milliseconds to format
        long: Use verbose formatting if True
        
    Returns:
        The formatted string
        
    Raises:
        MSError: If ms_value is not a finite number
        
    Examples:
        >>> format(172800000)
        '2d'
        >>> format(172800000, long=True)
        '2 days'
        >>> format(3600000)
        '1h'
    """
    if not isinstance(ms_value, (int, float)):
        raise MSError('Value provided to ms.format() must be of type number.')
    
    # Check if the number is finite (not NaN, not Infinity)
    if not math.isfinite(ms_value):
        raise MSError('Value provided to ms.format() must be of type number.')
    
    return _fmt_long(ms_value) if long else _fmt_short(ms_value)


def _fmt_short(ms_value: Union[int, float]) -> str:
    """Short format for ms."""
    ms_abs = abs(ms_value)
    
    if ms_abs >= Y:
        return f"{round(ms_value / Y)}y"
    if ms_abs >= MO:
        return f"{round(ms_value / MO)}mo"
    if ms_abs >= W:
        return f"{round(ms_value / W)}w"
    if ms_abs >= D:
        return f"{round(ms_value / D)}d"
    if ms_abs >= H:
        return f"{round(ms_value / H)}h"
    if ms_abs >= M:
        return f"{round(ms_value / M)}m"
    if ms_abs >= S:
        return f"{round(ms_value / S)}s"
    return f"{int(ms_value)}ms"


def _fmt_long(ms_value: Union[int, float]) -> str:
    """Long format for ms."""
    ms_abs = abs(ms_value)
    
    if ms_abs >= Y:
        return _plural(ms_value, ms_abs, Y, 'year')
    if ms_abs >= MO:
        return _plural(ms_value, ms_abs, MO, 'month')
    if ms_abs >= W:
        return _plural(ms_value, ms_abs, W, 'week')
    if ms_abs >= D:
        return _plural(ms_value, ms_abs, D, 'day')
    if ms_abs >= H:
        return _plural(ms_value, ms_abs, H, 'hour')
    if ms_abs >= M:
        return _plural(ms_value, ms_abs, M, 'minute')
    if ms_abs >= S:
        return _plural(ms_value, ms_abs, S, 'second')
    return f"{int(ms_value)} ms"


def _plural(ms_value: Union[int, float], ms_abs: float, n: float, name: str) -> str:
    """Pluralization helper."""
    is_plural = ms_abs >= n * 1.5
    rounded = round(ms_value / n)
    return f"{rounded} {name}{'s' if is_plural else ''}"
