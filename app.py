import streamlit as st
from bank_data_viewer import fetch_bank_metrics

# Streamlit app layout configuration
st.set_page_config(page_title="Bank Data", layout="wide")

# Single clear header
st.title("📊 Bank of America - Financial Metrics Viewer")

# Only show Bank of America for now
selected_bank = "Bank of America"

# Button to trigger data display
if st.button("🔍 Show Bank Data"):
    metrics = fetch_bank_metrics(selected_bank)
    if metrics:
        st.subheader(f"📄 Financial Data for {selected_bank}")
        for key, value in metrics.items():
            st.write(f"**{key}**: {value:,}" if isinstance(value, (int, float)) else f"**{key}**: {value}")
    else:
        st.warning("No data found for this bank.")
