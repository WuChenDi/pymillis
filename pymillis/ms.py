"""pymillis.ms - Core milliseconds conversion functionality."""

from __future__ import annotations

import math
import re
import warnings
from datetime import timedelta
from enum import Enum
from fractions import Fraction
from typing import Final, overload

__all__ = [
    "ErrorCode",
    "MSError",
    "format",
    "ms",
    "parse",
    "parse_strict",
    "parse_timedelta",
]

#: A number of milliseconds: ``int`` for whole values, ``float`` otherwise.
Milliseconds = int | float

# Time unit constants in milliseconds. A year is 365.25 days and a month is
# a twelfth of that; both land on whole milliseconds, so all constants are
# exact integers.
S: Final = 1000
M: Final = S * 60
H: Final = M * 60
D: Final = H * 24
W: Final = D * 7
Y: Final = int(D * 365.25)
MO: Final = Y // 12


class ErrorCode(str, Enum):
    """Machine-readable reason attached to every :class:`MSError`."""

    EMPTY = "empty"
    TOO_LONG = "too_long"
    INVALID_FORMAT = "invalid_format"
    INVALID_TYPE = "invalid_type"
    NOT_FINITE = "not_finite"


class MSError(ValueError):
    """Raised when a value cannot be parsed or formatted.

    Subclasses :class:`ValueError`, so existing ``except ValueError`` handlers
    keep working. The :attr:`code` attribute identifies the failure without
    matching on the message text.
    """

    def __init__(self, message: str, code: ErrorCode) -> None:
        super().__init__(message)
        self.code = code


# Numeric part, optional whitespace, optional alphabetic unit. Always applied
# with fullmatch(), so trailing characters are rejected.
_PATTERN: Final = re.compile(r"(?P<value>-?\d*\.?\d+)\s*(?P<unit>[A-Za-z]*)")

_UNIT_MULTIPLIERS: Final[dict[str, int]] = {
    "years": Y, "year": Y, "yrs": Y, "yr": Y, "y": Y,
    "months": MO, "month": MO, "mo": MO,
    "weeks": W, "week": W, "w": W,
    "days": D, "day": D, "d": D,
    "hours": H, "hour": H, "hrs": H, "hr": H, "h": H,
    "minutes": M, "minute": M, "mins": M, "min": M, "m": M,
    "seconds": S, "second": S, "secs": S, "sec": S, "s": S,
    "milliseconds": 1, "millisecond": 1, "msecs": 1, "msec": 1, "ms": 1,
}  # fmt: skip

# Formatting tiers from largest to smallest: threshold in milliseconds, short
# suffix, and long unit name.
_UNITS: Final[tuple[tuple[int, str, str], ...]] = (
    (Y, "y", "year"),
    (MO, "mo", "month"),
    (W, "w", "week"),
    (D, "d", "day"),
    (H, "h", "hour"),
    (M, "m", "minute"),
    (S, "s", "second"),
)

_MAX_LENGTH: Final = 100

# Long format switches to the plural at 1.5 units.
_PLURAL_THRESHOLD: Final = Fraction(3, 2)


@overload
def ms(value: str) -> Milliseconds: ...


@overload
def ms(value: int | float, *, long: bool = False) -> str: ...


def ms(value: str | int | float, *, long: bool = False) -> Milliseconds | str:
    """Parse or format the given value.

    Args:
        value: The string to parse, or the number of milliseconds to format.
        long: Set to ``True`` to use verbose formatting. Defaults to ``False``.

    Returns:
        Milliseconds when ``value`` is a string, a formatted string when it is
        a number.

    Raises:
        MSError: If ``value`` is neither a string nor a number, or cannot be
            converted.

    Examples:
        >>> ms('2 days')
        172800000
        >>> ms(172800000)
        '2d'
        >>> ms(172800000, long=True)
        '2 days'
    """
    if isinstance(value, str):
        return parse(value)
    if isinstance(value, (int, float)):
        return format(value, long=long)
    raise MSError(
        f"Value provided to ms() must be a string or number. value={value!r}",
        ErrorCode.INVALID_TYPE,
    )


