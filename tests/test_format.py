"""Tests for format function"""

import pytest
from pyms import format


class TestFormatNumberLong:
    """Test format(number, long=True)"""
    
    def test_should_not_throw_an_error(self):
        """should not throw an error"""
        format(500, long=True)  # Should not raise
    
    def test_should_support_milliseconds(self):
        """should support milliseconds"""
        assert format(500, long=True) == '500 ms'
        assert format(-500, long=True) == '-500 ms'
    
    def test_should_support_seconds(self):
        """should support seconds"""
        assert format(1000, long=True) == '1 second'
        assert format(1200, long=True) == '1 second'
        assert format(10000, long=True) == '10 seconds'
        
        assert format(-1000, long=True) == '-1 second'
        assert format(-1200, long=True) == '-1 second'
        assert format(-10000, long=True) == '-10 seconds'
    
    def test_should_support_minutes(self):
        """should support minutes"""
        assert format(60 * 1000, long=True) == '1 minute'
        assert format(60 * 1200, long=True) == '1 minute'
        assert format(60 * 10000, long=True) == '10 minutes'
        
        assert format(-1 * 60 * 1000, long=True) == '-1 minute'
        assert format(-1 * 60 * 1200, long=True) == '-1 minute'
        assert format(-1 * 60 * 10000, long=True) == '-10 minutes'
    
    def test_should_support_hours(self):
        """should support hours"""
        assert format(60 * 60 * 1000, long=True) == '1 hour'
        assert format(60 * 60 * 1200, long=True) == '1 hour'
        assert format(60 * 60 * 10000, long=True) == '10 hours'
        
        assert format(-1 * 60 * 60 * 1000, long=True) == '-1 hour'
        assert format(-1 * 60 * 60 * 1200, long=True) == '-1 hour'
        assert format(-1 * 60 * 60 * 10000, long=True) == '-10 hours'
    
    def test_should_support_days(self):
        """should support days"""
        assert format(1 * 24 * 60 * 60 * 1000, long=True) == '1 day'
        assert format(1 * 24 * 60 * 60 * 1200, long=True) == '1 day'
        assert format(6 * 24 * 60 * 60 * 1000, long=True) == '6 days'
        
        assert format(-1 * 1 * 24 * 60 * 60 * 1000, long=True) == '-1 day'
        assert format(-1 * 1 * 24 * 60 * 60 * 1200, long=True) == '-1 day'
        assert format(-1 * 6 * 24 * 60 * 60 * 1000, long=True) == '-6 days'
    
    def test_should_support_weeks(self):
        """should support weeks"""
        assert format(1 * 7 * 24 * 60 * 60 * 1000, long=True) == '1 week'
        assert format(2 * 7 * 24 * 60 * 60 * 1000, long=True) == '2 weeks'
        
        assert format(-1 * 1 * 7 * 24 * 60 * 60 * 1000, long=True) == '-1 week'
        assert format(-1 * 2 * 7 * 24 * 60 * 60 * 1000, long=True) == '-2 weeks'
    
    def test_should_support_months(self):
        """should support months"""
        assert format(30.4375 * 24 * 60 * 60 * 1000, long=True) == '1 month'
        assert format(30.4375 * 24 * 60 * 60 * 1200, long=True) == '1 month'
        assert format(30.4375 * 24 * 60 * 60 * 10000, long=True) == '10 months'
        
        assert format(-1 * 30.4375 * 24 * 60 * 60 * 1000, long=True) == '-1 month'
        assert format(-1 * 30.4375 * 24 * 60 * 60 * 1200, long=True) == '-1 month'
        assert format(-1 * 30.4375 * 24 * 60 * 60 * 10000, long=True) == '-10 months'
    
    def test_should_support_years(self):
        """should support years"""
        assert format(365.25 * 24 * 60 * 60 * 1000 + 1, long=True) == '1 year'
        assert format(365.25 * 24 * 60 * 60 * 1200 + 1, long=True) == '1 year'
        assert format(365.25 * 24 * 60 * 60 * 10000 + 1, long=True) == '10 years'
        
        assert format(-1 * 365.25 * 24 * 60 * 60 * 1000 - 1, long=True) == '-1 year'
        assert format(-1 * 365.25 * 24 * 60 * 60 * 1200 - 1, long=True) == '-1 year'
        assert format(-1 * 365.25 * 24 * 60 * 60 * 10000 - 1, long=True) == '-10 years'
    
    def test_should_round(self):
        """should round"""
        assert format(234234234, long=True) == '3 days'
        assert format(-234234234, long=True) == '-3 days'


