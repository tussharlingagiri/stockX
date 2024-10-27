import yfinance as yf
import matplotlib.pyplot as plt
import requests

# Function to get basic financial data for JP Morgan
def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    stock_price_data = stock.history(period="5y")
    pe_ratio = stock.info.get('trailingPE')
    pb_ratio = stock.info.get('priceToBook')
    dividend_yield = stock.info.get('dividendYield')
    payout_ratio = stock.info.get('payoutRatio')
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

# Function to get economic indicators from Alpha Vantage
def get_economic_indicators(api_key):
    interest_rate_url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&apikey={api_key}&datatype=json'
    try:
        response = requests.get(interest_rate_url)
        data = response.json()
        current_interest_rate = float(data['data'][0]['value'])
        print(f"Current Federal Funds Rate: {current_interest_rate:.2f}%")
    except Exception as e:
        print(f"Error fetching interest rates: {e}")
        current_interest_rate = None

    cpi_url = f'https://www.alphavantage.co/query?function=CPI&apikey={api_key}&datatype=json'
    try:
        response = requests.get(cpi_url)
        data = response.json()
        current_cpi = float(data['data'][0]['value'])
        print(f"Current Consumer Price Index (CPI): {current_cpi:.2f}")
    except Exception as e:
        print(f"Error fetching CPI data: {e}")
        current_cpi = None

    return current_interest_rate, current_cpi

# Function to analyze and give clear guidance on buying/selling
def analyze_and_advise(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi):
    industry_pe = 10  
    industry_pb = 1.2  
    advice = "HOLD"

    # Valuation Analysis
    if pe_ratio > industry_pe or pb_ratio > industry_pb:
        print("Current P/E and P/B ratios indicate overvaluation compared to the industry.")
        print("Consider buying again if P/E ratio falls below the industry average by 10% or aligns with it.")
    else:
        print("P/E and P/B ratios are favorable for buying.")
        advice = "BUY"

    # Dividend Analysis
    if dividend_yield and payout_ratio:
        if dividend_yield > 0.03 and payout_ratio < 0.6:
            print("Dividend yield and payout ratio are strong, indicating sustainable returns.")
            if advice == "HOLD":
                advice = "REVIEW"
        else:
            print("Caution: Dividend yield is either low or the payout ratio is high.")
            print("Consider re-evaluating when dividend yield exceeds 3% with a payout ratio under 60%.")

    # Expense Ratio Analysis
    if expense_ratio and expense_ratio < 0.6:
        print("Low expense ratio: effective cost management.")
    else:
        print("High expense ratio could indicate higher operational costs.")

    # Economic Indicators Recommendations
    if interest_rate and cpi:
        if interest_rate > 3:
            print("High interest rates: exercise caution due to potential impacts on loan growth.")
            print("Consider buying again when interest rates are under 3%.")
        if cpi > 270:
            print("High inflation could lead to increased default rates.")
            print("Consider buying again if inflation stabilizes under CPI = 270.")
    else:
        print("Economic indicators incomplete; proceed based on available metrics.")

    # Final Recommendation
    if advice == "BUY":
        print("\nRecommendation: BUY - JP Morgan is a favorable investment based on current metrics.")
    elif advice == "REVIEW":
        print("\nRecommendation: REVIEW - JP Morgan has some positive metrics. Monitor quarterly results.")
    else:
        print("\nRecommendation: HOLD - Current market conditions suggest waiting before buying.")

    return advice

# Run the program
if __name__ == "__main__":
    ticker = "JPM"
    stock_data, pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio = get_financial_data(ticker)

    # Use Alpha Vantage API key
    api_key = 'S2MVB1J2Z0CAAM9H'
    interest_rate, cpi = get_economic_indicators(api_key)

    # Analyze and advise
    analyze_and_advise(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi)
