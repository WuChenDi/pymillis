[![PyPI version](https://badge.fury.io/py/pymillis.svg)](https://badge.fury.io/py/pymillis)
[![Python Support](https://img.shields.io/pypi/pyversions/pymillis.svg)](https://pypi.org/project/pymillis/)

# pymillis

Use this package to easily convert various time formats to milliseconds. Zero runtime dependencies.

## Installation

```bash
pip install pymillis
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add pymillis
```

## Usage

### Basic Usage

```python
from pymillis import ms

# Parse time strings to milliseconds
ms("2 days")  # 172800000
ms("1d")  # 86400000
ms("10h")  # 36000000
ms("2.5 hrs")  # 9000000
ms("2h")  # 7200000
ms("1m")  # 60000
ms("5s")  # 5000
ms("1y")  # 31557600000
ms("100")  # 100
ms("-3 days")  # -259200000
ms("-1h")  # -3600000
ms("-200")  # -200

# Format milliseconds to strings
ms(60000)  # '1m'
ms(2 * 60000)  # '2m'
ms(-3 * 60000)  # '-3m'
ms(172800000)  # '2d'

# Use long format
ms(60000, long=True)  # '1 minute'
ms(2 * 60000, long=True)  # '2 minutes'
ms(172800000, long=True)  # '2 days'
ms(ms("10 hours"), long=True)  # '10 hours'
```

### Durations

Use `parse_timedelta()` to get a `datetime.timedelta` directly:

```python
from datetime import timedelta
from pymillis import parse_timedelta

parse_timedelta("1.5s")  # timedelta(milliseconds=1500)
parse_timedelta("2h")  # timedelta(hours=2)
parse_timedelta("-1h")  # timedelta(hours=-1)
```

## API

### `ms(value, *, long=False)`

Parse or format the given value.

**Parameters:**
- `value` (str | int | float): The string or number to convert
- `long` (bool, optional): Set to `True` to use verbose formatting. Defaults to `False`.

**Returns:**
- If `value` is a string, returns milliseconds as `int` (for whole numbers) or `float` (for decimals)
- If `value` is a number, returns the formatted string

**Raises:**
- `MSError`: If value is not a non-empty string or a number

### `parse(value)`

Parse the given string and return milliseconds.

**Parameters:**
- `value` (str): A string to parse to milliseconds

**Returns:**
- `int | float`: The parsed value in milliseconds (`int` for whole numbers, `float` for decimals)

**Raises:**
- `MSError` with `code` set to:
  - `ErrorCode.INVALID_TYPE` if the value is not a string
  - `ErrorCode.EMPTY` if the string is empty
  - `ErrorCode.TOO_LONG` if the string is longer than 100 characters
  - `ErrorCode.INVALID_FORMAT` if the string is not a valid time string

```python
from pymillis import parse

parse("2h")  # 7200000
parse("1d")  # 86400000
parse("10 seconds")  # 10000
parse("-1h")  # -3600000
parse(".5ms")  # 0.5
```

### `parse_timedelta(value)`

Parse the given string and return a `datetime.timedelta`. Accepts the same input as `parse()` and raises the same errors. Negative durations are supported.

### `format(ms_value, *, long=False)`

Format the given milliseconds as a string.

**Parameters:**
- `ms_value` (int | float): Milliseconds to format
- `long` (bool, optional): Use verbose formatting if `True`

**Returns:**
- `str`: The formatted string

**Raises:**
- `MSError` with `code` set to `ErrorCode.INVALID_TYPE` for non-numbers, or `ErrorCode.NOT_FINITE` for `nan` and infinities

### `parse_strict(value)` (deprecated)

Deprecated since 2.0.0 — use `parse()` instead. It is functionally equivalent and emits a `DeprecationWarning`.

### `MSError` and `ErrorCode`

`MSError` subclasses `ValueError`, so `except ValueError` keeps working. Every instance carries a `code` attribute so failures can be handled without matching on the message text:

```python
from pymillis import ErrorCode, MSError, parse

try:
    parse("invalid")
except MSError as e:
    if e.code is ErrorCode.INVALID_FORMAT:
        print("not a valid time string")
    else:
        print(f"Error: {e}")
```

| `ErrorCode`      | Meaning                                       |
| ---------------- | --------------------------------------------- |
| `EMPTY`          | the input string is empty                     |
| `TOO_LONG`       | the input string is longer than 100 characters |
| `INVALID_FORMAT` | the input is not a valid time string          |
| `INVALID_TYPE`   | the value is not of an accepted type          |
| `NOT_FINITE`     | the value to format is `nan` or an infinity   |

### Import Options

```python
# Import main function
from pymillis import ms

# Import specific functions
from pymillis import format, parse, parse_timedelta

# Import error types
from pymillis import ErrorCode, MSError

# Import everything
from pymillis import ErrorCode, MSError, format, ms, parse, parse_timedelta
```

## Supported Time Units

- `ms`, `msec`, `msecs`, `millisecond`, `milliseconds` - Milliseconds
- `s`, `sec`, `secs`, `second`, `seconds` - Seconds
- `m`, `min`, `mins`, `minute`, `minutes` - Minutes
- `h`, `hr`, `hrs`, `hour`, `hours` - Hours
- `d`, `day`, `days` - Days
- `w`, `week`, `weeks` - Weeks
- `mo`, `month`, `months` - Months (calculated as 1/12 of a year)
- `y`, `yr`, `yrs`, `year`, `years` - Years (calculated as 365.25 days)

### Case Insensitive

All units are case-insensitive, so `1D`, `1d`, `1 Day`, `1 DAY` are all equivalent.

## Features

- 🚀 Simple and intuitive API
- 📦 Zero runtime dependencies
- 🔄 Bidirectional conversion (string ↔ milliseconds)
- ⏱️ Supports negative time values
- ⏳ `parse_timedelta()` for `datetime.timedelta` interop
- 📝 Long and short format options
- 🎯 Fully type-hinted and `py.typed`
- ✅ Structured error handling with `MSError.code`
- 🛡️ Exact arithmetic — no binary floating-point drift

## Common Use Cases

### Setting Timeouts

```python
import time
from pymillis import parse_timedelta

# Parse directly to a timedelta for time.sleep()
time.sleep(parse_timedelta("5s").total_seconds())
```

### Async Operations

```python
import asyncio
from pymillis import parse_timedelta


async def main():
    await asyncio.sleep(parse_timedelta("2s").total_seconds())
```

### Caching

```python
import time
from pymillis import ms

# Set cache expiration
cache_duration = ms("1h")
expires_at = time.time() * 1000 + cache_duration
```

### Rate Limiting

```python
from pymillis import ms

# Define rate limit window
rate_limit_window = ms("1m")
max_requests = 100
```

### Calculating Durations

```python
from pymillis import ms

# Calculate time differences
meeting_duration = ms("2h") - ms("30m")  # 5400000 ms (1.5 hours)
```

## Notes

### Precision

- **Month calculation**: 1 month = 1/12 year ≈ 30.44 days (average value)
- **Year calculation**: 1 year = 365.25 days (accounting for leap years)
- Parsing uses exact rational arithmetic, so `parse("0.1s")` is `100`, not `100.00000000000001`

### Rounding

When formatting, values are rounded to the nearest integer for the selected unit, with ties rounded away from zero (matching the JavaScript and Rust ports):

```python
ms(1500)  # '2s'  (rounded from 1.5s)
ms(2500)  # '3s'  (a tie, rounded away from zero)
ms(90000)  # '2m'  (rounded from 1.5m)
```

## Migrating from 1.x

- `MSError` now subclasses `ValueError` and carries a `code` attribute (`ErrorCode`). Existing `except MSError` and `except ValueError` handlers are unaffected.
- Formatting now rounds ties away from zero. Previously Python's banker's rounding applied, so `ms(2500)` returned `'2s'` and now returns `'3s'`.
- Parsing is now exact. Results that previously carried floating-point noise (`parse("0.1s")` → `100.00000000000001`) are now whole numbers.
- `parse_strict()` is deprecated and emits a `DeprecationWarning`; it behaves identically to `parse()`.
- `parse_timedelta()` is new: it parses straight to `datetime.timedelta`.
- Python 3.9 is no longer supported; the minimum is Python 3.10.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
make install     # create the virtualenv and install the dev dependencies
make test        # run the test suite with coverage
make lint        # ruff check
make fmt         # ruff format + autofix
make typecheck   # mypy
make build       # build the sdist and wheel
make lock        # upgrade the locked dependencies
```

## Related

- [millis](https://github.com/WuChenDi/rsmillis) — the Rust port

## 📜 License

[MIT](./LICENSE) License &copy; 2025-PRESENT [wudi](https://github.com/WuChenDi)
