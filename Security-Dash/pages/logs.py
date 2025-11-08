import streamlit as st
import pandas as pd
#logs table from dataset
st.title("📂 Logs Explorer")

logs = pd.read_csv("data/clean_data.csv")

ip_filter = st.text_input("Filter by IP")
if ip_filter:
    logs = logs[logs["ip"].str.contains(ip_filter)]

st.dataframe(logs)
