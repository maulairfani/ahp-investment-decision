import streamlit as st
from utils import get_alternatives_data, get_all_tickers_and_name
import pandas as pd
import numpy as np
import json

ticker_code, name = get_all_tickers_and_name()
df_ticker = pd.DataFrame({'ticker': ticker_code, 'name': name})
df_sector = pd.read_csv("./data/sector.csv")
sectors = list(df_sector['sector'].unique())

# Load existing data from JSON files
with open("./data/temps/alternatives.json", "r") as f:
    default_ticker = json.load(f)

with open('./data/temps/sector_terpilih.json', 'r') as f:
    sector_pilihan = json.load(f)

st.title("Pilih Saham Alternatif 🎯")

# Select sectors
sector_pilihan = st.multiselect(
    'Pilih beberapa sektor saham terlebih dahulu! (max 5 agar AHP tidak terlalu kompleks)',
    sectors,
    default=sector_pilihan)

# Save selected sectors to JSON file
with open('./data/temps/sector_terpilih.json', 'w') as f:
    json.dump(sector_pilihan, f)

# Filter ticker DataFrame based on selected sectors
df_sector_pilihan = df_sector[df_sector['sector'].isin(sector_pilihan)]
df_ticker = pd.merge(df_ticker, df_sector_pilihan, on='ticker', how='inner')
ticker_code = df_ticker['ticker'].tolist()

# Function to format ticker options
def format_func(raw_options):
    data = df_ticker[df_ticker['ticker'] == raw_options]
    out = f"{data['ticker'].iloc[0]} ({data['name'].iloc[0]})"
    return out

# Select alternative tickers
try:
    alternatives = st.multiselect(
        'Pilih saham untuk alternatif AHP!',
        ticker_code, format_func=format_func,
        default=default_ticker)
except:
    alternatives = st.multiselect(
        'Pilih saham untuk alternatif AHP!',
        ticker_code, format_func=format_func)



# Save selected alternative tickers to JSON file
with open("./data/temps/alternatives.json", "w") as f:
    json.dump(alternatives, f)

# Get alternative data
df_alternatives = get_alternatives_data(alternatives)

# Write alternative data to CSV file
if len(alternatives) >= 1:
    df_alternatives.to_csv("./data/temps/Alternatives.csv", index=False)

# Generate and save sector DataFrame to Excel file
df_sector = pd.DataFrame(columns=sector_pilihan, index=sector_pilihan)
np.fill_diagonal(df_sector.values, 1)
df_sector.to_excel("./data/temps/Sector.xlsx")

# Check for incomplete data
not_eligible = df_alternatives[df_alternatives.apply(lambda x: '-' in x.values or x.isna().any(), axis=1)]['Ticker Code'].tolist()

st.write(df_alternatives)
st.write(df_alternatives.columns)

# Show message based on data completeness
if not_eligible:
    st.error(f'Silahkan ganti {not_eligible} karena data tidak lengkap!')
elif len(alternatives) < 1:
    st.warning("Silahkan pilih alternatif terlebih dahulu")
else:
    st.success('Data berhasil tersimpan!')