def parse(value: str) -> Milliseconds:
    """Parse the given string and return milliseconds.

    Args:
        value: A string to parse to milliseconds, e.g. ``'2h'`` or ``'1 day'``.

    Returns:
        The parsed value in milliseconds, as an ``int`` when it is a whole
        number and a ``float`` otherwise.

    Raises:
        MSError: If ``value`` is not a string, is empty, exceeds 100
            characters, or is not a valid time string.

    Examples:
        >>> parse('2d')
        172800000
        >>> parse('1.5 hours')
        5400000
        >>> parse('.5ms')
        0.5
    """
    if not isinstance(value, str):
        raise MSError(
            f"Value provided to ms.parse() must be a string. value={value!r}",
            ErrorCode.INVALID_TYPE,
        )
    if not value:
        raise MSError(
            "Value provided to ms.parse() must not be empty.",
            ErrorCode.EMPTY,
        )
    if len(value) > _MAX_LENGTH:
        raise MSError(
            f"Value provided to ms.parse() must not exceed {_MAX_LENGTH} characters.",
            ErrorCode.TOO_LONG,
        )

    match = _PATTERN.fullmatch(value)
    if match is None:
        raise MSError(
            f"Invalid time string format. value={value!r}",
            ErrorCode.INVALID_FORMAT,
        )

    unit = match["unit"].lower() or "ms"
    multiplier = _UNIT_MULTIPLIERS.get(unit)
    if multiplier is None:
        raise MSError(
            f'Unknown unit "{unit}" provided to ms.parse(). value={value!r}',
            ErrorCode.INVALID_FORMAT,
        )

    # Fraction keeps the arithmetic exact: 0.1 * 1000 is 100, not 100.000000001.
    result = Fraction(match["value"]) * multiplier
    return result.numerator if result.denominator == 1 else float(result)


def parse_strict(value: str) -> Milliseconds:
    """Parse the given string and return milliseconds.

    .. deprecated:: 2.0.0
        Use :func:`parse` instead; this is an alias kept for API compatibility.
    """
    warnings.warn(
        "parse_strict() is deprecated since 2.0.0; use parse() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return parse(value)


def parse_timedelta(value: str) -> timedelta:
    """Parse the given string and return a :class:`datetime.timedelta`.

    Accepts the same input as :func:`parse`. Unlike the Rust counterpart,
    negative durations are supported because ``timedelta`` can represent them.

    Args:
        value: A string to parse.

    Returns:
        The parsed duration.

    Raises:
        MSError: The same errors as :func:`parse`.

    Examples:
        >>> parse_timedelta('1.5s')
        datetime.timedelta(seconds=1, microseconds=500000)
        >>> parse_timedelta('-1h')
        datetime.timedelta(days=-1, seconds=82800)
    """
    return timedelta(milliseconds=parse(value))


def format(ms_value: int | float, *, long: bool = False) -> str:
    """Format the given milliseconds as a string.

    Args:
        ms_value: Milliseconds to format.
        long: Use verbose formatting if ``True``.

    Returns:
        The formatted string.

    Raises:
        MSError: If ``ms_value`` is not a finite number.

    Examples:
        >>> format(172800000)
        '2d'
        >>> format(172800000, long=True)
        '2 days'
        >>> format(3600000)
        '1h'
    """
    if not isinstance(ms_value, (int, float)):
        raise MSError(
            f"Value provided to ms.format() must be of type number. value={ms_value!r}",
            ErrorCode.INVALID_TYPE,
        )
    if not math.isfinite(ms_value):
        raise MSError(
            f"Value provided to ms.format() must be finite. value={ms_value!r}",
            ErrorCode.NOT_FINITE,
        )

    value = Fraction(ms_value)
    value_abs = abs(value)
    for threshold, suffix, name in _UNITS:
        if value_abs >= threshold:
            count = _round_half_away(value / threshold)
            if not long:
                return f"{count}{suffix}"
            plural = "s" if value_abs >= threshold * _PLURAL_THRESHOLD else ""
            return f"{count} {name}{plural}"

    count = _round_half_away(value)
    return f"{count} ms" if long else f"{count}ms"


def _round_half_away(value: Fraction) -> int:
    """Round to the nearest integer, with ties going away from zero.

    Matches the rounding of the JavaScript and Rust implementations; Python's
    built-in :func:`round` would round ties to even instead.
    """
    numerator, denominator = value.numerator, value.denominator
    sign = -1 if numerator < 0 else 1
    return sign * ((2 * abs(numerator) + denominator) // (2 * denominator))
