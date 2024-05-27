import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

# Sample sales data (replace this with your actual data loading code)
sales_data = pd.DataFrame({
    'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    'Sales': [10000, 12000, 15000, 11000]
})

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1(children="Good Morning, Welcome."),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    
    dcc.Dropdown(
        id='store-dropdown',
        options=[
            {'label': 'Store 1', 'value': 'Store 1'},
            {'label': 'Store 2', 'value': 'Store 2'}
            # Add more stores if needed
        ],
        value='Store 1'  # Default selected store
    ),
    dcc.Graph(id='sales-graph')
])

# Define callback to update graph
@app.callback(
    dash.dependencies.Output('sales-graph', 'figure'),
    [dash.dependencies.Input('store-dropdown', 'value')]
)
def update_graph(selected_store):
    # Sample data manipulation (replace with your actual data filtering code)
    filtered_data = sales_data  # You may filter the data based on selected_store
    # Prepare data for plotting
    trace = go.Scatter(
        x=filtered_data['Week'],
        y=filtered_data['Sales'],
        mode='lines+markers',
        name='Sales'
    )
    layout = go.Layout(
        title='Weekly Sales for {}'.format(selected_store),
        xaxis={'title': 'Week'},
        yaxis={'title': 'Sales'}
    )
    return {'data': [trace], 'layout': layout}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)