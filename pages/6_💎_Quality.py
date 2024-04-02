import streamlit as st
import pandas as pd
import numpy as np
from utils import process

st.title("Kriteria Quality✨")
st.markdown(
    "Quality mengacu pada sejauh mana sebuah perusahaan dapat diandalkan untuk menghasilkan laba yang stabil dan pertumbuhan di masa mendatang. Perusahaan-perusahaan berkualitas biasanya memiliki keunggulan kompetitif, seperti merek yang kuat atau teknologi inovatif, serta manajemen yang efisien dan etis. Dalam analisis saham, kualitas perusahaan sering ditentukan oleh sejumlah rasio keuangan.✨💰"
)

df = pd.read_excel("./data/temps/quality.xlsx", index_col="Unnamed: 0")
criterias = df.columns
np.fill_diagonal(df.values, 1)

st.subheader("Mari Mengenal Kriteria Quality Berikut:")
with st.expander("Return on Equity (TTM)💸"):
    st.markdown(
        "Return on Equity (ROE) adalah ukuran efisiensi dari sebuah perusahaan. ROE dihitung dengan membagi laba bersih dengan ekuitas atau nilai buku perusahaan. Jika ROE tinggi, artinya perusahaan mampu menghasilkan keuntungan yang tinggi dari modal yang diinvestasikan pemegang saham. 💹💼"
    )

with st.expander("Net Profit Margin (TTM)(%)💰"):
    st.markdown(
        "Net Profit Margin adalah ukuran seberapa efektif perusahaan mengubah pendapatan menjadi laba bersih. Jika margin tinggi, artinya biaya operasional perusahaan rendah relatif terhadap pendapatannya, sehingga perusahaan dapat menghasilkan lebih banyak laba bersih dari setiap unit pendapatan. ⭐📈"
    )

with st.expander("Current Ratio (Quarter)✨"):
    st.markdown(
        "Current ratio adalah ukuran likuiditas perusahaan, atau kemampuannya untuk memenuhi kewajiban jangka pendek. Jika rasio ini tinggi, artinya perusahaan memiliki aset lancar lebih dari cukup untuk membayar utang jangka pendeknya. Ini adalah tanda bahwa perusahaan cenderung memiliki keuangan yang sehat.💰📊"
    )

with st.expander("Debt to Equity Ratio (Quarter)💳"):
    st.markdown(
        "Debt to Equity Ratio mengukur seberapa banyak utang yang digunakan oleh perusahaan untuk mendanai asetnya dibandingkan dengan ekuitasnya. Jika rasio ini rendah, berarti perusahaan lebih banyak menggunakan ekuitas atau modal sendiri dalam pendanaannya, sehingga risikonya cenderung lebih rendah. 💸💰"
    )


st.divider()
st.subheader("Matriks Perbandingan Kriteria")

st.markdown("**Input Matriks**")
col1_1, col1_2, col1_3 = st.columns([5,0.3,6])

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

        df.to_excel("./data/temps/quality.xlsx")

st.divider()
st.subheader("Matriks Perbandingan Kriteria")
st.table(df)


st.subheader("Matriks Nilai Kriteria")
df_pairwise, ci, ri, cr = process(df)
df_pairwise.to_excel("./data/result/Quality.xlsx")
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
