[![PyPI version](https://badge.fury.io/py/pymillis.svg)](https://badge.fury.io/py/pymillis)
[![Python Support](https://img.shields.io/pypi/pyversions/pymillis.svg)](https://pypi.org/project/pymillis/)

# pymillis

Use this package to easily convert various time formats to milliseconds.

## Installation

```bash
pip install pymillis
```

## Usage

### Basic Usage

```python
from pymillis import ms

# Parse time strings to milliseconds
ms('2 days')          # 172800000
ms('1d')              # 86400000
ms('10h')             # 36000000
ms('2.5 hrs')         # 9000000
ms('2h')              # 7200000
ms('1m')              # 60000
ms('5s')              # 5000
ms('1y')              # 31557600000
ms('100')             # 100
ms('-3 days')         # -259200000
ms('-1h')             # -3600000
ms('-200')            # -200

# Format milliseconds to strings
ms(60000)             # '1m'
ms(2 * 60000)         # '2m'
ms(-3 * 60000)        # '-3m'
ms(172800000)         # '2d'

# Use long format
ms(60000, long=True)           # '1 minute'
ms(2 * 60000, long=True)       # '2 minutes'
ms(172800000, long=True)       # '2 days'
ms(ms('10 hours'), long=True)  # '10 hours'
```

### API

#### `ms(value, *, long=False)`

Parse or format the given value.

**Parameters:**
- `value` (str | int | float): The string or number to convert
- `long` (bool, optional): Set to `True` to use verbose formatting. Defaults to `False`.

**Returns:**
- If `value` is a string, returns milliseconds as `int` (for whole numbers) or `float` (for decimals)
- If `value` is a number, returns formatted string as `str`

**Raises:**
- `MSError`: If value is not a non-empty string or a number

#### `parse(value)`

Parse the given string and return milliseconds.

**Parameters:**
- `value` (str): A string to parse to milliseconds

**Returns:**
- `int | float`: The parsed value in milliseconds (int for whole numbers, float for decimals)

**Raises:**
- `MSError`: If the string is invalid or cannot be parsed

#### `format(ms_value, *, long=False)`

Format the given milliseconds as a string.

**Parameters:**
- `ms_value` (int | float): Milliseconds to format
- `long` (bool, optional): Use verbose formatting if `True`

**Returns:**
- `str`: The formatted string

**Raises:**
- `MSError`: If ms_value is not a finite number

### Import Options

```python
# Import main function
from pymillis import ms

# Import specific functions
from pymillis import parse, format, parse_strict

# Import exception
from pymillis import MSError

# Import everything
from pymillis import ms, parse, format, MSError
```

## Supported Time Units

### Short Format

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
- 📦 Zero dependencies
- 🔄 Bidirectional conversion (string ↔ milliseconds)
- ⏱️ Supports negative time values
- 📝 Long and short format options
- 🎯 Type hints for better IDE support
- ✅ Comprehensive error handling

## Common Use Cases

### Setting Timeouts

```python
import time
from pymillis import ms

# Convert to seconds for time.sleep()
timeout = ms('5s') / 1000
time.sleep(timeout)
```

### Caching

```python
import time
from pymillis import ms

# Set cache expiration
cache_duration = ms('1h')
expires_at = time.time() * 1000 + cache_duration
```

### Rate Limiting

```python
from pymillis import ms

# Define rate limit window
rate_limit_window = ms('1m')
max_requests = 100
```

### Calculating Durations

```python
from pymillis import ms

# Calculate time differences
meeting_duration = ms('2h') - ms('30m')  # 5400000 ms (1.5 hours)
```

## Error Handling

The library raises `MSError` for invalid inputs:

```python
from pymillis import ms, MSError

# Invalid format
try:
    ms('invalid')
except MSError as e:
    print(f"Error: {e}")

# Non-finite number
try:
    ms(float('nan'))
except MSError as e:
    print(f"Error: {e}")

# Empty string
try:
    ms('')
except MSError as e:
    print(f"Error: {e}")

# String too long (>100 characters)
try:
    ms('a' * 101)
except MSError as e:
    print(f"Error: {e}")
```

## Notes

### Precision

- **Month calculation**: 1 month = 1/12 year ≈ 30.44 days (average value)
- **Year calculation**: 1 year = 365.25 days (accounting for leap years)

### Rounding

When formatting, values are rounded to the nearest integer for the selected unit:

```python
ms(1500)              # '2s'  (rounded from 1.5s)
ms(90000)             # '2m'  (rounded from 1.5m)
```

## 📜 License

[MIT](./LICENSE) License &copy; 2025-PRESENT [wudi](https://github.com/WuChenDi)
