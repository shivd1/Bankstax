import streamlit as st
from bank_data_viewer import fetch_bank_metrics

st.set_page_config(page_title="Bank Viewer", layout="wide")
st.title("🏦 Bank Financial Data Viewer")

# Dropdown
selected_bank = st.selectbox("Select a Bank", ["Bank of America"])

if st.button("Show Data"):
    metrics = fetch_bank_metrics(selected_bank)
    if metrics:
        st.subheader(f"📊 Financial Metrics for {selected_bank}")
        for key, value in metrics.items():
            st.write(f"**{key}**: {value:,}" if isinstance(value, (int, float)) else f"**{key}**: {value}")
    else:
        st.warning("No data found for the selected bank.")
