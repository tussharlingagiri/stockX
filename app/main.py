from financial_data import get_financial_data
from economic_indicators import get_economic_indicators
from plot_stock import plot_stock_price
from llm_recommendation import get_recommendation

def main():
    ticker = "JPM"
    stock_data, pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio = get_financial_data(ticker)
    plot_stock_price(stock_data, ticker)

    interest_rate, cpi = get_economic_indicators()

    recommendation = get_recommendation(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi)
    print("LLM Recommendation:\n", recommendation)

if __name__ == "__main__":
    main()
