import streamlit as st
import pandas as pd
import numpy as np
from utils import process

st.title("Kriteria Index📉📈")
st.markdown(
    "Dalam analisis saham, index adalah indikator penting dari tren pasar secara keseluruhan. Indeks saham seperti IDX30, IDX BUMN20, dan LQ45 merangkum kinerja sejumlah perusahaan dalam satu angka tunggal, menyederhanakan proses pemantauan pasar dan membuat perbandingan kinerja antara saham menjadi lebih mudah. Terutama untuk investor pemula, indikator ini dapat membantu mengambil keputusan investasi yang lebih terinformasi. 👩‍💼📊"
)

df = pd.read_excel("data/temps/index.xlsx", index_col="Unnamed: 0")
criterias = df.columns
np.fill_diagonal(df.values, 1)

st.subheader("Mari Mengenal Kriteria Indeks Berikut:")
with st.expander("LQ45⭐"):
    st.markdown(
        "LQ45 adalah indeks yang mencakup 45 perusahaan dengan nilai kapitalisasi pasar dan volume perdagangan paling tinggi di BEI. Artinya, perusahaan-perusahaan ini adalah yang paling 'likuid' dalam arti banyak ditransaksikan oleh investor. Sebagai titik referensi bagi pasar secara keseluruhan, LQ45 sering digunakan sebagai acuan dalam analisis dan strategi investasi.💼💰"
    )
    
with st.expander("IDX30💹"):
    st.markdown(
        "IDX30 adalah indeks yang mencakup 30 perusahaan terbesar di BEI dalam hal nilai kapitalisasi pasar. IDX30 memberikan gambaran cepat tentang dinamika pasar dengan memfokuskan pada perusahaan-perusahaan besar yang kegiatan usahanya memiliki dampak signifikan terhadap ekonomi. 💱📈"
    )

with st.expander("IDXHIDIV20💸"):
    st.markdown(
        "IDXHIDIV20, atau indeks dengan dividen tinggi, adalah indeks yang berisikan 20 perusahaan yang memiliki tingkat pembayaran dividen tertinggi. IDXHIDIV20 bisa menjadi pilihan menarik bagi investor yang mencari penghasilan pasif dari dividen, selain potensi kenaikan harga saham. 💵💰"
    )

with st.expander("IDXBUMN20🏢"):
    st.markdown(
        "IDXBUMN20 adalah indeks yang terdiri dari 20 saham dari perusahaan-perusahaan yang dimiliki oleh pemerintah. Indeks ini memudahkan investor untuk memantau kinerja BUMN yang memiliki peran penting dalam perekonomian Indonesia. 🏦💼"
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

        df.to_excel("data/temps/Index.xlsx")

st.divider()
st.subheader("Matriks Perbandingan Kriteria")
st.table(df)


st.subheader("Matriks Nilai Kriteria")
df_pairwise, ci, ri, cr = process(df)
df_pairwise.to_excel("data/result/Index.xlsx")
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
