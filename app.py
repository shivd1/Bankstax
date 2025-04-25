import streamlit as st
import pandas as pd
from loan_safety_scoring import calculate_loan_safety

# Load data
@st.cache_data
def load_boa_data():
    df = pd.read_excel("Line items.xlsx", sheet_name="Sheet1", header=1, engine="openpyxl")
    df.columns = [
        "Company", "PAT", "Depreciation", "Liabilities", "Cash",
        "Assets", "CurrentAssets", "CurrentLiabilities", "Receivables",
        "MarketableSecurities", "CoreDeposits", "TotalDeposits", "Loans",
        "NPAs", "Tier1Capital", "Tier2Capital", "RWA"
    ]
    df.set_index("Company", inplace=True)
    return df.loc["Bank of America"]

# Compute ratios
def get_ratios(row):
    return {
        "Core Deposits to Total Deposits": row["CoreDeposits"] / row["TotalDeposits"],
        "NPAs to Total Loans": row["NPAs"] / row["Loans"],
        "Liquidity Ratio": row["CurrentAssets"] / row["CurrentLiabilities"],
        "Capital Adequacy Ratio": row["Tier1Capital"] / row["RWA"],
        "Solvency Ratio": (row["Assets"] - row["Liabilities"]) / row["Assets"],
        "Loans to Deposit Ratio": row["Loans"] / row["TotalDeposits"]
    }

# UI
st.set_page_config(page_title="Loan Safety Analyzer", layout="wide")
st.title("🏦 Loan Safety Analyzer")
st.write("Evaluate how safe it is to lend to **Bank of America** based on key ratios.")

if st.button("📊 Analyze Loan Safety"):
    row = load_boa_data()
    ratios = get_ratios(row)
    graded, final_grade = calculate_loan_safety(ratios)

    st.subheader("🔎 Ratio Breakdown:")
    for metric, details in graded.items():
        st.markdown(f"**{metric}**: `{details['value']:.2%}` — {details['label']}")

    st.markdown("---")
    st.subheader("🏁 Final Grade:")
    st.markdown(f"# {final_grade}")
