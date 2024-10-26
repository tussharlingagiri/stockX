import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import requests
import openai  # Ensure you have the OpenAI library installed
import time

# Set your OpenAI API key
openai.api_key = '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'

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
    interest_rate_url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&apikey={api_key}&datatype=json'
    try:
        response = requests.get(interest_rate_url)
        data = response.json()
        current_interest_rate = float(data['data'][0]['value'])
    except Exception as e:
        print(f"Error fetching interest rate: {e}")
        current_interest_rate = None

    cpi_url = f'https://www.alphavantage.co/query?function=CPI&apikey={api_key}&datatype=json'
    try:
        response = requests.get(cpi_url)
        data = response.json()
        current_cpi = float(data['data'][0]['value'])
    except Exception as e:
        print(f"Error fetching CPI: {e}")
        current_cpi = None

    return current_interest_rate, current_cpi

# Function to analyze metrics and get recommendations from LLM
def get_recommendation(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi):
    prompt = (
        f"Given the following financial metrics for JP Morgan:\n"
        f"Current P/E Ratio: {pe_ratio}\n"
        f"Current P/B Ratio: {pb_ratio}\n"
        f"Dividend Yield: {dividend_yield}\n"
        f"Payout Ratio: {payout_ratio}\n"
        f"Expense Ratio: {expense_ratio}\n"
        f"Current Federal Funds Rate: {interest_rate}\n"
        f"Current Consumer Price Index (CPI): {cpi}\n\n"
        "Provide a simple investment recommendation for someone with no finance background, "
        "indicating whether to buy, hold, or sell the stock, and the reasoning behind it."
    )

    while True:  # Loop to handle rate limit errors
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content']
        except openai.error.RateLimitError:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(60)  # Wait for 60 seconds before retrying

# Run the program
if __name__ == "__main__":
    ticker = "JPM"
    stock_data, pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio = get_financial_data(ticker)
    plot_stock_price(stock_data)

    api_key = 'S2MVB1J2Z0CAAM9H'  # Alpha Vantage API key
    interest_rate, cpi = get_economic_indicators(api_key)

    recommendation = get_recommendation(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi)
    print(recommendation)
