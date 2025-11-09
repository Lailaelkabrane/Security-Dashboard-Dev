import streamlit as st
import pandas as pd
from data_loader import load_data

st.set_page_config(
    page_title="Security Dashboard",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ Security Dashboard – Real-Time Threat Monitoring")
st.write("")  # Add spacing

# --- Load all data at once ---
metrics_df, attack_timeline_df, top_source_ips_df, top_destination_ports_df, cic_ids_df, stats_data = load_data()

# --- Display KPIs (from stats.json or fallback) ---
st.subheader("📊 Key Security Metrics")
st.write("")  # Extra space below the title

if stats_data:
    # --- Base metrics ---
    total_events = stats_data.get("total_events", len(cic_ids_df))
    malicious_rate = round(stats_data.get("attack_rate_pct", 0), 2)

    attack_types = stats_data.get("by_attack_type", {})
    attack_types_filtered = {k: v for k, v in attack_types.items() if k != "BENIGN"}
    top_attack = max(attack_types_filtered, key=attack_types_filtered.get) if attack_types_filtered else "N/A"

    # Average response time from dataset
    if not cic_ids_df.empty and "timestamp" in cic_ids_df.columns:
        cic_ids_df["timestamp"] = pd.to_datetime(cic_ids_df["timestamp"])
        cic_ids_df = cic_ids_df.sort_values("timestamp")
        time_diffs = cic_ids_df["timestamp"].diff().dt.total_seconds().dropna()
        avg_response = f"{round(time_diffs.mean(), 2)} s" if not time_diffs.empty else "<30s>"
    else:
        avg_response = "<30s>"

    # --- Additional metrics ---
    unique_sources = cic_ids_df['source_ip'].nunique() if not cic_ids_df.empty else 0
    unique_dest_ports = cic_ids_df['destination_ip'].nunique() if not cic_ids_df.empty else 0

    top_dest_port = stats_data.get("top_destination_ports", {})
    top_port = max(top_dest_port, key=top_dest_port.get) if top_dest_port else "N/A"

    benign_count = stats_data.get("total_benign", 0)
    total_attacks_count = stats_data.get("total_attacks", 0)
    total_traffic = benign_count + total_attacks_count
    benign_pct = round((benign_count / total_traffic) * 100, 2) if total_traffic > 0 else 0
    malicious_pct = round((total_attacks_count / total_traffic) * 100, 2) if total_traffic > 0 else 0

    # --- KPI Row 1 ---
    st.write("")  # Add spacing before first row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🗂️ Total Events", total_events)
    
    # Color highlighting for malicious traffic
    delta_color = "inverse" if malicious_rate > 50 else "normal"
    col2.metric("🚨 Malicious Traffic (%)", f"{malicious_rate}%", delta_color=delta_color)
    
    col3.metric("🔥 Top Attack Type", top_attack)
    col4.metric("⏱️ Avg Response Time", avg_response)

    # --- KPI Row 2 ---
    st.write("")  # Add spacing before second row
    col5, col6, col7, col8 = st.columns(4)
    col5.metric("🌐 Unique Source IPs", unique_sources)
    col6.metric("🖧 Unique Destination IPs", unique_dest_ports)
    col7.metric("🛡️ Top Destination Port", top_port)
    col8.metric("✅ Benign Traffic (%)", f"{benign_pct}%")
    st.write("") 
    col8.metric("🚨 Malicious Traffic", f"{malicious_pct}%")
    st.write("")  # Extra spacing after KPI section

else:
    st.warning("stats.json is empty or not found.")

# --- Summary preview ---
st.subheader("🗂️ Data Overview with Attack Highlight")
st.write("")  # Space before table

if not cic_ids_df.empty:
    # Highlight malicious attacks
    cic_ids_df["is_malicious"] = cic_ids_df["attack_type"].apply(lambda x: x != "BENIGN")
    st.dataframe(
        cic_ids_df.head(10).style.applymap(
            lambda v: 'background-color: red' if v != "BENIGN" else '', subset=["attack_type"]
        ),
        use_container_width=True
    )
else:
    st.warning("No dataset found. Please add data to the /data folder.")
