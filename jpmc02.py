import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

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

# Function to get current economic indicators
def get_economic_indicators():
    # Use static CSV links to get interest rates and CPI data
    interest_rate_url = 'https://fred.stlouisfed.org/data/FDTR.txt'
    cpi_url = 'https://fred.stlouisfed.org/data/CPIAUCNS.txt'
    
    # Fetch interest rates
    try:
        interest_rate_data = pd.read_csv(interest_rate_url, sep='\t', header=None, skiprows=9)
        current_interest_rate = interest_rate_data.iloc[-1, 1]  # Get the most recent interest rate
        print(f"Current Federal Funds Rate: {current_interest_rate:.2f}%")
    except Exception as e:
        print(f"Error fetching interest rates: {e}")
        current_interest_rate = None

    # Fetch CPI data
    try:
        cpi_data = pd.read_csv(cpi_url, sep='\t', header=None, skiprows=9)
        current_cpi = cpi_data.iloc[-1, 1]  # Get the most recent CPI
        print(f"Current Consumer Price Index (CPI): {current_cpi:.2f}")
    except Exception as e:
        print(f"Error fetching CPI data: {e}")
        current_cpi = None

    return current_interest_rate, current_cpi

# Function to analyze P/E Ratio, P/B Ratio, and dividend yield against hypothetical industry averages
def analyze_ratios(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi):
    industry_pe = 10  # Placeholder for a more accurate average
    industry_pb = 1.2  # Placeholder for the industry price-to-book average
    
    # Valuation Analysis
    buy_recommendation = False
    if pe_ratio < industry_pe and pb_ratio < industry_pb:
        print("JPM is currently undervalued relative to the industry average (P/E and P/B are low).")
        buy_recommendation = True
    else:
        print("JPM is trading at or above the industry average P/E and P/B ratios.")

    # Dividend Analysis
    if dividend_yield and payout_ratio:
        if dividend_yield > 0.03 and payout_ratio < 0.6:
            print("The dividend yield is strong and sustainable (low payout ratio).")
            buy_recommendation = True
        else:
            print("The dividend yield is either low or the payout ratio is high, suggesting caution.")
    else:
        print("Dividend information is incomplete.")

    # Expense Ratio (Operational Efficiency) Analysis
    if expense_ratio and expense_ratio < 0.6:
        print("JP Morgan's expense ratio indicates effective cost management.")
        buy_recommendation = True
    else:
        print("JP Morgan has a high expense ratio, suggesting higher operational costs.")

    # Economic Condition Recommendations
    print("\n--- Summary for Investment Decision ---")
    if interest_rate is not None:
        if interest_rate < 3:
            print("When Interest Rates Are Rising Moderately: This can be a good time to buy JP Morgan, as it may increase revenue through higher loan rates.")
        else:
            print("High Interest Rates: This might indicate caution due to potential impacts on loan growth.")

    if cpi is not None:
        if cpi > 270:  # Example threshold for high inflation
            print("During High Inflation: Caution is warranted, as inflationary pressures can hurt banks due to higher defaults and operating costs.")
        else:
            print("Low Inflation: This could be favorable for banks.")

    print("With a Steep Yield Curve: Positive for banks, as it signals profitable lending conditions.")
    print("With an Inverted Yield Curve: Be cautious, as it often indicates economic downturn risks, which could strain JP Morgan’s lending and default rates.")
    print("Additional Tip: Track quarterly results and forward guidance from JP Morgan's management to better understand the impact of these factors on their outlook.\n")

    return buy_recommendation

# Run the program
if __name__ == "__main__":
    ticker = "JPM"
    stock_data, pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio = get_financial_data(ticker)
    plot_stock_price(stock_data)

    # Get current economic indicators
    interest_rate, cpi = get_economic_indicators()

    # Analyze ratios and make a recommendation
    recommend = analyze_ratios(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi)
    if recommend:
        print("Recommendation: BUY - Based on current metrics, JP Morgan appears to be a good buy.")
    else:
        print("Recommendation: HOLD/REVIEW - JP Morgan may not be undervalued or have sufficient metrics to recommend a buy.")
