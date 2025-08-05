import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Nigeria Poverty Rate", layout="wide")

st.title("🇳🇬 Poverty Rate Across Nigerian LGAs")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("./MyProject/pages/New_povertyrate")  # Make sure this path is correct

df = load_data()

# Create tabs
tab_data, tab_viz = st.tabs([" Data", "Visualisation"])

# Tab 1: Show data
with tab_data:
    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)
    st.markdown(f"**Total Rows:** {df.shape[0]} | **Total Columns:** {df.shape[1]}")

# Tab 2: Scatter plots
with tab_viz:
    st.subheader("Poverty Rate Visualisation")

    top10 = df.sort_values("Poverty_Ra", ascending=False).head(10)
    bottom10 = df.sort_values("Poverty_Ra").head(10)

    st.markdown("### Top 10 Most Affected LGAs")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.scatter(top10["NAME_23"], top10["Poverty_Ra"], color="red", s=100)
    ax1.set_title("Top 10 LGAs by Poverty Rate")
    ax1.set_ylabel("Poverty Rate (%)")
    ax1.set_xlabel("LGA")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    st.markdown("### Bottom 10 Least Affected LGAs")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.scatter(bottom10["NAME_23"], bottom10["Poverty_Ra"], color="green", s=100)
    ax2.set_title("Bottom 10 LGAs by Poverty Rate")
    ax2.set_ylabel("Poverty Rate (%)")
    ax2.set_xlabel("LGA")
    plt.xticks(rotation=45)
    st.pyplot(fig2)
