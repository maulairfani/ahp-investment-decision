import streamlit as st
import pandas as pd
from utils import final_process_ahp
import plotly.express as px

alternatif = pd.read_csv("data/temps/Alternatives.csv")
level0 = pd.read_excel("data/result/Level0.xlsx", index_col='Unnamed: 0')
sector = pd.read_excel("data/result/Sector.xlsx", index_col='Unnamed: 0')
index = pd.read_excel("data/result/Index.xlsx", index_col='Unnamed: 0')
size = pd.read_excel("data/result/Size.xlsx", index_col='Unnamed: 0')
quality = pd.read_excel("data/result/Quality.xlsx", index_col='Unnamed: 0')
value = pd.read_excel("data/result/Value.xlsx", index_col='Unnamed: 0')
growth = pd.read_excel("data/result/Growth.xlsx", index_col='Unnamed: 0')

col_size = ['Market Cap', 'Enterprise Value', 'Current Share Outstanding']
col_quality = ['Return on Equity (TTM)', 'Net Profit Margin (TTM)(%)', 'Current Ratio (Quarter)', 'Debt to Equity Ratio (Quarter)']
col_value = ['Current PE Ratio (TTM)', 'Current Price To Free Cashflow (TTM)', 'Current Price to Book Value']
col_growth = ['EPS Growth Streak', 'Sales Growth Streak']

st.title("Hasil Akhir🚨")

st.subheader("**🚩Data Alternatif**")
st.write(alternatif)

df_final = final_process_ahp(alternatif)


# with st.expander("#### Nilai Kriteria", True):
st.subheader("🚀Nilai Kriteria")
kriteria = st.selectbox("Pilih kriteria untuk di visualisasikan!", options=["Sector", "Index", "Size", "Quality", "Value", "Growth", "Kriteria Utama"])


if kriteria == "Sector":
    col1, col2 = st.columns(2)

    with col1:
        temp = sector['Prioritas'].iloc[:-1].sort_values(ascending=True).reset_index()
        temp.columns = ["Kriteria", "Skor Prioritas"]
        fig = px.bar(temp, x='Skor Prioritas', y='Kriteria', title="Sector", height=300)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        temp_col = ['Sector', 'Ticker Code']
        temp = df_final[temp_col].copy()
        total = []
        for i in range(len(temp)):
            total.append(temp.iloc[i, :-1].sum())
        temp["Skor"]  = total
        temp = temp.sort_values("Skor", ascending=True)
        fig = px.bar(temp, x='Skor', y='Ticker Code', title="Saham Terbaik Berdasarkan Kriteria Sector", height=300)
        st.plotly_chart(fig, use_container_width=True)

elif kriteria == "Index":
    col1, col2 = st.columns(2)

    with col1:
        temp =index['Prioritas'].iloc[:-1].sort_values(ascending=True).reset_index()
        temp.columns = ["Kriteria", "Skor Prioritas"]
        fig = px.bar(temp, x='Skor Prioritas', y='Kriteria', title="Index", height=300)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        temp_col = ["Index", 'Ticker Code']
        temp = df_final[temp_col].copy()
        total = []
        for i in range(len(temp)):
            total.append(temp.iloc[i, :-1].sum())
        temp["Skor"]  = total
        temp = temp.sort_values("Skor", ascending=True)
        fig = px.bar(temp, x='Skor', y='Ticker Code', title="Saham Terbaik Berdasarkan Kriteria Index", height=300)
        st.plotly_chart(fig, use_container_width=True)

elif kriteria == "Size":
    col1, col2 = st.columns(2)

    with col1:
        temp = size['Prioritas'].iloc[:-1].sort_values(ascending=True).reset_index()
        temp.columns = ["Kriteria", "Skor Prioritas"]
        fig = px.bar(temp, x='Skor Prioritas', y='Kriteria', title="Size", height=300)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        temp_col = col_size + ['Ticker Code']
        temp = df_final[temp_col].copy()
        total = []
        for i in range(len(temp)):
            total.append(temp.iloc[i, :-1].sum())
        temp["Skor"]  = total
        temp = temp.sort_values("Skor", ascending=True)
        fig = px.bar(temp, x='Skor', y='Ticker Code', title="Saham Terbaik Berdasarkan Kriteria Size", height=300)
        st.plotly_chart(fig, use_container_width=True)

