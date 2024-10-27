import unittest
from src.economic_indicators import get_economic_indicators

class TestEconomicIndicators(unittest.TestCase):
    def test_get_economic_indicators(self):
        interest_rate, cpi = get_economic_indicators()

        self.assertIsNotNone(interest_rate, "Interest Rate should not be None.")
        self.assertIsNotNone(cpi, "CPI should not be None.")

if __name__ == '__main__':
    unittest.main()
