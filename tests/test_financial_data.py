import unittest
from src.financial_data import get_financial_data

class TestFinancialData(unittest.TestCase):
    def test_get_financial_data(self):
        stock_data, pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio = get_financial_data("JPM")

        self.assertIsNotNone(stock_data, "Stock price data should not be None.")
        self.assertIsNotNone(pe_ratio, "P/E ratio should not be None.")
        self.assertIsNotNone(pb_ratio, "P/B ratio should not be None.")
        self.assertIsNotNone(dividend_yield, "Dividend Yield should not be None.")
        self.assertIsNotNone(payout_ratio, "Payout Ratio should not be None.")
        self.assertIsNotNone(expense_ratio, "Expense Ratio should not be None.")

if __name__ == '__main__':
    unittest.main()
