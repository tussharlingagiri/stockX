import yfinance as yf
from src.logger import logger

def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    stock_price_data = stock.history(period="5y")

    # Retrieve each metric and log errors if None
    pe_ratio = stock.info.get('trailingPE')
    pb_ratio = stock.info.get('priceToBook')
    dividend_yield = stock.info.get('dividendYield')
    payout_ratio = stock.info.get('payoutRatio')
    net_income = stock.info.get('netIncomeToCommon')
    revenue = stock.info.get('totalRevenue')
    expense_ratio = (net_income / revenue) if revenue else None

    # Null checks with logging
    if pe_ratio is None:
        logger.error(f"{ticker} P/E ratio retrieval failed.")
    if pb_ratio is None:
        logger.error(f"{ticker} P/B ratio retrieval failed.")
    if dividend_yield is None:
        logger.error(f"{ticker} Dividend Yield retrieval failed.")
    if payout_ratio is None:
        logger.error(f"{ticker} Payout Ratio retrieval failed.")
    if net_income is None:
        logger.error(f"{ticker} Net Income retrieval failed.")
    if revenue is None:
        logger.error(f"{ticker} Revenue retrieval failed.")
    if expense_ratio is None:
        logger.error(f"{ticker} Expense Ratio calculation failed (possible division by zero).")

    return stock_price_data, pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio
