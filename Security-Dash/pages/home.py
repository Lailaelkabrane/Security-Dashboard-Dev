# pages/1_Home.py
import streamlit as st
from data_loader import load_data

st.title("Security Dashboard - KPI Overview")

# Load the data
metrics_df, attack_timeline_df, top_source_ips_df, top_destination_ports_df, cic_ids_df, stats_data = load_data()

# Example KPIs
#st.write("Columns in cic_ids_df:", cic_ids_df.columns.tolist())

total_attacks = len(cic_ids_df)
unique_sources = cic_ids_df['source_ip'].nunique()
unique_dest_ports = cic_ids_df['destination_ip'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Attacks", total_attacks)
col2.metric("Unique Source IPs", unique_sources)
col3.metric("Unique Destination Ports", unique_dest_ports)
