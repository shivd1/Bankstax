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
def grade_ratio(metric, value):
    # Apply thresholds for grading each metric
    if metric == "Core Deposits to Total Deposits":
        if value > 0.80: return 3, "🟢 Safe"
        elif value >= 0.60: return 2, "🟡 Watch"
        else: return 1, "🔴 Risky"

    elif metric == "NPAs to Total Loans":
        if value < 0.02: return 3, "🟢 Safe"
        elif value <= 0.04: return 2, "🟡 Watch"
        else: return 1, "🔴 Risky"

    elif metric == "Liquidity Ratio":
        if value > 1.2: return 3, "🟢 Safe"
        elif value >= 1.0: return 2, "🟡 Watch"
        else: return 1, "🔴 Risky"

    elif metric == "Capital Adequacy Ratio":
        if value > 0.12: return 3, "🟢 Safe"
        elif value >= 0.08: return 2, "🟡 Watch"
        else: return 1, "🔴 Risky"

    elif metric == "Solvency Ratio":
        if value > 0.20: return 3, "🟢 Safe"
        elif value >= 0.10: return 2, "🟡 Watch"
        else: return 1, "🔴 Risky"

    elif metric == "Loans to Deposit Ratio":
        if 0.80 <= value <= 0.90: return 3, "🟢 Optimal"
        elif 0.70 <= value <= 1.00: return 2, "🟡 Acceptable"
        else: return 1, "🔴 Risky"

    return 0, "Invalid"

def calculate_loan_safety(data):
    graded = {}
    score_total = 0
    for metric, value in data.items():
        score, label = grade_ratio(metric, value)
        graded[metric] = {"value": value, "score": score, "label": label}
        score_total += score

    # Final grade
    if score_total >= 16: grade = "🅰️ A (Very Safe)"
    elif score_total >= 13: grade = "🅱️ B (Generally Safe)"
    elif score_total >= 10: grade = "🇨 C (Caution)"
    elif score_total >= 7: grade = "🇩 D (Risky)"
    else: grade = "🇫 F (Unsafe)"

    return graded, grade