class TestFormatNumber:
    """Test format(number)"""
    
    def test_should_not_throw_an_error(self):
        """should not throw an error"""
        format(500)  # Should not raise
    
    def test_should_support_milliseconds(self):
        """should support milliseconds"""
        assert format(500) == '500ms'
        assert format(-500) == '-500ms'
    
    def test_should_support_seconds(self):
        """should support seconds"""
        assert format(1000) == '1s'
        assert format(10000) == '10s'
        
        assert format(-1000) == '-1s'
        assert format(-10000) == '-10s'
    
    def test_should_support_minutes(self):
        """should support minutes"""
        assert format(60 * 1000) == '1m'
        assert format(60 * 10000) == '10m'
        
        assert format(-1 * 60 * 1000) == '-1m'
        assert format(-1 * 60 * 10000) == '-10m'
    
    def test_should_support_hours(self):
        """should support hours"""
        assert format(60 * 60 * 1000) == '1h'
        assert format(60 * 60 * 10000) == '10h'
        
        assert format(-1 * 60 * 60 * 1000) == '-1h'
        assert format(-1 * 60 * 60 * 10000) == '-10h'
    
    def test_should_support_days(self):
        """should support days"""
        assert format(24 * 60 * 60 * 1000) == '1d'
        assert format(24 * 60 * 60 * 6000) == '6d'
        
        assert format(-1 * 24 * 60 * 60 * 1000) == '-1d'
        assert format(-1 * 24 * 60 * 60 * 6000) == '-6d'
    
    def test_should_support_weeks(self):
        """should support weeks"""
        assert format(1 * 7 * 24 * 60 * 60 * 1000) == '1w'
        assert format(2 * 7 * 24 * 60 * 60 * 1000) == '2w'
        
        assert format(-1 * 1 * 7 * 24 * 60 * 60 * 1000) == '-1w'
        assert format(-1 * 2 * 7 * 24 * 60 * 60 * 1000) == '-2w'
    
    def test_should_support_months(self):
        """should support months"""
        assert format(30.4375 * 24 * 60 * 60 * 1000) == '1mo'
        assert format(30.4375 * 24 * 60 * 60 * 1200) == '1mo'
        assert format(30.4375 * 24 * 60 * 60 * 10000) == '10mo'
        
        assert format(-1 * 30.4375 * 24 * 60 * 60 * 1000) == '-1mo'
        assert format(-1 * 30.4375 * 24 * 60 * 60 * 1200) == '-1mo'
        assert format(-1 * 30.4375 * 24 * 60 * 60 * 10000) == '-10mo'
    
    def test_should_support_years(self):
        """should support years"""
        assert format(365.25 * 24 * 60 * 60 * 1000 + 1) == '1y'
        assert format(365.25 * 24 * 60 * 60 * 1200 + 1) == '1y'
        assert format(365.25 * 24 * 60 * 60 * 10000 + 1) == '10y'
        
        assert format(-1 * 365.25 * 24 * 60 * 60 * 1000 - 1) == '-1y'
        assert format(-1 * 365.25 * 24 * 60 * 60 * 1200 - 1) == '-1y'
        assert format(-1 * 365.25 * 24 * 60 * 60 * 10000 - 1) == '-10y'
    
    def test_should_round(self):
        """should round"""
        assert format(234234234) == '3d'
        assert format(-234234234) == '-3d'


class TestFormatInvalidInputs:
    """Test format(invalid inputs)"""
    
    def test_should_throw_error_when_format_empty_string(self):
        """should throw an error, when format("")"""
        with pytest.raises(Exception):
            format('') # type: ignore
    
    def test_should_throw_error_when_format_undefined(self):
        """should throw an error, when format(undefined)"""
        with pytest.raises(Exception):
            format(None) # type: ignore
    
    def test_should_throw_error_when_format_null(self):
        """should throw an error, when format(null)"""
        with pytest.raises(Exception):
            format(None) # type: ignore
    
    def test_should_throw_error_when_format_list(self):
        """should throw an error, when format([])"""
        with pytest.raises(Exception):
            format([]) # type: ignore
    
    def test_should_throw_error_when_format_dict(self):
        """should throw an error, when format({})"""
        with pytest.raises(Exception):
            format({}) # type: ignore
    
    def test_should_throw_error_when_format_nan(self):
        """should throw an error, when format(NaN)"""
        with pytest.raises(Exception):
            format(float('nan'))
    
    def test_should_throw_error_when_format_infinity(self):
        """should throw an error, when format(Infinity)"""
        with pytest.raises(Exception):
            format(float('inf'))
    
    def test_should_throw_error_when_format_negative_infinity(self):
        """should throw an error, when format(-Infinity)"""
        with pytest.raises(Exception):
            format(float('-inf'))
