import os
import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# ── A. App header ──────────────────────────────────────────────────────────
st.set_page_config(page_title="Loan Provider Selector", layout="wide")
st.title("🔍 Compare Loan Offers from Top Institutions")

# ── B. Load the institutions.csv ──────────────────────────────────────────
# 1. Let user upload…
uploaded_file = st.sidebar.file_uploader("Upload institutions.csv", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not read uploaded CSV: {e}")
        st.stop()
# 2. …or fall back to a local file
elif os.path.exists("institutions.csv"):
    try:
        df = pd.read_csv("institutions.csv")
    except Exception as e:
        st.error(f"Could not read institutions.csv: {e}")
        st.stop()
# 3. If neither, stop
else:
    st.error(
        "No CSV found! Please either:\n"
        "• Upload your `institutions.csv` via the uploader above, or\n"
        "• Place `institutions.csv` in this folder and rerun."
    )
    st.stop()

# ── C. Normalize & preprocess the DataFrame ─────────────────────────────────
# 1. Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.replace(r"[^0-9A-Za-z]", "", regex=True)
)

# 2. Rename known variants
df = df.rename(columns={
    "InterestRate%": "InterestRate",
    "InterestRatePercentage": "InterestRate",
    "MaxLoanAmount$": "MaxLoanAmount"
})

# 3. Ensure numeric fields exist & cast
for col in ["InterestRate", "MaxLoanAmount", "ROE", "ROA", "NPLRatio"]:
    df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0)

# 4. Covenants → list of strings
df["Covenants"] = (
    df.get("Covenants", "")
      .fillna("")
      .astype(str)
      .apply(lambda x: x.split(";") if x else [])
)

# 5. LoanType → default "Other"
df["LoanType"] = df.get("LoanType", "Other").fillna("Other").astype(str)

# 6. Ticker → default empty
df["Ticker"] = df.get("Ticker", "").fillna("").astype(str)

# 7. Institution name → required
if "Institution" not in df.columns:
    df["Institution"] = [f"Inst {i+1}" for i in range(len(df))]

# ── D. (Optional) Fetch live metrics via yfinance ──────────────────────────
tickers = [t for t in df["Ticker"].unique() if t]
if tickers:
    @st.cache
    def fetch_metrics(tks):
        out = []
        for t in tks:
            try:
                info = yf.Ticker(t).info
                out.append({
                    "Ticker":        t,
                    "PE":            info.get("trailingPE"),
                    "DebtEquity":    info.get("debtToEquity"),
                    "ReturnOnEquity":info.get("returnOnEquity")
                })
            except Exception:
                pass
        return pd.DataFrame(out)

    metrics_df = fetch_metrics(tickers)
    if not metrics_df.empty:
        df = df.merge(metrics_df, on="Ticker", how="left")

# ── E. Sidebar filters ─────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filter Offers")

    # Interest Rate slider
    ir_min, ir_max = df["InterestRate"].min(), df["InterestRate"].max()
    if ir_min < ir_max:
        rate_min, rate_max = st.slider(
            "Interest Rate (%)",
            float(ir_min), float(ir_max),
            (float(ir_min), float(ir_max))
        )
    else:
        st.info(f"All rates = {ir_min}%.")
        rate_min = rate_max = float(ir_min)

    # Loan Amount slider
    la_min, la_max = df["MaxLoanAmount"].min(), df["MaxLoanAmount"].max()
    if la_min < la_max:
        amt_min, amt_max = st.slider(
            "Max Loan Amount ($)",
            float(la_min), float(la_max),
            (float(la_min), float(la_max))
        )
    else:
        st.info(f"All loan caps = ${la_min}.")
        amt_min = amt_max = float(la_min)

    # Loan types
    loan_types   = df["LoanType"].unique().tolist()
    chosen_types = st.multiselect("Loan Type", loan_types, default=loan_types)

    # Covenants
    all_covs     = sorted({c for covs in df["Covenants"] for c in covs})
    needed_covs  = st.multiselect("Required Covenants", all_covs, default=[])

    # Comparison metric
    metric = st.selectbox(
        "Compare by Metric",
        ["InterestRate", "PE", "DebtEquity", "ReturnOnEquity", "ROE", "NPLRatio"]
    )

# ── F. Apply filters & show table ──────────────────────────────────────────
filtered = df[
    df["InterestRate"].between(rate_min, rate_max) &
    df["MaxLoanAmount"].between(amt_min, amt_max) &
    df["LoanType"].isin(chosen_types) &
    df["Covenants"].apply(lambda covs: all(c in covs for c in needed_covs))
]

st.subheader(f"Matching Institutions: {len(filtered)}")
st.dataframe(filtered, use_container_width=True)

# ── G. Charts ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### 📊 {metric} Comparison")
    fig1 = px.bar(filtered, x="Institution", y=metric, height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### 🔍 Rate vs. Max Loan Amount")
    fig2 = px.scatter(
        filtered,
        x="InterestRate", y="MaxLoanAmount", text="Institution",
        labels={
            "InterestRate": "Interest Rate (%)",
            "MaxLoanAmount": "Max Loan Amount ($)"
        },
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)
