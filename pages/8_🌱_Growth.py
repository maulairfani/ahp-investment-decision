import streamlit as st
import pandas as pd
import numpy as np
from utils import process

st.title("Kriteria Growth🌱")
st.markdown(
    "Growth atau pertumbuhan adalah salah satu faktor yang paling sering dicari oleh investor dalam memilih saham. Perusahaan-perusahaan dengan prospek pertumbuhan yang kuat cenderung mampu menghasilkan keuntungan yang bertambah seiring waktu, yang pada akhirnya bisa meningkatkan harga saham.💹🚀"
)

df = pd.read_excel("./data/temps/Growth.xlsx", index_col="Unnamed: 0")
criterias = df.columns
np.fill_diagonal(df.values, 1)

st.subheader("Apa Saja Kriteria di Growth?")
with st.expander("EPS Growth Streak💸"):
    st.markdown(
        "EPS Growth Streak adalah ukuran seberapa lama sebuah perusahaan telah mengalami peningkatan laba per saham secara berturut-turut. Jika streak ini panjang, berarti perusahaan terus-menerus meningkatkan labanya, yang adalah tanda pertumbuhan yang kuat dan konsisten.💰📈"
    )
with st.expander("Sales Growth Streak💰"):
    st.markdown(
        "Sales Growth Streak adalah ukuran seberapa lama sebuah perusahaan telah mengalami peningkatan penjualan secara berturut-turut. Jika streak ini panjang, berarti perusahaan terus-menerus meningkatkan penjualannya, yang bisa menjadi tanda pertumbuhan yang sehat dan konsisten.💹💸"
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

        df.to_excel("./data/temps/Growth.xlsx")

st.divider()
st.subheader("Matriks Perbandingan Kriteria")
st.table(df)


st.subheader("Matriks Nilai Kriteria")
df_pairwise, ci, ri, cr = process(df)
df_pairwise.to_excel("./data/result/Growth.xlsx")
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
