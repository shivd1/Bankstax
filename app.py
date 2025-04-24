import streamlit as st
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

# Initialize Alpha Vantage API key and TimeSeries object
API_KEY = 'your_actual_api_key_here'  # Replace with your valid API key
ts = TimeSeries(key=API_KEY, output_format='pandas')

# Function to fetch financial data for a given ticker
def fetch_financial_data(ticker):
    try:
        # Example: Get daily adjusted close data
        data, meta_data = ts.get_daily_adjusted(symbol=ticker, outputsize='compact')
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")

# Streamlit app layout
st.title('Bank Financial Data Viewer')
selected_bank = st.selectbox('Select a Bank', ['JP Morgan Chase'])

if selected_bank:
    st.subheader(f'Financial Data for {selected_bank}')
    ticker = 'JPM'  # Replace with the ticker symbol for the selected bank
    financial_data = fetch_financial_data(ticker)

    # Display financial data
    if financial_data is not None:
        st.write(financial_data)
