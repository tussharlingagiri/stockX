from flask import Flask, render_template, send_file
import matplotlib
matplotlib.use('Agg')

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Function to get basic financial data for JP Morgan
def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    
    # Gather stock price data and basic statistics
    stock_price_data = stock.history(period="1y")
    pe_ratio = stock.info.get('trailingPE')
    pb_ratio = stock.info.get('priceToBook')
    dividend_yield = stock.info.get('dividendYield')
    
    return stock_price_data, pe_ratio, pb_ratio, dividend_yield

# Function to create a plot of the stock price
def plot_stock_price(stock_price_data):
    plt.figure(figsize=(10, 5))
    plt.plot(stock_price_data.index, stock_price_data['Close'], label='Close Price')
    plt.title("JP Morgan Chase (JPM) Stock Price - Last 1 Year")
    plt.xlabel("Date")
    plt.ylabel("Close Price (USD)")
    plt.legend()
    plt.grid(True)

    # Save the plot as an image file
    plt.savefig('static/jpm_stock_price.png')
    plt.close()  # Close the plot to free memory

@app.route('/')
def home():
    ticker = "JPM"
    stock_data, pe_ratio, pb_ratio, dividend_yield = get_financial_data(ticker)
    plot_stock_price(stock_data)

    # Calculate the investment decision
    decision = ""
    if pe_ratio < 15 and dividend_yield > 2:
        decision = "BUY"
    else:
        decision = "HOLD"

    return render_template('index.html', pe_ratio=pe_ratio, pb_ratio=pb_ratio,
                           dividend_yield=dividend_yield*100, decision=decision)

@app.route('/plot')
def plot():
    return send_file('static/jpm_stock_price.png')

if __name__ == "__main__":
    # Ensure the static directory exists
    if not os.path.exists('static'):
        os.makedirs('static')

    app.run(host='127.0.0.1', port=5000, debug=True)
