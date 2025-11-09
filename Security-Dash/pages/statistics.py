import pandas as pd
import plotly.express as px
import streamlit as st
from data_loader import load_data

st.set_page_config(page_title="Statistics", page_icon="📊", layout="wide")
st.title("📊 Attack Statistics and Analysis")

# --- Load data ---
metrics_df, attack_timeline_df, top_source_ips_df, top_destination_ports_df, cic_ids_df, stats_data = load_data()

# --- Tabs for better layout ---
tab1, tab2, tab3 = st.tabs(["Attack Distribution", "Trends Over Time", "Top IPs & Ports"])

# --- Tab 1: Attack Type Distribution ---
with tab1:
    if "attack_type" in cic_ids_df.columns:
        attacks_only = cic_ids_df[cic_ids_df["attack_type"] != "BENIGN"]
        st.subheader("Attack Type Distribution (Malicious Only)")

        # Pie chart
        attack_type_counts = attacks_only['attack_type'].value_counts().reset_index()
        attack_type_counts.columns = ['attack_type', 'count']
        attack_type_fig = px.pie(
            attack_type_counts,
            names='attack_type',
            values='count',
            title='Distribution of Attack Types',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(attack_type_fig, use_container_width=True)

        # --- Filtered Attack Types (Bar chart) ---
        st.subheader("Filtered Attack Types")
        attack_type_selected = st.multiselect(
            "Select Attack Type(s):",
            options=[a for a in cic_ids_df['attack_type'].unique() if a != "BENIGN"],
            default=[a for a in cic_ids_df['attack_type'].unique() if a != "BENIGN"]
        )

        filtered_df = cic_ids_df[cic_ids_df['attack_type'].isin(attack_type_selected)]
        filtered_attack_counts = filtered_df['attack_type'].value_counts().reset_index()
        filtered_attack_counts.columns = ['attack_type', 'count']

        fig_filtered = px.bar(
            filtered_attack_counts,
            x='attack_type',
            y='count',
            text='count',
            title="Filtered Attack Types",
            color='count',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_filtered, use_container_width=True)

    else:
        st.warning("'attack_type' column not found in dataset.")


# --- Tab 2: Temporal Trends ---
with tab2:
    if "timestamp" in cic_ids_df.columns and "attack_type" in cic_ids_df.columns:
        cic_ids_df["timestamp"] = pd.to_datetime(cic_ids_df["timestamp"])
        attacks_only = cic_ids_df[cic_ids_df["attack_type"] != "BENIGN"]
        daily_attacks = attacks_only.groupby(attacks_only['timestamp'].dt.date).size().reset_index(name="Attack Count")
        daily_attacks.rename(columns={"timestamp": "Date"}, inplace=True)

        st.subheader("Daily Attacks Over Time")
        timeline_fig = px.line(
            daily_attacks,
            x='Date',
            y='Attack Count',
            title='Daily Attacks Over Time',
            markers=True
        )
        st.plotly_chart(timeline_fig, use_container_width=True)
    else:
        st.warning("Columns 'timestamp' or 'attack_type' not found in dataset.")

# --- Tab 3: Top IPs & Ports ---
with tab3:
    col1, col2 = st.columns(2)

    # Top Destination Ports
    with col1:
        if not top_destination_ports_df.empty:
            st.subheader("Top Destination Ports (Top 10)")
            top_destination_ports_df["Destination Port"] = top_destination_ports_df["Destination Port"].astype(str)
            top_ports_df = top_destination_ports_df.sort_values("count", ascending=False).head(10)
            top_ports_fig = px.bar(
                top_ports_df,
                x="Destination Port",
                y="count",
                text="count",
                title="Top 10 Destination Ports",
                color="count",
                color_continuous_scale="Reds"
            )
            top_ports_fig.update_layout(yaxis_title="Number of Attacks", xaxis_title="Destination Port")
            st.plotly_chart(top_ports_fig, use_container_width=True)
        else:
            st.warning("top_destination_ports.csv not found or empty.")

    # Top Source IPs
    with col2:
        if not top_source_ips_df.empty:
            st.subheader("Top Source IPs (Top 10)")
            top_src_df = top_source_ips_df.sort_values("count", ascending=False).head(10)
            top_sources_fig = px.bar(
                top_src_df,
                x="source_ip",
                y="count",
                text="count",
                title="Top 10 Source IPs by Number of Attacks",
                color="count",
                color_continuous_scale="Blues"
            )
            top_sources_fig.update_layout(yaxis_title="Number of Attacks", xaxis_title="Source IP")
            st.plotly_chart(top_sources_fig, use_container_width=True)
        else:
            st.warning("top_source_ips.csv not found or empty.")


