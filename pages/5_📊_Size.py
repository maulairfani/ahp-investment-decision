import streamlit as st
import pandas as pd
import numpy as np
from utils import process

st.title("Kriteria Size🎯")
st.markdown(
    "Ukuran perusahaan sering digunakan sebagai kriteria dalam analisis saham. Perusahaan-perusahaan berukuran besar cenderung lebih stabil dan memiliki akses ke lebih banyak sumber daya dibandingkan perusahaan-perusahaan kecil. Di sisi lain, perusahaan-perusahaan kecil bisa memiliki potensi pertumbuhan yang tinggi. Memahami ukuran perusahaan, oleh karena itu, sangat penting dalam membuat strategi investasi. 🏢📈"
)

df = pd.read_excel("./data/temps/size.xlsx", index_col="Unnamed: 0")
criterias = df.columns
np.fill_diagonal(df.values, 1)

st.subheader("Apa Saja Ukuran yang Biasa Dilihat?")
with st.expander("Market Cap💵"):
    st.markdown(
        "Market Cap, atau kapitalisasi pasar, adalah nilai total harga saham sebuah perusahaan. Ini dihitung dengan mengalikan harga per saham dengan jumlah total saham yang beredar. Dengan melihat Market Cap, Anda bisa mendapatkan gambaran umum tentang ukuran perusahaan dan bagaimana investor lain memandang nilai perusahaan tersebut. 💼💰"
    )

with st.expander("Enterprise Value💸"):
    st.markdown(
        "Enterprise Value, atau EV, adalah penilaian lengkap sebuah perusahaan. EV dihitung dengan menambahkan Market Cap dengan total utang, lalu dikurangi dengan kas dan setara kas yang dimiliki perusahaan. Dengan melihat EV, Anda bisa mendapatkan gambaran yang lebih komprehensif tentang nilai perusahaan, termasuk bagaimana perusahaan itu dibiayai (hutang atau ekuitas) dan seberapa likuid posisi keuangannya. 💱💼"
    )

with st.expander("Current Share Outstanding💹"):
    st.markdown(
        "Current Share Outstanding adalah jumlah total saham yang beredar di pasar. Jumlah ini penting karena menentukan berapa banyak kepemilikan yang dimiliki oleh seorang pemegang saham. Jika sebuah perusahaan memiliki banyak saham yang beredar, maka setiap saham mewakili sebagian kecil dari kepemilikan perusahaan. 📉💰"
    )



st.divider()
st.subheader("Matriks Perbandingan Kriteria")

st.markdown("**Input Matriks**")
col1_1, col1_2, col1_3 = st.columns([3,0.3,6])

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

        df.to_excel("./data/temps/size.xlsx")

st.divider()
st.subheader("Matriks Perbandingan Kriteria")
st.table(df)


st.subheader("Matriks Nilai Kriteria")
df_pairwise, ci, ri, cr = process(df)
df_pairwise.to_excel("./data/result/Size.xlsx")
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
