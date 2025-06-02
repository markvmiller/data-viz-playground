import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# ========== 1️⃣ Initialize App ==========
app = dash.Dash(__name__)

# Sample or real dataset
df = pd.read_csv('your_data.csv')  # or replace with synthetic data

# ========== 2️⃣ Define Layout ==========
app.layout = html.Div([
    html.H1('My Data Science Dashboard'),

    html.Label('Select Category:'),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': cat, 'value': cat} for cat in df['category_column'].unique()],
        value=df['category_column'].unique()[0]
    ),

    html.Label('Select Numeric Parameter:'),
    dcc.Slider(
        id='num-slider',
        min=1, max=100, step=1, value=10,
        marks={i: str(i) for i in range(1, 101, 10)}
    ),

    dcc.Graph(id='main-graph'),

    html.Div(id='summary-output', style={'marginTop': 20})
])

# ========== 3️⃣ Define Callback ==========
@app.callback(
    Output('main-graph', 'figure'),
    Output('summary-output', 'children'),
    Input('category-dropdown', 'value'),
    Input('num-slider', 'value')
)
def update_outputs(selected_category, num_value):
    # Filter or process data
    filtered_df = df[df['category_column'] == selected_category]

    # Example: take top N rows
    top_df = filtered_df.nlargest(num_value, 'numeric_column')

    # Example figure (change to fit your use case)
    fig = px.bar(top_df, x='x_column', y='numeric_column', title='Top Items')

    # Example summary text
    summary_text = f"Showing top {num_value} items for category '{selected_category}'."

    return fig, summary_text

# ========== 4️⃣ Run App ==========
if __name__ == '__main__':
    app.run(debug=True)
