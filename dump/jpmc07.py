import yfinance as yf
import requests
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

# Function to analyze P/E Ratio, P/B Ratio, and dividend yield against industry averages with scoring
def analyze_ratios(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi):
    # Score tracking
    score = 0
    max_score = 6  # Adjusted for 6 metrics in this example

    # P/E Ratio Analysis
    industry_pe = 10  # Placeholder industry average
    if pe_ratio and pe_ratio < industry_pe * 1.1:
        score += 1
    print("P/E Ratio indicates:", "favorable" if pe_ratio < industry_pe * 1.1 else "unfavorable")

    # P/B Ratio Analysis
    industry_pb = 1.2
    if pb_ratio and pb_ratio < industry_pb:
        score += 1
    print("P/B Ratio indicates:", "favorable" if pb_ratio < industry_pb else "unfavorable")

    # Dividend Yield & Payout Ratio Analysis
    if dividend_yield and payout_ratio:
        if dividend_yield > 0.03 and payout_ratio < 0.6:
            score += 1
    print("Dividend Yield indicates:", "favorable" if dividend_yield and dividend_yield > 0.03 and payout_ratio < 0.6 else "unfavorable")

    # Expense Ratio Analysis
    if expense_ratio and expense_ratio < 0.6:
        score += 1
    print("Expense Ratio indicates:", "favorable" if expense_ratio and expense_ratio < 0.6 else "unfavorable")

    # Interest Rate Analysis
    if interest_rate and interest_rate < 3:
        score += 1
    print("Interest Rate indicates:", "favorable" if interest_rate and interest_rate < 3 else "unfavorable")

    # Inflation Analysis
    if cpi and cpi < 270:
        score += 1
    print("Inflation (CPI) indicates:", "favorable" if cpi and cpi < 270 else "unfavorable")

    # Calculate Confidence Score
    confidence_score = (score / max_score) * 100

    # Investment Advice
    print("\n--- Investment Decision Summary ---")
    if confidence_score >= 70:
        print(f"Recommendation: BUY - Strong confidence ({confidence_score:.2f}%) based on current metrics.")
    elif 50 <= confidence_score < 70:
        print(f"Recommendation: HOLD/REVIEW - Moderate confidence ({confidence_score:.2f}%), but some factors are unfavorable.")
    else:
        print(f"Recommendation: SELL/AVOID - Low confidence ({confidence_score:.2f}%). Conditions are currently unfavorable for buying.")

    return confidence_score

# Run the program
if __name__ == "__main__":
    ticker = "JPM"
    stock_data, pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio = get_financial_data(ticker)

    # Use your Alpha Vantage API key
    api_key = 'S2MVB1J2Z0CAAM9H'
    interest_rate, cpi = get_economic_indicators(api_key)

    # Analyze ratios and make a recommendation
    confidence_score = analyze_ratios(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi)
