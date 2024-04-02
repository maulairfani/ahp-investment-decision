import streamlit as st
import pandas as pd
import numpy as np
from utils import process

st.title("Kriteria Utama🚩")
st.markdown("Berikut adalah penjelasan faktor-faktor utama yang kami pertimbangkan dalam sistem dukungan keputusan kami untuk membantu Anda menentukan saham terbaik. Kami menggunakan metode 'Analytical Hierarchy Process' (AHP) dan mempertimbangkan faktor-faktor berikut : **Sector**, **Index**, **Size**, **Quality**, **Value** dan **Growth**. Masing-masing faktor memiliki peran dan pertimbangan yang berbeda yang secara keseluruhan akan memberikan penilaian dan rekomendasi terbaik untuk Anda.")
df = pd.read_excel("./data/temps/level0.xlsx", index_col="Unnamed: 0")
criterias = df.columns
np.fill_diagonal(df.values, 1)

st.subheader("Penjelasan Kriteria")
with st.expander("Sector"):
    st.markdown(
    "Sektor saham mengacu pada kategori industri tempat suatu perusahaan beroperasi. Beberapa sektor contohnya adalah teknologi, kesehatan, dan finansial. Pentingnya mempertimbangkan sektor dalam memilih saham ada pada fakta bahwa setiap sektor memiliki dinamikanya sendiri yang bisa digunakan untuk memprediksi performa saham di masa mendatang. Misalnya, dalam kondisi ekonomi yang tidak menentu, saham konsumen non-primer cenderung lebih tahan banting dibandingkan yang lain. 🏭📈"
    )

with st.expander("Index"):
    st.markdown(
    "Dalam analisis saham, index adalah indikator penting dari tren pasar secara keseluruhan. Indeks saham seperti IDX30, IDX BUMN20, dan LQ45 merangkum kinerja sejumlah perusahaan dalam satu angka tunggal, menyederhanakan proses pemantauan pasar dan membuat perbandingan kinerja antara saham menjadi lebih mudah. Terutama untuk investor pemula, indikator ini dapat membantu mengambil keputusan investasi yang lebih terinformasi. 👩‍💼📊"
    )

with st.expander("Size"):
    st.markdown(
    "Ukuran perusahaan sering digunakan sebagai kriteria dalam analisis saham. Perusahaan-perusahaan berukuran besar cenderung lebih stabil dan memiliki akses ke lebih banyak sumber daya dibandingkan perusahaan-perusahaan kecil. Di sisi lain, perusahaan-perusahaan kecil bisa memiliki potensi pertumbuhan yang tinggi. Memahami ukuran perusahaan, oleh karena itu, sangat penting dalam membuat strategi investasi. 🏢📈"
    )

with st.expander("Quality"):
    st.markdown(
    "Quality mengacu pada sejauh mana sebuah perusahaan dapat diandalkan untuk menghasilkan laba yang stabil dan pertumbuhan di masa mendatang. Perusahaan-perusahaan berkualitas biasanya memiliki keunggulan kompetitif, seperti merek yang kuat atau teknologi inovatif, serta manajemen yang efisien dan etis. Dalam analisis saham, kualitas perusahaan sering ditentukan oleh sejumlah rasio keuangan.✨💰"
    )

with st.expander("Value"):
    st.markdown(
    "Value mengacu pada sejauh mana harga saham mencerminkan nilai sebenarnya dari perusahaan. Dalam mencari value, investor mencoba menemukan saham-saham yang dihargai kurang dari nilai intrinsiknya. Sejumlah rasio keuangan digunakan untuk menilai value, seperti rasio P/E, P/B, dan dividen yield.🏦💰"
    )

with st.expander("Growth"):
    st.markdown(
    "Growth atau pertumbuhan adalah salah satu faktor yang paling sering dicari oleh investor dalam memilih saham. Perusahaan-perusahaan dengan prospek pertumbuhan yang kuat cenderung mampu menghasilkan keuntungan yang bertambah seiring waktu, yang pada akhirnya bisa meningkatkan harga saham.💹🚀"
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

        df.to_excel("./data/temps/level0.xlsx")

st.divider()
st.subheader("Matriks Perbandingan Kriteria")
st.table(df)


st.subheader("Matriks Nilai Kriteria")
df_pairwise, ci, ri, cr = process(df)
df_pairwise.to_excel("./data/result/Level0.xlsx")
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
