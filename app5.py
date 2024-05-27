import dash
from dash import dcc, html
from datetime import datetime, timedelta
import plotly.graph_objs as go
import pandas as pd

# Read data from CSV file
sales_data = pd.read_csv('FootCounts_new.csv')

# Convert 'Date' column to datetime and then to date only
sales_data['Date'] = pd.to_datetime(sales_data['Date']).dt.date  # Convert to date only

# Initialize Dash app
app = dash.Dash(__name__)

# Function to get the time of day
def get_time_of_day():
    current_time = datetime.now().hour
    if 5 <= current_time < 12:
        return "Morning"
    elif 12 <= current_time < 17:
        return "Afternoon"
    else:
        return "Evening"

# Calculate the default date range (the most recent three days excluding today)
max_date = sales_data['Date'].max()
start_date = max_date - timedelta(days=2)
end_date = max_date

# Define layout
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'margin': '40px'}, children=[
    html.H1(children=f"Good {get_time_of_day()}, Welcome.", style={'textAlign': 'center'}),
    
    html.Div(children="Bata Store's Footfall Camera Reports Dashboard.", style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    html.Div([
        html.Label('Select Store:', style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='store-dropdown',
            options=[{'label': store, 'value': store} for store in sales_data['Store'].unique()],
            value=sales_data['Store'].unique()[0],  # Default selected store
            style={'width': '50%', 'marginBottom': '20px'}
        ),
    ], style={'textAlign': 'center'}),
    
    html.Div([
        html.Label('Select Date Range:', style={'fontWeight': 'bold'}),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=start_date,
            end_date=end_date,
            display_format='YYYY-MM-DD',
            style={'marginBottom': '20px'}
        ),
        html.Button('Reset Date Range', id='reset-date-range', n_clicks=0, style={'marginLeft': '10px'})
    ], style={'textAlign': 'center'}),

    dcc.Graph(id='sales-graph')
])

# Define callback to update graph
@app.callback(
    [dash.dependencies.Output('sales-graph', 'figure'),
     dash.dependencies.Output('date-picker-range', 'start_date'),
     dash.dependencies.Output('date-picker-range', 'end_date')],
    [dash.dependencies.Input('store-dropdown', 'value'),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('reset-date-range', 'n_clicks')]
)
def update_graph(selected_store, start_date, end_date, n_clicks):
    ctx = dash.callback_context

    # Check if the reset button was clicked
    if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0] == 'reset-date-range':
        start_date = sales_data['Date'].max() - timedelta(days=2)
        end_date = sales_data['Date'].max()

    # Ensure start_date and end_date are datetime.date objects
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Filter data based on selected store and date range
    filtered_data = sales_data[
        (sales_data['Store'] == selected_store) &
        (sales_data['Date'] >= start_date) &
        (sales_data['Date'] <= end_date)
    ]

    # Prepare data for plotting
    trace = go.Scatter(
        x=filtered_data['Date'],
        y=filtered_data['Foot Count'],
        mode='lines+markers',
        name='Foot Count',
        line=dict(color='rgb(255, 127, 14)', width=2),
        marker=dict(symbol='diamond', size=6, color='rgb(31, 119, 180)', line=dict(width=1, color='rgb(31, 119, 180)'))
    )

    layout = go.Layout(
        title='Foot Count for {}'.format(selected_store),
        xaxis={'title': 'Date', 'tickangle': -45, 'tickfont': dict(size=12)},
        yaxis={'title': 'Foot Count', 'zeroline': False, 'rangemode': 'tozero', 'tickfont': dict(size=12)},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgb(255, 255, 255)',
        font=dict(family='Arial, sans-serif', size=14, color='rgb(50, 50, 50)'),
    )
    return {'data': [trace], 'layout': layout}, start_date, end_date

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
