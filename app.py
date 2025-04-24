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
    
#Finding gthe api key data 
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

import requests
from bs4 import BeautifulSoup

def get_sec_filings(company_name):
    # Construct the SEC EDGAR search URL
    base_url = "https://www.sec.gov"
    search_url = f"{base_url}/cgi-bin/browse-edgar"
    
    # Parameters for the search
    params = {
        "action": "getcompany",
        "CIK": "",  # Enter CIK number if known, otherwise search by company name
        "type": "",  # Enter type of document like 10-K, 10-Q, etc.
        "dateb": "",
        "owner": "exclude",
        "start": "0",
        "count": "10",  # Number of documents to retrieve
    }
    
    # Make a search request
    response = requests.get(search_url, params=params)
    
    # Parse the response content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract links to filings
    filing_links = []
    for row in soup.find_all("tr", class_="blueRow"):
        cells = row.find_all("td")
        if len(cells) > 3:
            filing_type = cells[0].text.strip()
            filing_date = cells[3].text.strip()
            filing_href = cells[1].find("a", href=True)["href"]
            filing_links.append({
                "type": filing_type,
                "date": filing_date,
                "link": base_url + filing_href
            })
    
    return filing_links

# Example usage
company_name = "JP Morgan Chase"
filings = get_sec_filings(company_name)
for filing in filings:
    print(f"{filing['type']} - {filing['date']}: {filing['link']}")
