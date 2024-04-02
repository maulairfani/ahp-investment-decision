import pandas as pd
from tqdm import tqdm
import json
import os
import random

ri_dict = {
    "1": 0.00,
    "2": 0.00,
    "3": 0.58,
    "4": 0.90,
    "5": 1.12,
    "6": 1.24,
    "7": 1.32,
    "8": 1.41,
    "9": 1.45,
    "10": 1.49,
    "11": 1.51
}

def process(df_pairwise):
    criteria = df_pairwise.columns

    # hitung total vertikal
    list_sum = []
    for i in range(len(df_pairwise.columns)):
        list_sum.append(df_pairwise.iloc[:, i].sum())
    temp = pd.DataFrame(index=["total"], columns=df_pairwise.columns)
    temp.loc["total"] = list_sum
    df_pairwise = pd.concat([df_pairwise, temp])
    total_awal = df_pairwise.loc["total"].copy()

    # Normalisasi
    for i in range(len(df_pairwise.columns)):
        total = df_pairwise.iloc[-1, i]
        for j in range(len(df_pairwise.columns)):
            df_pairwise.iloc[j, i] = df_pairwise.iloc[j, i] / total    

    # Hitung jumlah vertikal (lagi)
    list_sum = []
    for i in range(len(df_pairwise.columns)):
        list_sum.append(df_pairwise.iloc[:-1, i].sum())
    df_pairwise.loc["total"] = list_sum

    # Hitung jumlah horizontal
    list_sum = []
    for i in range(len(df_pairwise.index)):
        list_sum.append(df_pairwise.iloc[i, :].sum())

    df_pairwise['Jumlah'] = list_sum

    # Prioritas
    df_pairwise["Prioritas"] = df_pairwise["Jumlah"] / len(criteria)

    # Eigen Values
    list_prioritas = df_pairwise["Prioritas"].iloc[:-1].to_list()
    list_total_awal = total_awal.to_list()
    eigen_values = [list_prioritas[i] * list_total_awal[i] for i in range(len(list_prioritas))]
    eigen_values.append(sum(eigen_values))
    df_pairwise["Eigen Value"] = eigen_values

    # Hitung CI
    total_eigen = df_pairwise["Eigen Value"].iloc[-1]
    ci = (total_eigen-len(criteria)) / (len(criteria)-1)

    # Hitung CR
    ri = ri_dict[str(len(criteria))]
    cr = ci/ri

    return df_pairwise, ci, ri, cr

def get_alternatives_data(alternatives):
    # Data Ratios (Kuanti)
    data_ratios = dict()

    for f in tqdm(os.listdir('data/ratios')):
        with open(f'data/ratios/{f}', 'r') as file:
            data_ratios[f[:-5]] = json.load(file)

    # Kuali
    with open('data/index.json', 'r') as file:
        index = json.load(file)

    sector = pd.read_csv('data/sector.csv')

    cols = [
        'Ticker Code',
        'Current Ratio (Quarter)',
        'Current Share Outstanding',
        'Debt to Equity Ratio (Quarter)',
        'Enterprise Value',
        'EPS Growth Streak',
        'Market Cap',
        'Net Profit Margin (TTM)(%)',
        'Current Price to Book Value',
        'Current PE Ratio (TTM)',
        'Current Price To Free Cashflow (TTM)',
        'Return on Equity (TTM)',
        'Sales Growth Streak'
    ]

    df_alternatives = pd.DataFrame(columns=cols)
    for a in alternatives:
        print(a)
        temp_dict = {
            'Ticker Code': [a]
        }
        for key in tqdm(data_ratios.keys()):
            for i in range(len(data_ratios[key])):
                if data_ratios[key][i]['company']['symbol'] == a:
                    val = data_ratios[key][i]['results'][0]['display']
                    item_name = data_ratios[key][i]['results'][0]['item']

                    temp_dict[item_name] = val
            
        temp = pd.DataFrame(temp_dict)
        df_alternatives = pd.concat([df_alternatives, temp])

    index_to_append = list()
    sector_to_append = list()
    for i in range(len(alternatives)):
        member_to = []
        for k in index:
            if alternatives[i] in index[k]:
                member_to.append(k)
        if member_to:
            out = random.choice(member_to)
            index_to_append.append(out)
        else:
            index_to_append.append('OTHERS')

        sector_to_append.append(sector[sector['ticker'] == alternatives[i]].iloc[0]['sector'])

    df_alternatives['Sector'] = sector_to_append
    df_alternatives['Index'] = index_to_append

    return df_alternatives.reset_index(drop=True)

def get_all_tickers_and_name():
    with open('data/ratios/market_cap.json', 'r') as f:
        data = json.load(f)

    ticker_code = [data[i]['company']['symbol'] for i in range(len(data))]
    company_name = [data[i]['company']['name'] for i in range(len(data))]

    return ticker_code, company_name



# Final Process
from sklearn.preprocessing import MinMaxScaler

level0 = pd.read_excel("./data/result/Level0.xlsx", index_col='Unnamed: 0')
sector = pd.read_excel("./data/result/Sector.xlsx", index_col='Unnamed: 0')
index = pd.read_excel("./data/result/Index.xlsx", index_col='Unnamed: 0')
size = pd.read_excel("./data/result/Size.xlsx", index_col='Unnamed: 0')
quality = pd.read_excel("./data/result/Quality.xlsx", index_col='Unnamed: 0')
value = pd.read_excel("./data/result/Value.xlsx", index_col='Unnamed: 0')
growth = pd.read_excel("./data/result/Growth.xlsx", index_col='Unnamed: 0')

def final_process_ahp(df):
    df["Current Share Outstanding"] = df["Current Share Outstanding"].apply(lambda x: float(x[:-2]))
    df["Enterprise Value"] = df["Enterprise Value"].apply(lambda x: float(x[:-2].replace(",", "")))
    df["Market Cap"] = df["Market Cap"].apply(lambda x: float(x[:-2].replace(",", "")))
    df["Net Profit Margin (TTM)(%)"] = df["Net Profit Margin (TTM)(%)"].apply(lambda x: float(x[:-1].replace(",", "")))
    df["Return on Equity (TTM)"] = df["Return on Equity (TTM)"].apply(lambda x: float(x[:-1].replace(",", "")))

    scaler = MinMaxScaler(feature_range=(1e-3, 1))
    float_columns = df.select_dtypes("float").columns
    df[float_columns] = scaler.fit_transform(df[float_columns])

    df['Sector'] = df['Sector'].map(sector['Prioritas'].to_dict())
    df['Index'] = df['Index'].map(index['Prioritas'].to_dict())

    size = ['Market Cap', 'Enterprise Value', 'Current Share Outstanding']
    quality = ['Return on Equity (TTM)', 'Net Profit Margin (TTM)(%)', 'Current Ratio (Quarter)', 'Debt to Equity Ratio (Quarter)']
    value = ['Current PE Ratio (TTM)', 'Current Price To Free Cashflow (TTM)', 'Current Price to Book Value']
    growth = ['EPS Growth Streak', 'Sales Growth Streak']

    df[size] = df[size] * level0['Prioritas']['Size']
    df[quality] = df[quality] * level0['Prioritas']['Quality']
    df[value] = df[value] * level0['Prioritas']['Value']
    df[growth] = df[growth] * level0['Prioritas']['Growth']

    total = []
    for i in range(len(df)):
        total.append(df.iloc[i, 1:].sum())

    df["Total"]  = total

    return df