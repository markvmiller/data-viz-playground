#%%
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing

#%%
# Sample synthetic data
# Create 24 months
months = pd.date_range(start='2023-01-01', periods=24, freq='M')

# Create sales for North (24 values)
north_sales = 200 + pd.Series(range(24)) * 5 + pd.Series(range(24)).apply(lambda x: 20 * (x % 2))

# Create sales for South (24 values)
south_sales = 150 + pd.Series(range(24)) * 3 + pd.Series(range(24)).apply(lambda x: 15 * (x % 3))

# Combine into single DataFrame
north_df = pd.DataFrame({'Month': months, 'Region': 'North', 'Sales': north_sales})
south_df = pd.DataFrame({'Month': months, 'Region': 'South', 'Sales': south_sales})

# Concatenate both regions
df = pd.concat([north_df, south_df], ignore_index=True)

display(df)
#%%
# Initialize app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1('Sales Forecast Dashboard'),
    
    html.Label('Select Region:'),
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': r, 'value': r} for r in df['Region'].unique()],
        value='North'
    ),
    
    html.Label('Forecast Horizon (Months):'),
    dcc.Slider(
        id='horizon-slider',
        min=1, max=12, step=1, value=6,
        marks={i: str(i) for i in range(1, 13)}
    ),
    
    dcc.Graph(id='forecast-graph')
])

# Callback
@app.callback(
    Output('forecast-graph', 'figure'),
    Input('region-dropdown', 'value'),
    Input('horizon-slider', 'value')
)
def update_forecast(region, horizon): #when an input in the above decorator changes, this runs
    # Filter data
    data = df[df['Region'] == region].set_index('Month')['Sales']
    
    # Fit model
    model = ExponentialSmoothing(data, trend='add', seasonal='add', seasonal_periods=12)
    fit = model.fit()
    forecast = fit.forecast(horizon)
    
    # Prepare plot
    fig = px.line()
    fig.add_scatter(x=data.index, y=data, mode='lines', name='Actual Sales')
    fig.add_scatter(x=forecast.index, y=forecast, mode='lines', name='Forecasted Sales')
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)

#check at: http://127.0.0.1:8050/
# %%
