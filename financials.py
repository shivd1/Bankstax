import yfinance as yf

# Define ticker symbols
tickers = ['JPM', 'BAC', 'AXP', 'MS', 'TD', 'CFG', 'GS']

# Fetch data from Yahoo Finance
financial_data = yf.download(tickers, start="2020-01-01", end="2025-01-01")

# Display the data
print(financial_data)
