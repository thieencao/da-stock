import requests
import pandas as pd
from time import sleep

# ============================
# CONFIG
# ============================
COUNTRY = "VNM"
START = 2020
END = 2025

# World Bank Indicator Codes
INDICATORS = {
    "GDP": "NY.GDP.MKTP.CD",
    "CPI": "FP.CPI.TOTL.ZG",
    "Unemployment": "SL.UEM.TOTL.ZS",
    "InterestRate": "FR.INR.RINR",          # Real Interest Rate
    "ExchangeRate": "PA.NUS.FCRF",          # VND per USD
    "RetailSales": "NE.CON.PRVT.KD.ZG"      # Proxy: Household consumption growth
}

# ============================
# FUNCTION WITH RETRY
# ============================
def get_wb(indicator, country):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
    params = {"format": "json", "per_page": 2000}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    for retry in range(5):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=20)
            if r.status_code == 200:
                data = r.json()[1]  # Data section
                df = pd.json_normalize(data)
                df = df[["date", "value"]].rename(columns={"date": "year"})
                df["year"] = df["year"].astype(int)
                return df
        except Exception as e:
            print(f"Retry {retry+1}/5 for {indicator} due to error: {e}")
            sleep(2)

    print(f"Failed to fetch {indicator}")
    return pd.DataFrame(columns=["year", "value"])

# ============================
# CRAWL ALL DATA
# ============================
dfs = []

for name, code in INDICATORS.items():
    print(f"Fetching {name}...")
    df = get_wb(code, COUNTRY)
    df = df[(df["year"] >= START) & (df["year"] <= END)]
    df = df.rename(columns={"value": name})
    dfs.append(df)

# ============================
# MERGE INTO ONE TABLE
# ============================
df_final = dfs[0]

for df in dfs[1:]:
    df_final = df_final.merge(df, on="year", how="left")

df_final = df_final.sort_values("year").reset_index(drop=True)

print(df_final)

# SAVE CSV
df_final.to_csv("vietnam_macro_2020_2025.csv", index=False)
print("\nSaved to vietnam_macro_2020_2025.csv")
