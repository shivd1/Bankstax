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

