import unittest
import pandas as pd
import numpy as np
from pychow.chow_test import ChowTest

class TestChowTest(unittest.TestCase):
    def setUp(self):
        # Sample dataset
        self.data = pd.DataFrame({
            'x': np.arange(1, 21),
            'y': np.concatenate([np.arange(1, 11), np.arange(21, 31)])
        })
    
    def test_valid_chow_test(self):
        # Test a valid Chow test
        result = ChowTest.chow_test(self.data, 10, dependent_var='y', independent_vars=['x'])
        self.assertIn("Chow Test Statistic", result)
        self.assertIn("P-value", result)
        self.assertTrue(result["Chow Test Statistic"] > 0)
        self.assertTrue(0 <= result["P-value"] <= 1)
    
    def test_invalid_data_type(self):
        # Test with invalid data type
        with self.assertRaises(ValueError):
            ChowTest.chow_test("not a dataframe", 10, dependent_var='y', independent_vars=['x'])
    
    def test_invalid_breakpoint(self):
        # Test with invalid breakpoint
        with self.assertRaises(ValueError):
            ChowTest.chow_test(self.data, -1, dependent_var='y', independent_vars=['x'])
    
    def test_missing_dependent_variable(self):
        # Test with missing dependent variable
        with self.assertRaises(ValueError):
            ChowTest.chow_test(self.data, 10, dependent_var='z', independent_vars=['x'])
    
    def test_missing_independent_variable(self):
        # Test with missing independent variable
        with self.assertRaises(ValueError):
            ChowTest.chow_test(self.data, 10, dependent_var='y', independent_vars=['z'])

if __name__ == '__main__':
    unittest.main()
