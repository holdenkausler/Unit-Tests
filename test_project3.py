import unittest
from Project3 import validate_symbol, validate_chart_type, validate_time_series, validate_date

class TestStockSymbolValidation(unittest.TestCase):
    def test_valid_symbols(self):
        self.assertTrue(validate_symbol("AAPL"))
        self.assertTrue(validate_symbol("GOOGL"))
        self.assertTrue(validate_symbol("MSFT"))
        self.assertTrue(validate_symbol("TSLA"))

    def test_invalid_symbols(self):
        self.assertFalse(validate_symbol("aapl"))
        self.assertFalse(validate_symbol("AAPL123"))
        self.assertFalse(validate_symbol("12345"))
        self.assertFalse(validate_symbol(""))
        self.assertFalse(validate_symbol("EXTRALONGSYM"))

class TestChartTypeValidation(unittest.TestCase):
    def test_valid_chart_types(self):
        self.assertTrue(validate_chart_type(1))
        self.assertTrue(validate_chart_type(2))

    def test_invalid_chart_types(self):
        self.assertFalse(validate_chart_type(0))
        self.assertFalse(validate_chart_type(3))
        self.assertFalse(validate_chart_type(5))
        self.assertFalse(validate_chart_type("1"))
        self.assertFalse(validate_chart_type("2"))
        self.assertFalse(validate_chart_type(None))
        self.assertFalse(validate_chart_type(1.5))

class TestTimeSeriesValidation(unittest.TestCase):
    def test_valid_time_series(self):
        self.assertTrue(validate_time_series(1))
        self.assertTrue(validate_time_series(2))
        self.assertTrue(validate_time_series(3))
        self.assertTrue(validate_time_series(4))

    def test_invalid_time_series(self):
        self.assertFalse(validate_time_series(0))
        self.assertFalse(validate_time_series(5))
        self.assertFalse(validate_time_series(-1))
        self.assertFalse(validate_time_series("1"))
        self.assertFalse(validate_time_series(None))
        self.assertFalse(validate_time_series(2.5))

class TestStartDateValidation(unittest.TestCase):
    def test_valid_start_dates(self):
        self.assertTrue(validate_date("2024-11-13"))
        self.assertTrue(validate_date("2000-01-01"))
        self.assertTrue(validate_date("1999-12-31"))

    def test_invalid_start_dates(self):
        self.assertFalse(validate_date("13-11-2024"))  
        self.assertFalse(validate_date("2024/11/13"))  
        self.assertFalse(validate_date("2024-13-11"))
        self.assertFalse(validate_date("2024-11-32"))    
        self.assertFalse(validate_date("20241113"))    
        self.assertFalse(validate_date(""))

if __name__ == "__main__":
    unittest.main()