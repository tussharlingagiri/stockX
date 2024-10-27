import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import requests

# Function to get basic financial data for JP Morgan
def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    
    # Gather stock price data and basic statistics
    stock_price_data = stock.history(period="5y")  # Last 5 years for medium-term view
    pe_ratio = stock.info.get('trailingPE')
    pb_ratio = stock.info.get('priceToBook')
    dividend_yield = stock.info.get('dividendYield')
    payout_ratio = stock.info.get('payoutRatio')  # Dividends as a % of earnings
    net_income = stock.info.get('netIncomeToCommon')
    revenue = stock.info.get('totalRevenue')
    expense_ratio = (net_income / revenue) if revenue else None
    
    # Display basic financial information
    print(f"Current P/E Ratio: {pe_ratio}")
    print(f"Current P/B Ratio: {pb_ratio}")
    print(f"Dividend Yield: {dividend_yield * 100:.2f}%" if dividend_yield else "Dividend Yield: N/A")
    print(f"Payout Ratio: {payout_ratio * 100:.2f}%" if payout_ratio else "Payout Ratio: N/A")
    print(f"Expense Ratio: {expense_ratio * 100:.2f}%" if expense_ratio else "Expense Ratio: N/A")
    
    return stock_price_data, pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio

# Function to plot stock price history for JP Morgan
def plot_stock_price(stock_price_data):
    plt.figure(figsize=(10, 5))
    plt.plot(stock_price_data.index, stock_price_data['Close'], label='Close Price', color='blue')
    plt.title("JP Morgan Chase (JPM) Stock Price - Last 5 Years")
    plt.xlabel("Date")
    plt.ylabel("Close Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Function to get current economic indicators from Alpha Vantage
def get_economic_indicators(api_key):
    # Fetch interest rates from Alpha Vantage
    interest_rate_url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&apikey={api_key}&datatype=json'
    try:
        response = requests.get(interest_rate_url)
        data = response.json()
        current_interest_rate = float(data['data'][0]['value'])  # Get the most recent interest rate
        print(f"Current Federal Funds Rate: {current_interest_rate:.2f}%")
    except Exception as e:
        print(f"Error fetching interest rates: {e}")
        current_interest_rate = None

    # Fetch CPI data from Alpha Vantage
    cpi_url = f'https://www.alphavantage.co/query?function=CPI&apikey={api_key}&datatype=json'
    try:
        response = requests.get(cpi_url)
        data = response.json()
        current_cpi = float(data['data'][0]['value'])  # Get the most recent CPI
        print(f"Current Consumer Price Index (CPI): {current_cpi:.2f}")
    except Exception as e:
        print(f"Error fetching CPI data: {e}")
        current_cpi = None

    return current_interest_rate, current_cpi

# Function to analyze P/E Ratio, P/B Ratio, dividend yield, and economic indicators for buy/sell decision
def analyze_ratios(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi):
    industry_pe = 10  # Placeholder for a more accurate average
    industry_pb = 1.2  # Placeholder for the industry price-to-book average
    
    # Valuation Analysis
    buy_recommendation = False
    sell_recommendation = False
    reasons = []

    if pe_ratio > industry_pe and pb_ratio > industry_pb:
        reasons.append("JPM appears overvalued relative to the industry average (high P/E and P/B ratios).")
        sell_recommendation = True
    elif pe_ratio < industry_pe and pb_ratio < industry_pb:
        reasons.append("JPM appears undervalued relative to the industry average (low P/E and P/B ratios).")
        buy_recommendation = True
    else:
        reasons.append("JPM is trading near the industry average P/E and P/B ratios.")

    # Dividend Analysis
    if dividend_yield and payout_ratio:
        if dividend_yield < 0.02 or payout_ratio > 0.7:
            reasons.append("The dividend yield is low, or the payout ratio is high, suggesting potential cash flow strain.")
            sell_recommendation = True
        else:
            reasons.append("The dividend yield is strong, and the payout ratio is sustainable.")
            buy_recommendation = True
    else:
        reasons.append("Dividend information is incomplete.")

    # Expense Ratio (Operational Efficiency) Analysis
    if expense_ratio and expense_ratio > 0.6:
        reasons.append("JPM has a high expense ratio, indicating higher operational costs.")
        sell_recommendation = True
    else:
        reasons.append("JPM's expense ratio indicates effective cost management.")
        buy_recommendation = True

    # Economic Condition Recommendations
    if interest_rate is not None:
        if interest_rate > 3:
            reasons.append("High interest rates indicate caution due to potential impacts on loan growth and overall profitability.")
            sell_recommendation = True
        elif interest_rate < 3:
            reasons.append("Moderate interest rates may favor bank profits from higher loan rates.")
            buy_recommendation = True

    if cpi is not None:
        if cpi > 270:  # Example threshold for high inflation
            reasons.append("High inflation could lead to higher defaults and operational costs, affecting profitability.")
            sell_recommendation = True
        else:
            reasons.append("Low inflation may create favorable conditions for banks.")
            buy_recommendation = True

    print("\n--- Investment Decision Summary ---")
    for reason in reasons:
        print(f"- {reason}")

    if sell_recommendation and buy_recommendation:
        print("\nMixed signals detected. Current indicators suggest reviewing both positive and negative metrics carefully before making a final decision.")
    elif sell_recommendation:
        print("Recommendation: SELL - Current indicators suggest it may be prudent to sell JP Morgan stock.")
    elif buy_recommendation:
        print("Recommendation: BUY - Based on current metrics, JP Morgan appears to be a favorable buy.")
    else:
        print("Recommendation: HOLD/REVIEW - JP Morgan may not have sufficient metrics to recommend a buy or sell at this time.")
    
    return buy_recommendation, sell_recommendation

# Run the program
if __name__ == "__main__":
    ticker = "JPM"
    stock_data, pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio = get_financial_data(ticker)
    plot_stock_price(stock_data)

    # Use your Alpha Vantage API key
    api_key = 'S2MVB1J2Z0CAAM9H'
    interest_rate, cpi = get_economic_indicators(api_key)

    # Analyze ratios and make a recommendation
    buy_recommendation, sell_recommendation = analyze_ratios(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi)
