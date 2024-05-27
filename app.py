# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    'Category': ['Std Stock', 'April', 'May'],
    'Stocks': [10, 47, 60]
})

fig = px.bar(df, x="Category", y="Stocks", color="Category")

app.layout = html.Div(children=[
    html.H1(children="Hello there, Welcome."),

    html.Div(children='''
        WIP: Factory Trends 2024.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)
