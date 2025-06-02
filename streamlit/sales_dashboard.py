import streamlit as st
import pandas as pd
import numpy as np

st.title("Mock Data Visualization with Streamlit")

# Generate mock data
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

# Precompute
avg_profit = df.groupby('Category')['Profit'].mean()
df['Cumulative Sales'] = df['Sales'].cumsum()

# Create tabs
tab1, tab2, tab3 = st.tabs(["📈 Sales Over Time", "💰 Profit by Category", "📊 Cumulative Sales"])

with tab1:
    st.subheader("Sales Over Time")
    st.line_chart(df.set_index('Date')['Sales'])

with tab2:
    st.subheader("Average Profit by Category")
    st.bar_chart(avg_profit)

with tab3:
    st.subheader("Cumulative Sales Over Time")
    st.area_chart(df.set_index('Date')['Cumulative Sales'])

# Sidebar filter
st.sidebar.header("Filter Options")
selected_category = st.sidebar.selectbox("Select category:", df['Category'].unique())

filtered_df = df[df['Category'] == selected_category]
st.sidebar.write(f"Showing {len(filtered_df)} rows for category {selected_category}")

# Optional extra: show filtered data
st.sidebar.subheader("Filtered Sales Over Time")
st.sidebar.line_chart(filtered_df.set_index('Date')['Sales'])

# %%
