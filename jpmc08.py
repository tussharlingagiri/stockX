import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json

# Set your Hugging Face token
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

# Define the model and the Hugging Face API URL
model_name = "gpt2"  # You can choose a different model from Hugging Face
api_url = f"https://api-inference.huggingface.co/models/{model_name}"

# Create headers with your token
headers = {
    "Authorization": f"Bearer {os.environ['HUGGINGFACEHUB_API_TOKEN']}",
}

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

# Function to get current economic indicators from Alpha Vantage with caching
def get_economic_indicators(api_key):
    cache_file = 'economic_indicators_cache.json'
    
    # Check if the cache file exists
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
            return cache.get('interest_rate'), cache.get('cpi')

    # Fetch interest rate data
    interest_rate_url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&apikey={api_key}&datatype=json'
    try:
        response = requests.get(interest_rate_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        current_interest_rate = float(data['data'][0]['value']) if 'data' in data and data['data'] else None
    except Exception as e:
        print(f"Error fetching interest rate: {e}")
        current_interest_rate = None

    # Fetch CPI data
    cpi_url = f'https://www.alphavantage.co/query?function=CPI&apikey={api_key}&datatype=json'
    try:
        response = requests.get(cpi_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        current_cpi = float(data['data'][0]['value']) if 'data' in data and data['data'] else None
    except Exception as e:
        print(f"Error fetching CPI: {e}")
        current_cpi = None

    # Save the data to cache if valid
    with open(cache_file, 'w') as f:
        json.dump({'interest_rate': current_interest_rate, 'cpi': current_cpi}, f)

    return current_interest_rate, current_cpi

# Function to analyze metrics and get recommendations from Hugging Face model
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
        "Based on these financial metrics, explain whether to buy or not, and which metrics should be considered for buy/sell thresholds."
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 150,
        },
    }

    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        print("Error:", response.status_code, response.text)
        return None

# Run the program
if __name__ == "__main__":
    ticker = "JPM"
    stock_data, pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio = get_financial_data(ticker)
    plot_stock_price(stock_data)

    api_key = 'XM14CD2Y9TOP177V'  # Alpha Vantage API key

    interest_rate, cpi = get_economic_indicators(api_key)

    recommendation = get_recommendation(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi)
    print(recommendation)