elif kriteria == "Quality":
    col1, col2 = st.columns(2)

    with col1:
        temp = quality['Prioritas'].iloc[:-1].sort_values(ascending=True).reset_index()
        temp.columns = ["Kriteria", "Skor Prioritas"]
        fig = px.bar(temp, x='Skor Prioritas', y='Kriteria', title="Quality", height=300)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        temp_col = col_quality + ['Ticker Code']
        temp = df_final[temp_col].copy()
        total = []
        for i in range(len(temp)):
            total.append(temp.iloc[i, :-1].sum())
        temp["Skor"]  = total
        temp = temp.sort_values("Skor", ascending=True)
        fig = px.bar(temp, x='Skor', y='Ticker Code', title="Saham Terbaik Berdasarkan Kriteria Quality", height=300)
        st.plotly_chart(fig, use_container_width=True)

elif kriteria == "Value":
    col1, col2 = st.columns(2)

    with col1:
        temp = value['Prioritas'].iloc[:-1].sort_values(ascending=True).reset_index()
        temp.columns = ["Kriteria", "Skor Prioritas"]
        fig = px.bar(temp, x='Skor Prioritas', y='Kriteria', title="Value", height=300)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        temp_col = col_value + ['Ticker Code']
        temp = df_final[temp_col].copy()
        total = []
        for i in range(len(temp)):
            total.append(temp.iloc[i, :-1].sum())
        temp["Skor"]  = total
        temp = temp.sort_values("Skor", ascending=True)
        fig = px.bar(temp, x='Skor', y='Ticker Code', title="Saham Terbaik Berdasarkan Kriteria Value", height=300)
        st.plotly_chart(fig, use_container_width=True)

elif kriteria == "Growth":
    col1, col2 = st.columns(2)

    with col1:
        temp = growth['Prioritas'].iloc[:-1].sort_values(ascending=True).reset_index()
        temp.columns = ["Kriteria", "Skor Prioritas"]
        fig = px.bar(temp, x='Skor Prioritas', y='Kriteria', title="Growth", height=300)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        temp_col = col_growth + ['Ticker Code']
        temp = df_final[temp_col].copy()
        total = []
        for i in range(len(temp)):
            total.append(temp.iloc[i, :-1].sum())
        temp["Skor"]  = total
        temp = temp.sort_values("Skor", ascending=True)
        fig = px.bar(temp, x='Skor', y='Ticker Code', title="Saham Terbaik Berdasarkan Kriteria Growth", height=300)
        st.plotly_chart(fig, use_container_width=True)

elif kriteria == "Kriteria Utama":
    temp = level0['Prioritas'].iloc[:-1].sort_values(ascending=True).reset_index()
    temp.columns = ["Kriteria", "Skor Prioritas"]
    fig = px.bar(temp, x='Skor Prioritas', y='Kriteria', title="Quality", height=300)
    st.plotly_chart(fig, use_container_width=True)


df_ranking = df_final.copy()
df_ranking = df_final[["Ticker Code", "Total"]]
df_ranking.columns = ["Ticker Code", "Total Score"]

alternatif2 = pd.read_csv("data/temps/Alternatives.csv")
temp = pd.merge(alternatif2, df_ranking, on="Ticker Code", how="inner").sort_values("Total Score", ascending=False)

st.subheader("Saham Terbaik: {}🏆🏆".format(temp["Ticker Code"].iloc[0]))

col1, col2 = st.columns([1, 5])

with col1:
    st.write("")
    st.write("")
    color = st.radio("Select Color", ["Index", "Sector"])

with col2:
    fig = px.bar(temp, x="Ticker Code", y="Total Score", color=color,
             title="Ranking Saham Terbaik (Overall)")
    st.plotly_chart(fig, use_container_width=True)  