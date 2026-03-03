import streamlit as st
import pandas as pd
import plotly.express as px

# Fancy UI Config
st.set_page_config(page_title="HKDSE Analytics Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stMetric { border-radius: 15px; background: #1c1e26; border: 1px solid #3d4455; padding: 20px; }
    </style>
""", unsafe_allow_html=True)

# Load full CSV
@st.cache_data
def get_data():
    return pd.read_csv("data.csv")

df = get_data()

# --- SIDEBAR SEARCH ---
st.sidebar.title("🔍 HKDSE Search")
sub_list = sorted(df['Subject'].unique())
selected_sub = st.sidebar.selectbox("Choose Subject", sub_list)

# --- MAIN CONTENT ---
st.title(f"📊 {selected_subject} Performance Hub")

# Filter data
sub_df = df[df['Subject'] == selected_sub].sort_values('Year')

# 1. Automatic Mean Stats
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Avg 5** Cutoff", f"{sub_df['5**'].mean():.1f}%")
with col2: st.metric("Avg 5* Cutoff", f"{sub_df['5*'].mean():.1f}%")
with col3: st.metric("Avg 5 Cutoff", f"{sub_df['5'].mean():.1f}%")
with col4: st.metric("Avg 4 Cutoff", f"{sub_df['4'].mean():.1f}%")

# 2. Level Predictor (Requirement 4)
st.divider()
st.subheader("🎯 Result Predictor")
p_col1, p_col2 = st.columns([1, 2])

with p_col1:
    my_score = st.slider("Input Mock Exam Score (%)", 0.0, 100.0, 75.0)
    target_year = st.selectbox("Compare with Year:", sub_df['Year'].unique()[::-1])
    
    # Logic
    year_row = sub_df[sub_df['Year'] == target_year].iloc[0]
    result = "Below Level 2"
    for lvl in ['5**', '5*', '5', '4', '3', '2']:
        if my_score >= year_row[lvl]:
            result = f"Level {lvl}"
            break
    st.success(f"Based on {target_year} difficulty, you get: **{result}**")

with p_col2:
    # 3. Interactive Design (Requirement 1)
    fig = px.line(sub_df, x='Year', y=['5**', '5', '3'], 
                 title="Cutoff Difficulty Trend (2012-2025)",
                 markers=True, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# Full Data Visibility
st.subheader("📋 Historical Raw Data")
st.dataframe(sub_df, use_container_width=True)