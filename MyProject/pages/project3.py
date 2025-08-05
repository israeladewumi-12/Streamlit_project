import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Melbourne Housing Explorer", layout="wide")

st.title(" Melbourne Housing Market Analysis")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("./MyProject/pages/New_Melbourn_Less")
    return df

data = load_data()
data_clean = data.dropna(subset=["Price"])

# --- Tabs ---
tab1, tab2 = st.tabs(["  Data", " Data and Visuals"])

# === TAB 1: ORIGINAL DATA ===
with tab1:
    st.subheader("Raw Melbourne Housing Data")
    st.write(f" Shape: {data.shape}")
    st.dataframe(data.head())

    total_price = data["Price"].sum()
    st.metric(" Total Price", f"${total_price:,.2f}")

# === TAB 2: CLEANED DATA AND VISUALIZATIONS ===
with tab2:
    st.subheader("Cleaned_Data Price Values)")
    st.write(f"Shape: {data_clean.shape}")
    st.dataframe(data_clean.head())

    cleaned_total_price = data_clean["Price"].sum()
    st.metric(" Total Price (Cleaned)", f"${cleaned_total_price:,.2f}")

    # --- Visualization 1: Price Distribution ---
    st.markdown("Price Distribution")
    fig1, ax1 = plt.subplots()
    ax1.hist(data_clean["Price"], bins=30, color='skyblue', edgecolor='black')
    ax1.set_title("Distribution of Property Prices")
    ax1.set_xlabel("Price ($)")
    ax1.set_ylabel("Number of Properties")
    st.pyplot(fig1)

    # --- Visualization 2: Avg Price by Bedroom Count ---
    # st.markdown("Average Price by Number of Bedrooms")
    # if "Bedroom2" in data_clean.columns:
    #     avg_price_by_beds = data_clean.groupby("Bedroom2")["Price"].mean().reset_index()
    #     fig2, ax2 = plt.subplots()
    #     ax2.bar(avg_price_by_beds["Bedroom2"], avg_price_by_beds["Price"], color='green')
    #     ax2.set_title("Average Price vs Bedrooms")
    #     ax2.set_xlabel("Number of Bedrooms")
    #     ax2.set_ylabel("Average Price ($)")
    #     st.pyplot(fig2)
    # else:
    #     st.warning("")
