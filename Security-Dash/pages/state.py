import pandas as pd
import plotly.express as px
import streamlit as st
from data_loader import load_data

# Load data
metrics_df, attack_timeline_df, top_source_ips_df, top_destination_ports_df, cic_ids_df, stats_data = load_data()

# Convert timestamp to datetime
attack_timeline_df['timestamp'] = pd.to_datetime(attack_timeline_df['timestamp'])

# Aggregate attacks per day
daily_attacks = attack_timeline_df.groupby(attack_timeline_df['timestamp'].dt.date)['is_attack'].sum().reset_index()
daily_attacks.columns = ['Date', 'Attack Count']

# Plot aggregated line chart
st.subheader("Daily Attacks Over Time")
timeline_fig = px.line(
    daily_attacks,
    x='Date',
    y='Attack Count',
    title='Daily Attacks Over Time'
)
st.plotly_chart(timeline_fig, use_container_width=True)

#bar chart 
st.subheader("Top Source IPs")
top_sources_fig = px.bar(
    top_source_ips_df,
    x="source_ip",
    y="count",
    title="Top Source IPs by Number of Attacks"
)
st.plotly_chart(top_sources_fig, use_container_width=True)


#bar chart  2
st.subheader("Top Destination Ports")
top_ports_fig = px.bar(
    top_destination_ports_df,
    x="Destination Port",
    y="count",
    title="Top Destination Ports"
)
st.plotly_chart(top_ports_fig, use_container_width=True)


#pie chart 
st.write("Columns in cic_ids_df:", cic_ids_df.columns.tolist())
st.subheader("Attack Type Distribution")
attack_type_counts = cic_ids_df['attack_type'].value_counts().reset_index()
attack_type_counts.columns = ['attack_type', 'count']

attack_type_fig = px.pie(
    attack_type_counts,
    names='attack_type',
    values='count',
    title='Distribution of Attack Types'
)
st.plotly_chart(attack_type_fig, use_container_width=True)

# Filter by attack type
st.write("Columns in cic_ids_df:", cic_ids_df.columns.tolist())
attack_type_selected = st.multiselect(
    "Select Attack Type(s):",
    options=cic_ids_df['attack_type'].unique(),
    default=cic_ids_df['attack_type'].unique()
)

filtered_df = cic_ids_df[cic_ids_df['attack_type'].isin(attack_type_selected)]

# Update chart with filtered data
filtered_attack_counts = filtered_df['attack_type'].value_counts().reset_index()
filtered_attack_counts.columns = ['attack_type', 'count']

fig_filtered = px.bar(filtered_attack_counts, x='attack_type', y='count', title="Filtered Attack Types")
st.plotly_chart(fig_filtered, use_container_width=True)
