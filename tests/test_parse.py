"""Tests for parse function"""

import pytest
from pyms import parse


class TestParseString:
    """Test parse(string)"""
    
    def test_should_not_throw_an_error(self):
        """should not throw an error"""
        parse('1m')  # Should not raise
    
    def test_should_preserve_ms(self):
        """should preserve ms"""
        assert parse('100') == 100
    
    def test_should_convert_from_m_to_ms(self):
        """should convert from m to ms"""
        assert parse('1m') == 60000
    
    def test_should_convert_from_h_to_ms(self):
        """should convert from h to ms"""
        assert parse('1h') == 3600000
    
    def test_should_convert_d_to_ms(self):
        """should convert d to ms"""
        assert parse('2d') == 172800000
    
    def test_should_convert_w_to_ms(self):
        """should convert w to ms"""
        assert parse('3w') == 1814400000
    
    def test_should_convert_s_to_ms(self):
        """should convert s to ms"""
        assert parse('1s') == 1000
    
    def test_should_convert_ms_to_ms(self):
        """should convert ms to ms"""
        assert parse('100ms') == 100
    
    def test_should_convert_y_to_ms(self):
        """should convert y to ms"""
        assert parse('1y') == 31557600000
    
    def test_should_work_with_ms(self):
        """should work with ms"""
        assert parse('1.5h') == 5400000
    
    def test_should_work_with_multiple_spaces(self):
        """should work with multiple spaces"""
        assert parse('1   s') == 1000
    
    def test_should_return_nan_if_invalid(self):
        """should return NaN if invalid"""
        with pytest.raises(Exception):
            parse('☃')
        with pytest.raises(Exception):
            parse('10-.5')
        with pytest.raises(Exception):
            parse('foo')
    
    def test_should_be_case_insensitive(self):
        """should be case-insensitive"""
        assert parse('53 YeArS') == 1672552800000
        assert parse('53 WeEkS') == 32054400000
        assert parse('53 DaYS') == 4579200000
        assert parse('53 HoUrs') == 190800000
        assert parse('53 MiLliSeCondS') == 53
    
    def test_should_work_with_numbers_starting_with_dot(self):
        """should work with numbers starting with ."""
        assert parse('.5ms') == 0.5
    
    def test_should_work_with_negative_integers(self):
        """should work with negative integers"""
        assert parse('-100ms') == -100
    
    def test_should_work_with_negative_decimals(self):
        """should work with negative decimals"""
        assert parse('-1.5h') == -5400000
        assert parse('-10.5h') == -37800000
    
    def test_should_work_with_negative_decimals_starting_with_dot(self):
        """should work with negative decimals starting with "." """
        assert parse('-.5h') == -1800000


class TestParseLongString:
    """Test parse(long string)"""
    
    def test_should_not_throw_an_error(self):
        """should not throw an error"""
        parse('53 milliseconds')  # Should not raise
    
    def test_should_convert_milliseconds_to_ms(self):
        """should convert milliseconds to ms"""
        assert parse('53 milliseconds') == 53
    
    def test_should_convert_msecs_to_ms(self):
        """should convert msecs to ms"""
        assert parse('17 msecs') == 17
    
    def test_should_convert_sec_to_ms(self):
        """should convert sec to ms"""
        assert parse('1 sec') == 1000
    
    def test_should_convert_from_min_to_ms(self):
        """should convert from min to ms"""
        assert parse('1 min') == 60000
    
    def test_should_convert_from_hr_to_ms(self):
        """should convert from hr to ms"""
        assert parse('1 hr') == 3600000
    
    def test_should_convert_days_to_ms(self):
        """should convert days to ms"""
        assert parse('2 days') == 172800000
    
    def test_should_convert_weeks_to_ms(self):
        """should convert weeks to ms"""
        assert parse('1 week') == 604800000
    
    def test_should_convert_months_to_ms(self):
        """should convert months to ms"""
        assert parse('1 month') == 2629800000
    
    def test_should_convert_years_to_ms(self):
        """should convert years to ms"""
        assert parse('1 year') == 31557600000
    
    def test_should_work_with_decimals(self):
        """should work with decimals"""
        assert parse('1.5 hours') == 5400000
    
    def test_should_work_with_negative_integers(self):
        """should work with negative integers"""
        assert parse('-100 milliseconds') == -100
    
    def test_should_work_with_negative_decimals(self):
        """should work with negative decimals"""
        assert parse('-1.5 hours') == -5400000
    
    def test_should_work_with_negative_decimals_starting_with_dot(self):
        """should work with negative decimals starting with "." """
        assert parse('-.5 hr') == -1800000


class TestParseInvalidInputs:
    """Test parse(invalid inputs)"""
    
    def test_should_throw_error_when_parse_empty_string(self):
        """should throw an error, when parse("")"""
        with pytest.raises(Exception):
            parse('')
    
    def test_should_throw_error_when_parse_long_string(self):
        """should throw an error, when parseStrict("...>100 length string...")"""
        with pytest.raises(Exception):
            parse('▲' * 101)
    
    def test_should_throw_error_when_parse_undefined(self):
        """should throw an error, when parse(undefined)"""
        with pytest.raises(Exception):
            parse(None) # type: ignore
    
    def test_should_throw_error_when_parse_null(self):
        """should throw an error, when parse(null)"""
        with pytest.raises(Exception):
            parse(None) # type: ignore
    
    def test_should_throw_error_when_parse_list(self):
        """should throw an error, when parse([])"""
        with pytest.raises(Exception):
            parse([]) # type: ignore
    
    def test_should_throw_error_when_parse_dict(self):
        """should throw an error, when parse({})"""
        with pytest.raises(Exception):
            parse({}) # type: ignore
    
    def test_should_throw_error_when_parse_nan(self):
        """should throw an error, when parse(NaN)"""
        with pytest.raises(Exception):
            parse(float('nan')) # type: ignore
    
    def test_should_throw_error_when_parse_infinity(self):
        """should throw an error, when parse(Infinity)"""
        with pytest.raises(Exception):
            parse(float('inf')) # type: ignore
    
    def test_should_throw_error_when_parse_negative_infinity(self):
        """should throw an error, when parse(-Infinity)"""
        with pytest.raises(Exception):
            parse(float('-inf')) # type: ignore
