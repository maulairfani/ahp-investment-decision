import streamlit as st
import pandas as pd
import numpy as np
from utils import process

st.title("Kriteria Utama🚩")
st.markdown("This is the Economic Sector according to the Thomson Reuters Business Classification Schema (TRBC). There are 10 economic sectors in the schema which classify stocks across broad economic segments such as Technology and Financials.")

df = pd.read_excel("data/temps/level0.xlsx", index_col="Unnamed: 0")
criterias = df.columns
np.fill_diagonal(df.values, 1)

st.subheader("Penjelasan Kriteria")
with st.expander("LQ45"):
    st.markdown("LQ45 adalah indeks yang terdiri dari 45 saham dengan likuiditas (volume perdagangan) tertinggi di Bursa Efek Indonesia (BEI). Saham-saham yang masuk dalam indeks LQ45 dipilih berdasarkan kriteria likuiditas, kapitalisasi pasar, dan frekuensi perdagangan. Indeks ini sering digunakan sebagai acuan untuk mengukur kinerja pasar saham secara keseluruhan.")
    
with st.expander("IDX30"):
    st.markdown("IDX30 adalah indeks yang terdiri dari 30 saham unggulan di BEI. Saham-saham yang termasuk dalam indeks IDX30 dipilih berdasarkan kriteria kapitalisasi pasar, likuiditas, dan kinerja keuangan perusahaan. Indeks ini bertujuan untuk merepresentasikan kinerja saham-saham terbaik di pasar modal Indonesia.")

with st.expander("IDXHIDIV20"):
    st.markdown("IDXHIDIV20 adalah indeks yang terdiri dari 20 saham dengan dividen tertinggi di BEI. Saham-saham yang masuk dalam indeks IDXHIDIV20 dipilih berdasarkan tingginya tingkat dividen yang dibagikan kepada pemegang saham. Indeks ini memberikan gambaran tentang saham-saham yang memiliki kecenderungan untuk memberikan dividen yang stabil dan tinggi.")

with st.expander("IDXBUMN20"):
    st.markdown("IDXBUMN20 adalah indeks yang terdiri dari 20 saham dari perusahaan Badan Usaha Milik Negara (BUMN) yang terdaftar di BEI. Saham-saham yang termasuk dalam indeks IDXBUMN20 berasal dari perusahaan-perusahaan yang dimiliki oleh pemerintah Indonesia. Indeks ini memberikan gambaran tentang kinerja saham-saham BUMN yang merupakan bagian penting dari ekonomi Indonesia.")


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

        df.to_excel("data/temps/level0.xlsx")

st.divider()
st.subheader("Matriks Perbandingan Kriteria")
st.table(df)


st.subheader("Matriks Nilai Kriteria")
df_pairwise, ci, ri, cr = process(df)
df_pairwise.to_excel("data/result/Level0.xlsx")
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
