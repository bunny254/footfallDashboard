import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

# Sample sales data for two stores (replace this with your actual data loading code)
sales_data = pd.DataFrame({
    'Store': ['Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata Capital', 'Bata CD Outlet', 'Bata CD Outlet', 'Bata CD Outlet', 'Bata CD Outlet','Bata CD Outlet','Bata CD Outlet','Bata CD Outlet','Bata CD Outlet','Bata CD Outlet','Bata CD Outlet','Bata CD Outlet','Bata CD Outlet','Bata CD Outlet','Bata CD Outlet','Bata CD Outlet','Bata CD Outlet','Bata CD Outlet','Bata CD Outlet'],
    'Day': ['Sat 6', 'Sun 7', 'Mon 8', 'Tue 9','Wed 10','Thu 11', 'Fri 12', 'Sat 13', 'Sun 14', 'Mon 15', 'Tue 16', 'Wed 17', 'Thu 18', 'Fri 19', 'Sat 20', 'Sun 21', 'Mon 22', 'Tue 23', 'Sat 6', 'Sun 7', 'Mon 8', 'Tue 9','Wed 10','Thu 11', 'Fri 12', 'Sat 13', 'Sun 14', 'Mon 15', 'Tue 16', 'Wed 17', 'Thu 18', 'Fri 19', 'Sat 20', 'Sun 21', 'Mon 22', 'Tue 23'],
    'Sales': [377, 402, 319, 461,307,233,213,287,372,314,252,195,183,199,252,289,182,230, 483, 208, 339, 305, 206, 331, 396, 462, 197, 331, 321, 425, 298, 402, 553, 241, 300, 583]
})

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1(children="Good Morning, Welcome."),

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
        x=filtered_data['Day'],
        y=filtered_data['Sales'],
        mode='lines+markers',
        name='Sales'
    )
    layout = go.Layout(
        title='Weekly Foot Count for {}'.format(selected_store),
        xaxis={'title': 'Day'},
        yaxis={'title': 'Foot Count', 'zeroline': False, 'rangemode': 'tozero'}
    )
    return {'data': [trace], 'layout': layout}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)