import pandas as pd

# Load and parse Excel data
def load_excel_data():
    file_path = "Line items.xlsx"  # Adjust if needed
    df = pd.read_excel(file_path, sheet_name="Sheet1", header=1)
    df.columns = [
        "Company", "PAT", "Depreciation", "Liabilities", "Cash",
        "Assets", "CurrentAssets", "CurrentLiabilities", "Receivables",
        "MarketableSecurities", "CoreDeposits", "TotalDeposits", "Loans",
        "NPAs", "Tier1Capital", "Tier2Capital", "RWA"
    ]
    return df.set_index("Company")

# Fetch data for a specific bank
def fetch_bank_metrics(bank_name):
    df = load_excel_data()
    if bank_name in df.index:
        return df.loc[bank_name].to_dict()
    else:
        return None
