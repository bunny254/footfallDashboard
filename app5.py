import dash
from dash import dcc, html
from datetime import datetime, timedelta, date
import plotly.graph_objs as go
import pandas as pd

# Read data from CSV file
sales_data = pd.read_csv('FootCounts_new.csv')

# Convert 'Date' column to datetime and then to date only
sales_data['Date'] = pd.to_datetime(sales_data['Date']).dt.date  # Convert to date only

# List of public holidays in Kenya for 2024
public_holidays = [
    date(2024, 1, 1),   # New Year's Day
    date(2024, 4, 12),  # Good Friday
    date(2024, 4, 15),  # Easter Monday
    date(2024, 5, 1),   # Labour Day
    date(2024, 6, 1),   # Madaraka Day
    date(2024, 6, 16),  # Eid al-Fitr
    date(2024, 10, 20), # Mashujaa Day
    date(2024, 12, 12), # Jamhuri Day
    date(2024, 12, 25), # Christmas Day
    date(2024, 12, 26)  # Boxing Day
]

# Define an ordered list of store names with preferred stores first
preferred_store_order = [
    'Bata Hilton',  # Replace with actual store names 
    'Bata Jubilee',
    'Bata Tom Mboya Mega',
    'Bata Sarit Centre',
    'Bata Tropical Craft',
    'Bata CD Outlet',
    'Bata Kitengela One',
    'Bata Thika Road Mall'
]

# Add the remaining stores that are not in the preferred list
remaining_stores = [store for store in sales_data['Store'].unique() if store not in preferred_store_order]
store_order = preferred_store_order + remaining_stores

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# Function to get the time of day
def get_time_of_day():
    current_time = datetime.now().hour
    if 5 <= current_time < 12:
        return "Morning"
    elif 12 <= current_time < 17:
        return "Afternoon"
    else:
        return "Evening"

# Calculate the default date range (the most recent three months excluding today)
max_date = datetime.now().date() - timedelta(days=1)
start_date = max_date - timedelta(days=90)  # Approximately three months back
end_date = max_date

# Define layout
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'margin': '40px'}, children=[
    html.H1(children=f"Good {get_time_of_day()}, Welcome.", style={'textAlign': 'center'}),
    
    html.Div(children="Bata Store's Footfall Camera Reports Dashboard.", style={'textAlign': 'center', 'marginBottom': '20px'}),
    
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

    html.Div(id='graphs-container', style={'height': '80vh', 'overflowY': 'scroll', 'border': '1px solid #ccc', 'padding': '10px'}),

    html.Div([
        "Built by ",
        html.A("Simon Wachira", href="https://simonwachira.com", style={'font-style': 'italic', 'font-weight': '600'})
    ], style={'marginTop': '40px', 'textAlign': 'center'}) 
])

# Define callback to update graph
@app.callback(
    [dash.dependencies.Output('graphs-container', 'children'),
     dash.dependencies.Output('date-picker-range', 'start_date'),
     dash.dependencies.Output('date-picker-range', 'end_date')],
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('reset-date-range', 'n_clicks')]
)
def update_graph(start_date, end_date, n_clicks):
    ctx = dash.callback_context

    # Check if the reset button was clicked
    if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0] == 'reset-date-range':
        start_date = max_date - timedelta(days=60)
        end_date = max_date

    # Ensure start_date and end_date are datetime.date objects
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    graphs = []
    
    for store in store_order:
        # Filter data based on store and date range
        filtered_data = sales_data[
            (sales_data['Store'] == store) &
            (sales_data['Date'] >= start_date) &
            (sales_data['Date'] <= end_date)
        ]

        # Create a complete date range to ensure all dates are covered in the plot
        date_range = pd.date_range(start=start_date, end=end_date).date
        complete_data = pd.DataFrame(date_range, columns=['Date']).merge(
            filtered_data, on='Date', how='left'
        )

        # Replace zeros with None
        complete_data['Foot Count'] = complete_data['Foot Count'].replace(0, None)

        # Prepare data for plotting
        trace = go.Scatter(
            x=complete_data['Date'],
            y=complete_data['Foot Count'],
            mode='lines+markers',
            name='Foot Count',
            line=dict(color='rgb(255, 127, 14)', width=2, shape='spline'),  # Smoothed line
            marker=dict(symbol='diamond', size=6, color='rgb(31, 119, 180)', line=dict(width=1, color='rgb(31, 119, 180)'))
        )

        # Define a function to format the x-axis ticks
        def format_date(date):
            if date.weekday() >= 5 or date in public_holidays:
                return f'<b>{date.strftime("%d")}</b>'
            return date.strftime("%d")

        # Format the x-axis tick labels
        tickvals = [d.strftime("%Y-%m-%d") for d in date_range]
        ticktext = [format_date(d) for d in date_range]

        # Create annotations for the months
        annotations = []
        previous_month = None
        month_start_idx = 0
        for i, date in enumerate(date_range):
            if date.strftime("%b") != previous_month:
                if previous_month is not None:
                    month_end_idx = i - 1
                    mid_idx = (month_start_idx + month_end_idx) // 2
                    annotations.append(
                        dict(
                            x=date_range[mid_idx].strftime("%Y-%m-%d"),
                            y=-0.15,  # Adjusted position to be directly below the dates
                            xref='x',
                            yref='paper',
                            text=previous_month,
                            showarrow=False,
                            font=dict(size=14)
                        )
                    )
                month_start_idx = i
                previous_month = date.strftime("%b")

        # Add the last month annotation
        if previous_month is not None:
            month_end_idx = len(date_range) - 1
            mid_idx = (month_start_idx + month_end_idx) // 2
            annotations.append(
                dict(
                    x=date_range[mid_idx].strftime("%Y-%m-%d"),
                    y=-0.15,
                    xref='x',
                    yref='paper',
                    text=previous_month,
                    showarrow=False,
                    font=dict(size=14)
                )
            )

        layout = go.Layout(
            title=f'Foot Count for {store}',
            xaxis={
                'title': 'Date',
                'tickangle': -90,
                'tickfont': dict(size=12),
                'tickmode': 'array',
                'tickvals': tickvals,
                'ticktext': ticktext,
                'ticks': 'outside',
            },
            yaxis={'title': 'Foot Count', 'zeroline': False, 'rangemode': 'tozero', 'tickfont': dict(size=12)},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgb(255, 255, 255)',
            font=dict(family='Arial, sans-serif', size=14, color='rgb(50, 50, 50)'),
            width=1600,  # Adjusted width to fit better on the screen
            height=600,
            margin=dict(l=40, r=40, b=120, t=80),
            annotations=annotations
        )

        graph = dcc.Graph(
            id=f'sales-graph-{store}',
            figure={'data': [trace], 'layout': layout},
            style={'marginBottom': '40px'}
        )
        graphs.append(graph)

    return graphs, start_date, end_date

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
