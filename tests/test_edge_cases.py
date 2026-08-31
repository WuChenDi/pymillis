"""Edge-case regression tests for the 2.0.0 release."""

from datetime import timedelta

import pytest

from pymillis import ErrorCode, MSError, format, parse, parse_timedelta


class TestErrorCodes:
    """Test the machine-readable error codes on MSError"""

    def test_should_be_a_value_error(self):
        """should subclass ValueError so existing handlers keep working"""
        with pytest.raises(ValueError):
            parse("nope")

    def test_should_report_empty(self):
        """should report ErrorCode.EMPTY for an empty string"""
        with pytest.raises(MSError) as exc:
            parse("")
        assert exc.value.code is ErrorCode.EMPTY

    def test_should_report_too_long(self):
        """should report ErrorCode.TOO_LONG past 100 characters"""
        with pytest.raises(MSError) as exc:
            parse("1" * 101)
        assert exc.value.code is ErrorCode.TOO_LONG

    def test_should_accept_exactly_100_characters(self):
        """should accept a string of exactly 100 characters"""
        assert parse("1" * 98 + "ms") == int("1" * 98)

    def test_should_report_invalid_format(self):
        """should report ErrorCode.INVALID_FORMAT for a non-time string"""
        with pytest.raises(MSError) as exc:
            parse("invalid")
        assert exc.value.code is ErrorCode.INVALID_FORMAT

    def test_should_report_invalid_format_for_unknown_unit(self):
        """should report ErrorCode.INVALID_FORMAT for an unknown unit"""
        with pytest.raises(MSError) as exc:
            parse("1 fortnight")
        assert exc.value.code is ErrorCode.INVALID_FORMAT

    def test_should_report_invalid_type(self):
        """should report ErrorCode.INVALID_TYPE for a non-string"""
        with pytest.raises(MSError) as exc:
            parse(None)  # type: ignore[arg-type]
        assert exc.value.code is ErrorCode.INVALID_TYPE

    def test_should_report_not_finite(self):
        """should report ErrorCode.NOT_FINITE for nan and infinities"""
        for value in (float("nan"), float("inf"), float("-inf")):
            with pytest.raises(MSError) as exc:
                format(value)
            assert exc.value.code is ErrorCode.NOT_FINITE


class TestParseStrictness:
    """Test inputs the parser must reject"""

    def test_should_reject_a_trailing_newline(self):
        """should reject a trailing newline"""
        with pytest.raises(MSError):
            parse("1m\n")

    def test_should_reject_a_trailing_dot(self):
        """should reject a number ending in a dot"""
        with pytest.raises(MSError):
            parse("5.")

    def test_should_reject_trailing_whitespace(self):
        """should reject trailing whitespace"""
        with pytest.raises(MSError):
            parse("1m ")


class TestParseExactness:
    """Test that parsing is free of binary floating-point drift"""

    def test_should_return_an_exact_int_for_repeating_binary_fractions(self):
        """should not leak float error into the result"""
        result = parse("0.1s")
        assert result == 100
        assert isinstance(result, int)

    def test_should_keep_sub_millisecond_precision(self):
        """should return a float when the result is not whole"""
        assert parse(".5ms") == 0.5


class TestRoundingParity:
    """Test that ties round away from zero, matching the JS and Rust ports"""

    def test_should_round_ties_away_from_zero(self):
        """should round .5 up rather than to even"""
        assert format(2500) == "3s"
        assert format(-2500) == "-3s"
        assert format(1500) == "2s"
        assert format(90000) == "2m"

    def test_should_round_ties_away_from_zero_in_long_form(self):
        """should round the same way in long format"""
        assert format(2500, long=True) == "3 seconds"
        assert format(-2500, long=True) == "-3 seconds"


class TestParseTimedelta:
    """Test parse_timedelta(string)"""

    def test_should_parse_fractional_seconds(self):
        """should parse fractional seconds"""
        assert parse_timedelta("1.5s") == timedelta(milliseconds=1500)

    def test_should_parse_hours(self):
        """should parse hours"""
        assert parse_timedelta("2h") == timedelta(hours=2)

    def test_should_support_negative_durations(self):
        """should support negative durations, unlike the Rust port"""
        assert parse_timedelta("-1h") == timedelta(hours=-1)

    def test_should_propagate_parse_errors(self):
        """should propagate errors from parse()"""
        with pytest.raises(MSError) as exc:
            parse_timedelta("invalid")
        assert exc.value.code is ErrorCode.INVALID_FORMAT
