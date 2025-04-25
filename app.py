import streamlit as st
import pandas as pd
from scoring_engine import calculate_grades

# Custom style for luxury UI
def load_custom_css():
    st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f4f6f9;
        }
        h1, h2, h3 {
            color: #012b4a;
        }
        .card {
            background: white;
            padding: 1.2rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }
        .metric-title {
            font-weight: 600;
            font-size: 16px;
            color: #333;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

# Load Excel data
@st.cache_data
def load_data():
    df = pd.read_excel("Line items (3).xlsx", sheet_name="Sheet1", header=1, engine="openpyxl")
    df.columns = [
        "Company", "PAT", "Depreciation", "Liabilities", "Cash",
        "Assets", "CurrentAssets", "CurrentLiabilities", "Receivables",
        "MarketableSecurities", "CoreDeposits", "TotalDeposits", "Loans",
        "NPAs", "Tier1Capital", "Tier2Capital", "RWA"
    ]
    df.set_index("Company", inplace=True)
    return df

# Ratio calculator
def compute_ratios(row):
    return {
        "Core Deposits to Total Deposits": row["CoreDeposits"] / row["TotalDeposits"],
        "NPAs to Total Loans": row["NPAs"] / row["Loans"],
        "Liquidity Ratio": row["CurrentAssets"] / row["CurrentLiabilities"],
        "Capital Adequacy Ratio": row["Tier1Capital"] / row["RWA"],
        "Solvency Ratio": (row["Assets"] - row["Liabilities"]) / row["Assets"],
        "Loans to Deposit Ratio": row["Loans"] / row["TotalDeposits"]
    }

# App Layout
st.set_page_config(page_title="Bankstax Analyzer", layout="wide", page_icon="🏦")
load_custom_css()

st.markdown("<h1 style='text-align:center;'>🏦 Bankstax Risk Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:#444;'>Choose your role: depositor or corporate borrower — and analyze risk smartly.</h4>", unsafe_allow_html=True)
st.markdown("---")

# Choose role
role = st.radio("Choose your role:", ["💰 I’m a Depositor", "🏢 I’m a Borrower (Corporate)"])

# Choose bank
df = load_data()
bank_list = df.index.tolist()
selected_bank = st.selectbox("Select a bank to analyze", bank_list)

if st.button("🔍 Run Analysis"):
    row = df.loc[selected_bank]
    ratios = compute_ratios(row)
    results = calculate_grades(ratios)

    st.markdown(f"<h2 style='color:#012b4a;'>📌 Bank Selected: {selected_bank}</h2>", unsafe_allow_html=True)

    if "Depositor" in role:
        st.markdown("<h3>💰 Depositor Safety Analysis</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'><span class='metric-title'>Grade</span><br><span class='metric-value'>{results['depositor']['grade']}</span></div>", unsafe_allow_html=True)
        for metric, info in results["depositor"]["details"].items():
            st.markdown(f"""
                <div class="card">
                <div class='metric-title'>{metric}</div>
                <div class='metric-value'>{info['value']:.2%} — {info['reason']}</div>
                </div>
            """, unsafe_allow_html=True)

    elif "Borrower" in role:
        st.markdown("<h3>🏢 Corporate Loanworthiness Analysis</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'><span class='metric-title'>Grade</span><br><span class='metric-value'>{results['borrower']['grade']}</span></div>", unsafe_allow_html=True)
        for metric, info in results["borrower"]["details"].items():
            st.markdown(f"""
                <div class="card">
                <div class='metric-title'>{metric}</div>
                <div class='metric-value'>{info['value']:.2%} — {info['reason']}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.success("Analysis complete. You can switch roles or banks for a new view.")
