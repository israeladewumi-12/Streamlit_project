import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sidebar Setup
with st.sidebar:
    st.Page('project1.py', title='Home')
    st.Page('pages/Project2.py', title='Property Risk Page')

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("./pages/New_Melbourn_Full")
    df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')
    return df

data = load_data()

st.title("Melbourne Housing Explorer + Property Risk Detector")
tab1, tab2, tab3 = st.tabs(["Data Overview", "Visualizations", "Low-Lying Risk Detector"])

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

    st.subheader("Filter by Minimum Price")
    min_price = st.slider("Minimum price", int(data["Price"].min()), int(data["Price"].max()), 500000)
    filtered_data = data[data["Price"] >= min_price]
    st.write(f"Properties priced ≥ ${min_price}:")
    st.dataframe(filtered_data)

# --- Tab 2: Visualizations ---
with tab2:
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Price Distribution Histogram")
        fig1, ax1 = plt.subplots()
        ax1.hist(data["Price"].dropna(), bins=30, color='purple', edgecolor='black')
        ax1.set_title("Price Distribution")
        ax1.set_xlabel("Price (AUD)")
        ax1.set_ylabel("Count")
        st.pyplot(fig1)

    with col2:
        st.subheader("Raw Price Data")
        st.write(data["Price"])

    st.subheader("Landsize vs Price")
    fig2, ax2 = plt.subplots()
    ax2.scatter(data["Landsize"], data["Price"], alpha=0.5, color='darkblue')
    ax2.set_title("Landsize vs Price")
    ax2.set_xlabel("Landsize (sqm)")
    ax2.set_ylabel("Price (AUD)")
    st.pyplot(fig2)

# --- Tab 3: Low-Lying Property Risk Detector ---
with tab3:
    st.subheader("Risk Detector for Low-Lying Properties")
    elevation_threshold = st.slider("Maximum Lattitude (proxy for elevation)", float(data["Lattitude"].min()), float(data["Lattitude"].max()), 37.80)
    landsize_threshold = st.slider("Minimum Landsize", 0, int(data["Landsize"].max()), 500)

    # Simulate flood-prone properties: Low elevation (lattitude proxy) + Large land size
    flood_risk_df = data[
        (data["Lattitude"] <= elevation_threshold) &
        (data["Landsize"] >= landsize_threshold)
    ]

    st.write(f"Properties with lattitude ≤ {elevation_threshold} and landsize ≥ {landsize_threshold} sqm:")
    st.dataframe(flood_risk_df[["Suburb", "Address", "Price", "Landsize", "Lattitude", "Longtitude"]])

    if st.checkbox("Show properties on map"):
        st.map(flood_risk_df.rename(columns={"Lattitude": "lat", "Longtitude": "lon"}))

    st.write("Map displays properties that may be at higher flood risk due to low elevation and large land area.")
