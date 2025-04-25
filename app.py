import streamlit as st
from bank_data_viewer import fetch_bank_metrics

# Streamlit page setup
st.set_page_config(page_title="Bank Insights", layout="wide")

# Main title
st.markdown("<h1 style='text-align: center; color: navy;'>🏦 Bank Financial Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Access key financial metrics for leading institutions</h4>", unsafe_allow_html=True)
st.markdown("---")

# Focused on Bank of America for now
selected_bank = "Bank of America"

# Centered button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📊 View Data for Bank of America"):
        metrics = fetch_bank_metrics(selected_bank)

        if metrics:
            st.success(f"Showing financial data for {selected_bank}")

            # Divide into two columns for readability
            left, right = st.columns(2)
            items = list(metrics.items())
            midpoint = len(items) // 2

            with left:
                for key, value in items[:midpoint]:
                    st.markdown(f"**{key}**: {value:,}" if isinstance(value, (int, float)) else f"**{key}**: {value}")

            with right:
                for key, value in items[midpoint:]:
                    st.markdown(f"**{key}**: {value:,}" if isinstance(value, (int, float)) else f"**{key}**: {value}")
        else:
            st.error("No financial data found.")
if score_total >= 7: grade = "🇩 D (Risky)"
    else: grade = "🇫 F (Unsafe)"

    return graded, grade
