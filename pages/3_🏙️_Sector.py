import streamlit as st
import pandas as pd
import numpy as np
from utils import process
st.title("Kriteria Sektor🏗️")
st.markdown(
    "Sektor saham mengacu pada kategori industri tempat suatu perusahaan beroperasi. Beberapa sektor contohnya adalah teknologi, kesehatan, dan finansial. Pentingnya mempertimbangkan sektor dalam memilih saham ada pada fakta bahwa setiap sektor memiliki dinamikanya sendiri yang bisa digunakan untuk memprediksi performa saham di masa mendatang. Misalnya, dalam kondisi ekonomi yang tidak menentu, saham konsumen non-primer cenderung lebih tahan banting dibandingkan yang lain. 🏭📈"
)

df = pd.read_excel("data/temps/Sector.xlsx", index_col="Unnamed: 0")
criterias = df.columns
np.fill_diagonal(df.values, 1)

st.subheader("Halo Investor! ⚡")
with st.expander("Sektor Energi⛽"):
    st.markdown(
        "Dalam sektor energi, ada banyak perusahaan yang aktif dalam bidang eksplorasi dan produksi energi, termasuk energi terbarukan dan tidak terbarukan. Produk dan jasa mereka sangat penting untuk hampir semua aspek kehidupan modern, mulai dari penerangan hingga transportasi. Oleh karena itu, pertumbuhan ekonomi sering kali berkorelasi positif dengan pertumbuhan dalam sektor energi. 🛢️🔋"
    )
    
with st.expander("Sektor Barang Baku🏭"):
    st.markdown(
        "Perusahaan dalam sektor barang baku produsen berbagai jenis material yang dihasilkan dari alam dan digunakan dalam proses produksi sektor lain, mulai dari pertanian hingga manufaktur. Jika perusahaan Anda bergerak di sektor ini, kinerja saham Anda hampir pasti akan dipengaruhi oleh fluktuasi harga komoditas global. 🌽⛏️"
    )
    
with st.expander("Sektor Konsumen Non-Primer🍿"):
    st.markdown(
        "Sektor konsumen non-primer mencakup perusahaan yang menjual barang keperluan masyarakat yang bukan kebutuhan pokok, misalnya permainan, kosmetik, dan barang elektronik. Sebagian besar perusahaan dalam sektor ini memiliki tingkat elastisitas harga produk yang relatif tinggi, artinya permintaan cenderung fluktuatif seiring dengan pasang surut kondisi ekonomi. 📱💅"
    )
    
with st.expander("Sektor Konsumen Primer🍞"):
    st.markdown(
        "Konsumen Primer, alias barang pokok, adalah barang dan jasa yang selalu dibutuhkan konsumen, seperti makanan, produk rumah tangga, dan layanan kesehatan. Karena permintaan akan produk dan jasa ini cenderung stabil, sektor konsumen primer cenderung lebih tahan terhadap resesi ekonomi dibanding sektor lainnya. 🌽💊"
    )
    
with st.expander("Sektor Keuangan💼"):
    st.markdown(
        "Sektor keuangan mencakup bank, perusahaan asuransi, reksa dana, dan institusi keuangan lainnya. Dengan berinvestasi pada sektor ini, Anda bisa mendapatkan keuntungan dari peningkatan pendapatan dan pertumbuhan ekonomi, yang biasanya berdampak positif pada industri finansial. 💰🏦"
    )
    
with st.expander("Sektor Kesehatan👩‍⚕️"):
    st.markdown(
        "Sektor ini mencakup perusahaan yang bergerak dalam penelitian, pengembangan, produksi, dan distribusi produk dan layanan kesehatan. Dari perusahaan farmasi hingga penyedia layanan kesehatan, perusahaan dalam sektor ini sering kali menjadi bagian vital dalam kemajuan ilmu kesehatan dan well-being masyarakat. 💉🌡️"
    )
    
with st.expander("Sektor Perindustrian🔨"):
    st.markdown(
        "Sektor industri adalah sektor yang melibatkan perusahaan yang membuat produk dan peralatan fisik, seperti mesin, material konstruksi, dan peralatan elektrikal. Pertumbuhan dalam sektor ini biasanya tergantung pada permintaan global dan lokal terhadap barang-barang manufaktur ini, serta keberlangsungan dan inovasi dalam teknologi produksi. 🚜🧱"
    )

with st.expander("Sektor Infrastruktur🛣️"):
    st.markdown(
        "Infrastruktur adalah 'tulang punggung' dari perekonomian, karena mencakup perusahaan yang bergerak dalam bidang konstruksi dan pemeliharaan fasilitas dan sistem yang digunakan oleh masyarakat sehari-hari, termasuk jalan, jembatan, bandara, sistem pengairan, dan pelayanan publik lainnya. 🌉🏗️"
    )

with st.expander("Sektor Properti & Real Estat🏡"):
    st.markdown(
        "Perusahaan dalam sektor ini terlibat dalam berbagai kegiatan yang terkait dengan tanah dan bangunan, mulai dari pembelian dan penjualan tanah, pengembangan dan konstruksi proyek, hingga operasi dan manajemen properti. Kinerja saham di sektor ini cukup tergantung pada siklus properti dan faktor ekonomi makro. 🏙️🏠"
    )

with st.expander("Sektor Transportasi & Logistik🚚"):
    st.markdown(
        "Perusahaan yang bergerak di sektor ini memberikan layanan pengiriman barang dan penumpang. Perusahaan-perusahaan ini memegang peranan penting dalam kelancaran perekonomian, sebagai 'penggerak' barang dari produsen ke konsumen. Sejumlah besar perusahaan transportasi dan logistik juga beroperasi di tingkat internasional, membuat saham perusahaan ini sering kali terpengaruh oleh faktor geopolitik dan global yang mempengaruhi perdagangan internasional. 🚛✈️"
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
            try:
                index = int(df.iloc[i, j]) - 1
            except:
                index = 0
        else:
            first_crit = df.columns[j]
            second_crit = df.columns[i]
            try:
                index = int(df.iloc[j, i]) - 1
            except:
                index = 0

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

        df.to_excel("data/temps/Sector.xlsx")

st.divider()
st.subheader("Matriks Perbandingan Kriteria")
st.table(df)


st.subheader("Matriks Nilai Kriteria")
df_pairwise, ci, ri, cr = process(df)
df_pairwise.to_excel("data/result/Sector.xlsx")
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
