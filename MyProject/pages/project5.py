import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv('./pages/New_povertyrate')  # Make sure it ends with .csv

# Manually add 'Year' column (assuming 1985–1985+len(df))
df['Year'] = list(range(1985, 1985 + len(df)))

# Move 'Year' to front
cols = ['Year'] + [col for col in df.columns if col != 'Year']
df = df[cols]

# Convert all columns (except 'Year') to numeric (if needed)
for col in df.columns:
    if col != 'Year':
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Layout in two tabs
tab1, tab2 = st.tabs(["Dataset", "Visualisation"])

# --- Tab 1: Show the Cleaned Data ---
with tab1:
    st.header("Cleaned Poverty Dataset")
    st.dataframe(df)

# --- Tab 2: Scatter Plot Visualisation ---
with tab2:
    st.header("Scatter Plot of Poverty Rate vs Year")

    # Filter out unrealistic or missing data
    data = df[(df['Year'] >= 1900) & (df['Year'] <= 2025)]
    data = data[data['Poverty_Ra'].notna()]

    fig, ax = plt.subplots()
    ax.scatter(data["Year"], data["Poverty_Ra"], color='royalblue')
    ax.set_title("Poverty Rate over Years")
    ax.set_xlabel("Year")
    ax.set_ylabel("Poverty_Ra")
    st.pyplot(fig)
