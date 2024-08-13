# filename: stock_plot.py
import yfinance as yf
import matplotlib.pyplot as plt

# Download stock data for TSLA and META
tesla = yf.Ticker("TSLA")
meta = yf.Ticker("META")

# Get the current date
from datetime import date
current_date = date.today()

# Extract year from the current date
year = current_date.year

# Get YTD data for both stocks
tesla_ytd = tesla.history(start=f"{year}-01-01", end=current_date.strftime("%Y-%m-%d"))
meta_ytd = meta.history(start=f"{year}-01-01", end=current_date.strftime("%Y-%m-%d"))

# Calculate stock price gains YTD
tesla_gains = (tesla_ytd['Close'].iloc[-1] - tesla_ytd['Close'].iloc[0]) / tesla_ytd['Close'].iloc[0]
meta_gains = (meta_ytd['Close'].iloc[-1] - meta_ytd['Close'].iloc[0]) / meta_ytd['Close'].iloc[0]

# Print stock price gains YTD
print(f"TSLA's YTD gain: {tesla_gains*100:.2f}%")
print(f"META's YTD gain: {meta_gains*100:.2f}%")

# Plot TSLA and META stock prices over the year
plt.figure(figsize=(10,6))
plt.plot(tesla_ytd['Close'], label='TSLA')
plt.plot(meta_ytd['Close'], label='META')
plt.title('Stock Price Over the Year')
plt.xlabel('Days')
plt.ylabel('Price (USD)')
plt.legend()
plt.savefig('stock_gains.png')