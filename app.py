import streamlit as st
import pandas as pd
from scoring_engine import calculate_grades

# Inject custom luxury CSS
def load_custom_css():
    st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #0d1b2a, #1b263b);
            color: #f0f4f8;
        }
        .block-container {
            padding-top: 3rem;
            padding-bottom: 3rem;
            max-width: 1080px;
        }
        h1, h2, h3 {
            color: #e0e6ed;
        }
        .title-box {
            background: rgba(255,255,255,0.05);
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: 0 0 25px rgba(0,0,0,0.1);
        }
        .card {
            background-color: rgba(255,255,255,0.05);
            padding: 1.2rem 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            color: #f0f4f8;
            border-left: 4px solid #2196f3;
        }
        .metric-title {
            font-weight: 600;
            font-size: 16px;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #90caf9;
        }
        .highlight-grade {
            font-size: 32px;
            font-weight: bold;
            color: #00e5ff;
            background: rgba(0,0,0,0.2);
            padding: 1rem 2rem;
            border-radius: 12px;
            margin: 1rem 0;
            display: inline-block;
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

# Compute required ratios
def compute_ratios(row):
    return {
        "Core Deposits to Total Deposits": row["CoreDeposits"] / row["TotalDeposits"],
        "NPAs to Total Loans": row["NPAs"] / row["Loans"],
        "Liquidity Ratio": row["CurrentAssets"] / row["CurrentLiabilities"],
        "Capital Adequacy Ratio": row["Tier1Capital"] / row["RWA"],
        "Solvency Ratio": (row["Assets"] - row["Liabilities"]) / row["Assets"],
        "Loans to Deposit Ratio": row["Loans"] / row["TotalDeposits"]
    }

# Set page config
st.set_page_config(page_title="Bankstax 2.0 | Risk Analyzer", layout="wide", page_icon="💼")
load_custom_css()

# --- Hero Section ---
st.markdown("<div class='title-box'><h1>💼 Bankstax 2.0</h1><h4>Your personal dual-view analyzer for banking risk & lending confidence.</h4></div>", unsafe_allow_html=True)

# --- Step 1: Role Selection ---
role = st.radio("Who are you here as?", ["💰 I’m a Depositor", "🏢 I’m a Borrower (Corporate)"])

# --- Step 2: Bank Selection ---
df = load_data()
bank_list = df.index.tolist()
selected_bank = st.selectbox("Choose a bank to evaluate:", bank_list)

if st.button("🚀 Analyze Risk"):
    row = df.loc[selected_bank]
    ratios = compute_ratios(row)
    results = calculate_grades(ratios)

    st.markdown(f"<h2>📊 Analysis for: {selected_bank}</h2>", unsafe_allow_html=True)

    if "Depositor" in role:
        st.markdown("<h3>💰 Depositor Safety Score</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='highlight-grade'>{results['depositor']['grade']}</div>", unsafe_allow_html=True)
        for metric, info in results["depositor"]["details"].items():
            st.markdown(f"""
            <div class='card'>
                <div class='metric-title'>{metric}</div>
                <div class='metric-value'>{info['value']:.2%}</div>
                <div>{info['reason']}</div>
            </div>
            """, unsafe_allow_html=True)

    elif "Borrower" in role:
        st.markdown("<h3>🏢 Corporate Lending Strength</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='highlight-grade'>{results['borrower']['grade']}</div>", unsafe_allow_html=True)
        for metric, info in results["borrower"]["details"].items():
            st.markdown(f"""
            <div class='card'>
                <div class='metric-title'>{metric}</div>
                <div class='metric-value'>{info['value']:.2%}</div>
                <div>{info['reason']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("You can switch your role or bank to explore other views.")
