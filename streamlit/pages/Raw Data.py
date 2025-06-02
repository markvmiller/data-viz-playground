import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Raw Data")

st.title("📄 Raw Mock Data")

# Load the same cached data
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=100)
    sales = np.random.poisson(lam=100, size=100)
    profit = np.random.normal(loc=20, scale=5, size=100)
    category = np.random.choice(['A', 'B', 'C'], size=100)

    df = pd.DataFrame({
        'Date': dates,
        'Sales': sales,
        'Profit': profit,
        'Category': category
    })
    df['Cumulative Sales'] = df['Sales'].cumsum()
    return df

df = load_data()

# Show raw data
st.dataframe(df)

# Optional: let user download data
st.download_button("Download CSV", df.to_csv(index=False), "mock_data.csv", "text/csv")
