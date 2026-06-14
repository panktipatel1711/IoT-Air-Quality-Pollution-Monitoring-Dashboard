"""
Module: main.py
Description: Enterprise IoT Environmental Telemetry Simulator - Legacy Column Header Sync.
Version: 5.2.0 (Data Preservation Mode)
"""

import os
import csv
import time
import math
import random
import pandas as pd
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# ENTERPRISE APP INITIALIZATION & STYLING
# ==========================================
st.set_page_config(
    page_title="IoT Air Quality Analytics Center",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

class AppConfig:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(PROJECT_ROOT, "data")
    LOG_FILE = os.path.join(DATA_DIR, "pollution_logs.csv")
    
    # Air Quality Index (AQI) Classification Boundaries
    LIMIT_GOOD = 800
    LIMIT_MODERATE = 1800
    LIMIT_POOR = 3000

# Ensure persistent data layers exist safely
os.makedirs(AppConfig.DATA_DIR, exist_ok=True)
if not os.path.exists(AppConfig.LOG_FILE):
    with open(AppConfig.LOG_FILE, mode='w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([
            "Timestamp", "Gas_Concentration", "Temperature_C", 
            "Humidity_Pct", "Category", "Alert_Status"
        ])

# ==========================================
# ADVANCED SENSOR TELEMETRY SYNTHESIZER
# ==========================================
@st.cache_resource
def get_simulation_state():
    return {"tick": 0}

def simulate_sensor_hardware():
    state = get_simulation_state()
    state["tick"] += 1
    t = state["tick"]
    
    sine_wave = math.sin(t * 0.1)
    temperature = round(26.5 + (sine_wave * 4.0) + random.uniform(-0.3, 0.3), 1)
    humidity = round(52.0 - (sine_wave * 7.5) + random.uniform(-0.8, 0.8), 1)

    # Cyclical Environmental Ingestion Profiles
    if t % 60 < 15:
        gas = random.randint(350, 780)       
    elif 15 <= t % 60 < 35:
        gas = random.randint(1100, 1750)     
    elif 35 <= t % 60 < 50:
        gas = random.randint(3100, 4095)     
    else:
        gas = random.randint(650, 1050)      

    # Map raw gas readings to strict compliance thresholds (Synced with your original columns)
    if gas <= AppConfig.LIMIT_GOOD:
        grade, alert_status = "Good", "OFF"
    elif gas <= AppConfig.LIMIT_MODERATE:
        grade, alert_status = "Moderate", "OFF"
    elif gas <= AppConfig.LIMIT_POOR:
        grade, alert_status = "Poor", "ACTIVE_BLINK"
    else:
        grade, alert_status = "Hazardous", "CRITICAL_SIREN"

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(AppConfig.LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([stamp, gas, temperature, humidity, grade, alert_status])
    except PermissionError:
        st.sidebar.error("⚠️ CSV Access Denied! Please close 'pollution_logs.csv' in Excel or Notepad.")
        
    return stamp, gas, temperature, humidity, grade

# ==========================================
# PRESENTATION INTERFACE & VIEW LAYER
# ==========================================
st.title("🍃 IoT-Based Air Quality & Pollution Monitoring Dashboard")
st.markdown("---")

st.sidebar.header("🕹️ Edge Node Controls")
run_pipeline = st.sidebar.toggle("Activate Live Sensor Polling Engine", value=True)
refresh_rate = st.sidebar.slider("Sensor Ingestion Delay Interval (Seconds)", 1, 5, 2)

if run_pipeline:
    stamp, gas, temp, humid, grade = simulate_sensor_hardware()
    
    if grade in ["Poor", "Hazardous"]:
        st.error(f"🚨 CRITICAL ALARM: HIGH POLLUTION DETECTED AT {stamp}!")
        
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="💨 Gas Concentration Core", value=f"{gas} PPM")
    with col2:
        st.metric(label="Temperature", value=f"{temp} °C")
    with col3:
        st.metric(label="Humidity", value=f"{humid} % RH")
    with col4:
        st.markdown(f"### System Status\n**Assessment:** `{grade.upper()}`")
        
    st.markdown("### 📈 Real-Time Diagnostic Visualization Streams")
    
    if os.path.exists(AppConfig.LOG_FILE):
        try:
            df = pd.read_csv(AppConfig.LOG_FILE)
            
            if len(df) > 40:
                df = df.tail(40)
                
            col_left, col_right = st.columns(2)
            
            with col_left:
                # Fixed to map with your exact file header 'Gas_Concentration'
                fig_gas = px.line(
                    df, x="Timestamp", y="Gas_Concentration", 
                    title="Continuous Chemical & Gas Concentration Monitoring Timeline (PPM)",
                    color_discrete_sequence=["#e74c3c"]
                )
                fig_gas.update_layout(template="plotly_dark", xaxis_title="Timeline Frames", yaxis_title="Units (PPM)")
                st.plotly_chart(fig_gas, use_container_width=True)
                
            with col_right:
                fig_climate = go.Figure()
                fig_climate.add_trace(go.Scatter(x=df["Timestamp"], y=df["Temperature_C"], name="Temperature (°C)", line=dict(color="#2ecc71", width=2.5)))
                fig_climate.add_trace(go.Scatter(x=df["Timestamp"], y=df["Humidity_Pct"], name="Humidity (%)", line=dict(color="#3498db", width=2.5, dash='dash')))
                fig_climate.update_layout(template="plotly_dark", title="Microclimate Diagnostics Tracking Core", xaxis_title="Timeline Frames")
                st.plotly_chart(fig_climate, use_container_width=True)

            st.markdown("### 🗃️ Downstream Data Log Ledger Repository (Persistent Storage)")
            st.dataframe(df.sort_values(by="Timestamp", ascending=False), use_container_width=True, hide_index=True)
        except Exception as e:
            st.sidebar.warning(f"Sync configuration in progress... ({str(e)})")

    # Replaced automatic blinking loop with a professional manual update anchor
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Fetch Live IoT Data"):
        st.rerun()
else:
    st.info("System Standby Mode.")