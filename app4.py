import dash
from dash import dcc, html
from datetime import datetime
import plotly.graph_objs as go
import pandas as pd

# Read data from CSV file
sales_data = pd.read_csv('FootCounts_new.csv')



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

# Define layout
app.layout = html.Div([
    html.H1(children=f"Good {get_time_of_day()}, Welcome."),

    html.Div(children='''
        Bata Store's Footfall Camera Reports Dashboard.
    '''),
    
    dcc.Dropdown(
        id='store-dropdown',
        options=[
            {'label': store, 'value': store} for store in sales_data['Store'].unique()
        ],
        value=sales_data['Store'].unique()[0]  # Default selected store
    ),
    dcc.Graph(id='sales-graph')
])

# Define callback to update graph
@app.callback(
    dash.dependencies.Output('sales-graph', 'figure'),
    [dash.dependencies.Input('store-dropdown', 'value')]
)
def update_graph(selected_store):
    # Filter data based on selected store
    filtered_data = sales_data[sales_data['Store'] == selected_store]
    
    # Prepare data for plotting
    trace = go.Scatter(
        x=filtered_data['Date'],
        y=filtered_data['Foot Count'],  # Assuming you want to plot foot count
        mode='lines+markers',
        name='Foot Count',
        line=dict(color='rgb(255, 127, 14)', width=2),  # Custom line style
        marker=dict(symbol='diamond', size=4, color='rgb(31, 119, 180)', line=dict(width=1, color='rgb(31, 119, 180)'))  # Custom marker style
    )
    layout = go.Layout(
        title='Weekly Foot Count for {}'.format(selected_store),
        xaxis={'title': 'Date', 'tickangle': -45, 'tickfont': dict(size=12)},
        yaxis={'title': 'Foot Count', 'zeroline': False, 'rangemode': 'tozero','tickfont': dict(size=12)},
        plot_bgcolor='rgba(0,0,0,0)',  # Set transparent plot background
        paper_bgcolor='rgb(255, 255, 255)',  # Set paper background color
        font=dict(family='Arial, sans-serif', size=14, color='rgb(50, 50, 50)'),  # Custom font style
    )
    '''
    layout = go.Layout(
    title='Weekly Foot Count for {}'.format(selected_store),
    xaxis={'title': 'Date', 'tickangle': -45, 'tickfont': dict(size=12)},  # Adjust angle and font size of x-axis ticks
    yaxis={'title': 'Foot Count', 'zeroline': False, 'rangemode': 'tozero', 'tickfont': dict(size=12)},  # Adjust font size of y-axis ticks
    plot_bgcolor='rgba(0,0,0,0)',  # Set transparent plot background
    paper_bgcolor='rgb(255, 255, 255)',  # Set paper background color
    font=dict(family='Arial, sans-serif', size=14, color='rgb(50, 50, 50)'),  # Custom font style
    margin=dict(l=50, r=50, t=70, b=50),  # Adjust margins
    legend=dict(font=dict(size=12), orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)  # Adjust legend position and font size
)
'''
    return {'data': [trace], 'layout': layout}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
