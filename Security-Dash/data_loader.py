# data_loader.py
import pandas as pd
import json
import streamlit as st

@st.cache_data
def load_data():
    metrics_df = pd.read_csv("data/metrics.csv")
    attack_timeline_df = pd.read_csv("data/attack_timeline.csv")
    top_source_ips_df = pd.read_csv("data/top_source_ips.csv")
    top_destination_ports_df = pd.read_csv("data/top_destination_ports.csv")
    cic_ids_df = pd.read_csv("data/cic_ids2017_cleaned.csv")
    with open("data/stats.json") as f:
        stats_data = json.load(f)
    return metrics_df, attack_timeline_df, top_source_ips_df, top_destination_ports_df, cic_ids_df, stats_data
