import streamlit as st
import pandas as pd

# Define the list of banks and their ticker symbols
banks = {
    'JP Morgan Chase': 'JPM',
    'Bank of America': 'BAC',
    'American Express': 'AXP',
    'Morgan Stanley': 'MS',
    'TD Bank': 'TD',
    'Citizens Bank': 'CFG',
    'Goldman Sachs': 'GS'
}

# Function to fetch financial data
def fetch_financial_data(bank_name, ticker):
    # You can replace this with actual data retrieval code
    financial_data = {
        'Bank Name': bank_name,
        'Ticker': ticker,
        'Cash Holdings': 'To be retrieved',
        'Credit Rating': 'To be retrieved',
        'Liquidity Ratios': 'To be retrieved',
        'NPAs': 'To be retrieved',
        'Capital Adequacy Ratio': 'To be retrieved',
        'Debt to Income Ratio': 'To be retrieved',
        'Debt Ratio': 'To be retrieved',
        'Tier 1 Capital Ratio': 'To be retrieved'
    }
    return financial_data

# Streamlit app layout
st.title('Bank Financial Data Viewer')
selected_bank = st.selectbox('Select a Bank', list(banks.keys()))

if selected_bank:
    st.subheader(f'Financial Data for {selected_bank}')
    ticker = banks[selected_bank]
    financial_data = fetch_financial_data(selected_bank, ticker)

    # Display financial data
    df = pd.DataFrame([financial_data])
    st.write(df)

    st.markdown("---")
    st.write("Data source: Replace 'To be retrieved' with actual financial metrics retrieved from data providers or APIs.")

import streamlit as st
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

# Initialize Alpha Vantage API key and TimeSeries object
API_KEY = 'KA5TG8VK6M12Y4F5'
ts = TimeSeries(key=API_KEY, output_format='pandas')

# Function to fetch financial data for a given bank
def fetch_financial_data(bank_ticker):
    try:
        # Example: Fetch data for JP Morgan Chase (JPM)
        data, meta_data = ts.get_quote_endpoint(symbol=bank_ticker)
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")

# Streamlit app layout
st.title('Bank Financial Data Viewer')

# Select box for bank selection
selected_bank = st.selectbox('Select a Bank', ['JP Morgan Chase', 'Bank of America', 'American Express', 'Morgan Stanley', 'TD Bank', 'Citizens Bank', 'Goldman Sachs'])

if selected_bank:
    st.subheader(f'Financial Data for {selected_bank}')

    # Map bank names to their ticker symbols
    bank_tickers = {
        'JP Morgan Chase': 'JPM',
        'Bank of America': 'BAC',
        'American Express': 'AXP',
        'Morgan Stanley': 'MS',
        'TD Bank': 'TD',
        'Citizens Bank': 'CFG',
        'Goldman Sachs': 'GS'
    }

    # Fetch financial data based on selected bank
    bank_ticker = bank_tickers.get(selected_bank)
    financial_data = fetch_financial_data(bank_ticker)

    # Display financial data
    if financial_data is not None:
        st.write(financial_data)
