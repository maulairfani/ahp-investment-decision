import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide"
)

st.title("Selamat Datang di DSS Investasi Saham👋")
st.markdown("Hai, Investor👋! Platform ini dirancang untuk membantu keputusan investasi kamu menggunakan metode AHP (Analytical Hierarchical Process) khusus untuk kamu yang ingin menemukan saham terbaik untuk portofolio kamu. 🚀📈")

st.markdown("AHP adalah metode yang dipakai banyak orang untuk memudahkan pengambilan keputusan yang kompleks, khususnya saat kamu harus mempertimbangkan banyak kriteria. Dalam dunia investasi, terutama saham, tentunya kamu harus mempertimbangkan banyak faktor penting sebelum menentukan pilihan 👀.")

st.markdown("Skala pembobotan yang kami gunakan untuk tiap kriteria adalah sebagai berikut:")
st.image("data/skala.png", caption="Skala Pembobotan Kriteria AHP")


st.subheader("Kriteria AHP")
st.markdown("Oke, jadi di DSS ini kita akan mempertimbangkan kriteria-kriteria penting 🏆 dalam memilih suatu saham, yaitu:")
st.image("data/ahp.drawio.png")


