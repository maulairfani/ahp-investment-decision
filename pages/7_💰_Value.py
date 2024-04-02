import streamlit as st
import pandas as pd
import numpy as np
from utils import process

st.title("Kriteria Value💳")
st.markdown(
    "Value mengacu pada sejauh mana harga saham mencerminkan nilai sebenarnya dari perusahaan. Dalam mencari value, investor mencoba menemukan saham-saham yang dihargai kurang dari nilai intrinsiknya. Sejumlah rasio keuangan digunakan untuk menilai value, seperti rasio P/E, P/B, dan dividen yield.🏦💰"
)

df = pd.read_excel("data/temps/value.xlsx", index_col="Unnamed: 0")
criterias = df.columns
np.fill_diagonal(df.values, 1)

st.subheader("Mari Mengenal Kriterianya!")
with st.expander("Current PE Ratio (TTM)💹"):
    st.markdown(
        "Price to Earnings (P/E) ratio adalah ukuran harga saham relatif terhadap laba per saham. Jika P/E ratio rendah, berarti harga saham rendah relatif terhadap laba yang dihasilkan perusahaan, oleh karenanya saham tersebut bisa dianggap undervalued atau dihargai di bawah nilai sebenarnya.📈💰"
    )

with st.expander("Current Price to Free Cashflow (TTM)💰"):
    st.markdown(
        "Price to Free Cash Flow ratio mengukur sejauh mana harga saham mencerminkan cash flow atau aliran uang kas yang dihasilkan perusahaan. Jika rasio ini rendah, berarti harga saham rendah relatif terhadap cash flow, sehingga saham tersebut bisa dianggap undervalued.💸💼"
    )

with st.expander("Current Price to Book Value📘"):
    st.markdown(
        "Price to Book Value ratio adalah ukuran harga saham relatif terhadap nilai buku per saham atau ekuitas perusahaan. Jika rasio ini rendah, berarti harga saham rendah relatif terhadap nilai aset sebuah perusahaan setelah dikurangi liabilities atau kewajibannya. Karenanya, saham tersebut bisa dianggap undervalued.🏦💳"
    )
    
st.divider()
st.subheader("Matriks Perbandingan Kriteria")

st.markdown("**Input Matriks**")
col1_1, col1_2, col1_3 = st.columns([6,0.3,6])

for i in range(len(df)):
    for j in range(i+1, len(df)):
        if np.isnan(df.iloc[j, i]) or df.iloc[j, i] < 1:
            first_crit = df.columns[i]
            second_crit = df.columns[j]
            index = int(df.iloc[i, j]) - 1
        else:
            first_crit = df.columns[j]
            second_crit = df.columns[i]
            index = int(df.iloc[j, i]) - 1

        with col1_1:
            crit = st.selectbox(label=f"{df.columns[i]} VS {df.columns[j]}", options=[first_crit, second_crit], )

        with col1_3:
            skala = st.radio(label="Skala", options=[1,2,3,4,5,6,7,8,9], horizontal=True, key=f"{df.columns[i]} VS {df.columns[j]}", index=index)
            st.write("")

        if crit == df.columns[j]:
            df.iloc[j, i] = skala
            df.iloc[i, j] = 1/skala
        else:
            df.iloc[i, j] = skala
            df.iloc[j, i] = 1/skala

        df.to_excel("data/temps/value.xlsx")

st.divider()
st.subheader("Matriks Perbandingan Kriteria")
st.table(df)


st.subheader("Matriks Nilai Kriteria")
df_pairwise, ci, ri, cr = process(df)
df_pairwise.to_excel("data/result/Value.xlsx")
st.table(df_pairwise)

consistency = pd.DataFrame({"Value": [ci, ri, cr]},
    index=["Consistency Index", "Random Index", "Consistency Ratio"]
)

st.subheader("Consistency")
st.table(consistency)

if cr > 0.1:
    st.error("Konsistensi perbandingan tidak memenuhi standar yang diinginkan (> 0.1). Periksa kembali perbandingan yang dibuat.")
else:
    st.success("Konsistensi perbandingan sesuai dengan standar yang diinginkan.")
