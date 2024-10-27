import matplotlib.pyplot as plt

def plot_stock_price(stock_price_data, ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(stock_price_data.index, stock_price_data['Close'], label='Close Price', color='blue')
    plt.title(f"{ticker} Stock Price - Last 5 Years")
    plt.xlabel("Date")
    plt.ylabel("Close Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.show()
