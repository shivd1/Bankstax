import pandas as pd

def fetch_bank_metrics(bank_name):
    file_path = "Line items.xlsx"
    df = pd.read_excel(file_path, sheet_name="Sheet1", header=1, engine="openpyxl")

    df.columns = [
        "Company", "PAT", "Depreciation", "Liabilities", "Cash",
        "Assets", "CurrentAssets", "CurrentLiabilities", "Receivables",
        "MarketableSecurities", "CoreDeposits", "TotalDeposits", "Loans",
        "NPAs", "Tier1Capital", "Tier2Capital", "RWA"
    ]

    df.set_index("Company", inplace=True)
    if bank_name in df.index:
        return df.loc[bank_name].to_dict()
    else:
        return None
