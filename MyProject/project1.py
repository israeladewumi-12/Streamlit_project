import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sidebar Setup

with st.sidebar:
    st.Page('project1.py', title='Home')
    st.Page('pages/Project2.py', title='Flood Risk Page')

# Load Data
@st.cache_data

def load_data():
    df = pd.read_csv("/workspaces/Streamlit_project/MyProject/New_California_Less")
    df = df.drop(columns=["Unnamed: 14", "Unnamed: 15"], errors='ignore')
    return df

data = load_data()

# Tabs
st.title("California Cities Explorer + Flood Risk Detector")
tab1, tab2, tab3 = st.tabs(["Data Overview", "Visualizations", "Flood Risk Detector"])

# --- Tab 1: Data Overview ---
with tab1:
    st.subheader("Dataset Overview")
    st.write(f"Shape of data: {data.shape}")
    st.dataframe(data.head())

    st.subheader("Summary Statistics")
    st.write(data.describe())

    st.subheader("Choose Columns to Display")
    selected_columns = st.multiselect("Select columns:", data.columns.tolist(), default=data.columns.tolist())
    st.dataframe(data[selected_columns])

    st.subheader("Filter by Minimum Population")
    min_pop = st.slider("Minimum population", int(data["population_total"].min()), int(data["population_total"].max()), 50000)
    filtered_data = data[data["population_total"] >= min_pop]
    st.write(f"Cities with population >= {min_pop}:")
    st.dataframe(filtered_data)

# --- Tab 2: Visualizations ---
with tab2:
    col1, col2 = st.columns([3, 1])

    with col1:
        
        st.subheader("Population Histogram")
        fig1, ax1 = plt.subplots()
        ax1.hist(data["population_total"] ,  bins=20, color='skyblue', edgecolor='black')
        ax1.set_title("Population Histogram")
        ax1.set_xlabel("Population")
        ax1.set_ylabel("Number of Cities")
        st.pyplot(fig1)

  
    
    with col2:
        st.subheader("Raw Population Data")
        st.write(data["population_total"])

    st.subheader("Population vs Land Area")
    fig2, ax2 = plt.subplots()
    ax2.scatter(data["area_land_km2"], data["population_total"], alpha=0.7, color='green')
    ax2.set_title("Population vs Land Area")
    ax2.set_xlabel("Land Area (km²)")
    ax2.set_ylabel("Population")
    st.pyplot(fig2)




# --- Tab 3: Flood Risk Detector ---
with tab3:
    st.subheader("Flood Risk Detector")
    elevation_threshold = st.slider("Maximum Elevation for Risk (meters)", 0, 200, 50)
    water_percent_threshold = st.slider("Minimum Water Area %", 0, 100, 10)

    flood_risk_df = data[
        (data["elevation_m"] <= elevation_threshold) &
        (data["area_water_percent"] >= water_percent_threshold)
    ]

    st.write(f"Cities below {elevation_threshold}m elevation and ≥ {water_percent_threshold}% water area")
    st.dataframe(flood_risk_df[["city", "elevation_m", "area_water_percent", "population_total"]])

    if st.checkbox("Show cities on map"):
        st.map(flood_risk_df.rename(columns={"latd": "lat", "longd": "lon"}))
    st.write("This map shows cities at risk of flooding based on the selected criteria.")
