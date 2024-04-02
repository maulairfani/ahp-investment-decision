import streamlit as st
import pandas as pd
from utils import final_process_ahp

alternatif = pd.read_csv("data/temps/Alternatives.csv")
level0 = pd.read_excel("data/result/Level0.xlsx", index_col='Unnamed: 0')
sector = pd.read_excel("data/result/Sector.xlsx", index_col='Unnamed: 0')
index = pd.read_excel("data/result/Index.xlsx", index_col='Unnamed: 0')
size = pd.read_excel("data/result/Size.xlsx", index_col='Unnamed: 0')
quality = pd.read_excel("data/result/Quality.xlsx", index_col='Unnamed: 0')
value = pd.read_excel("data/result/Value.xlsx", index_col='Unnamed: 0')
growth = pd.read_excel("data/result/Growth.xlsx", index_col='Unnamed: 0')

st.title("🔨 Hasil Akhir")

with st.expander("#### Nilai Kriteria", True):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("**Kriteria Utama (Level 0)**")
        st.table(level0['Prioritas'].iloc[:-1].sort_values(ascending=False))
    with col2:
        st.markdown("**Sector**")
        st.table(sector['Prioritas'].iloc[:-1].sort_values(ascending=False))
    with col3:
        st.markdown("**Index**")
        st.table(index['Prioritas'].iloc[:-1].sort_values(ascending=False))
    with col4:
        st.markdown("**Size**")
        st.table(size['Prioritas'].iloc[:-1].sort_values(ascending=False))

    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Quality**")
        st.table(quality['Prioritas'].iloc[:-1].sort_values(ascending=False))
    with col2:
        st.markdown("**Value**")
        st.table(value['Prioritas'].iloc[:-1].sort_values(ascending=False))
    with col3:
        st.markdown("**Growth**")
        st.table(growth['Prioritas'].iloc[:-1].sort_values(ascending=False))

with st.expander("#### Alternatif", True):
    st.markdown("**Data Alternatif**")
    st.write(alternatif)

    st.markdown("**Normalized Data**")
    df_final = final_process_ahp(alternatif)
    st.write(df_final)

st.subheader("Ranking")
df_ranking = df_final.copy()
df_ranking = df_final[["Ticker Code", "Total"]].sort_values("Total", ascending=False).reset_index()
df_ranking.columns = ["Ranking", "Ticker Code", "Total Score"]
st.write(df_ranking)