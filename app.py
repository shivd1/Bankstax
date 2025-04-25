import streamlit as st
import pandas as pd
from scoring_engine import calculate_grades

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("Line items (2).xlsx", sheet_name="Sheet1", header=1, engine="openpyxl")
    df.columns = [
        "Company", "PAT", "Depreciation", "Liabilities", "Cash",
        "Assets", "CurrentAssets", "CurrentLiabilities", "Receivables",
        "MarketableSecurities", "CoreDeposits", "TotalDeposits", "Loans",
        "NPAs", "Tier1Capital", "Tier2Capital", "RWA"
    ]
    df.set_index("Company", inplace=True)
    return df

# Extract ratios for one bank
def compute_ratios(row):
    return {
        "Core Deposits to Total Deposits": row["CoreDeposits"] / row["TotalDeposits"],
        "NPAs to Total Loans": row["NPAs"] / row["Loans"],
        "Liquidity Ratio": row["CurrentAssets"] / row["CurrentLiabilities"],
        "Capital Adequacy Ratio": row["Tier1Capital"] / row["RWA"],
        "Solvency Ratio": (row["Assets"] - row["Liabilities"]) / row["Assets"],
        "Loans to Deposit Ratio": row["Loans"] / row["TotalDeposits"]
    }

# App UI
st.set_page_config(page_title="Bank Loan Safety Analyzer", layout="wide")
st.title("🏦 2-Tier Bank Safety Analyzer")
st.write("Get separate safety grades for **Depositors** and **Corporate Borrowers**.")

# Load and select bank
df = load_data()
bank_list = df.index.tolist()
selected_bank = st.selectbox("Select a bank to evaluate:", bank_list)

if st.button("🔍 Analyze"):
    row = df.loc[selected_bank]
    ratios = compute_ratios(row)
    results = calculate_grades(ratios)

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 Depositor Safety View")
        st.markdown(f"**Grade**: {results['depositor']['grade']}")
        for metric, info in results["depositor"]["details"].items():
            st.markdown(f"""
            - **{metric}**: `{info['value']:.2%}`  
              → {info['reason']}
            """)

    with col2:
        st.subheader("🏢 Corporate Lending View")
        st.markdown(f"**Grade**: {results['borrower']['grade']}")
        for metric, info in results["borrower"]["details"].items():
            st.markdown(f"""
            - **{metric}**: `{info['value']:.2%}`  
              → {info['reason']}
            """)

    st.markdown("---")
    st.success("Analysis complete. Adjust Excel data to refresh grades across banks.")
