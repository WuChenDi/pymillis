# pyms

Milliseconds conversion utility - Python port of the popular JavaScript [ms](https://github.com/vercel/ms) library.

Convert between milliseconds and human-readable time strings with ease.

## Installation

```bash
pip install pyms
```

## Usage

### Basic Usage

```python
from pyms import ms

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
- If `value` is a string, returns milliseconds as `int`
- If `value` is a number, returns formatted string

**Raises:**
- `MSError`: If value is not a non-empty string or a number

#### `parse(value)`

Parse the given string and return milliseconds.

**Parameters:**
- `value` (str): A string to parse to milliseconds

**Returns:**
- `int`: The parsed value in milliseconds

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
from pyms import ms

# Import specific functions
from pyms import parse, format, parse_strict

# Import exception
from pyms import MSError

# Import everything
from pyms import ms, parse, format, MSError
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

## Error Handling

The library raises `MSError` for invalid inputs:

```python
from pyms import ms, MSError

try:
    ms('invalid')
except MSError as e:
    print(f"Error: {e}")

try:
    ms(float('nan'))
except MSError as e:
    print(f"Error: {e}")
```

## 📜 License

[MIT](./LICENSE) License &copy; 2025-PRESENT [wudi](https://github.com/WuChenDi)
