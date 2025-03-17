import json
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import xml.etree.ElementTree as ET


tree = ET.parse(r'offerte/PO_Offerte_E_MLIBERO_20250317.xml')
root = tree.getroot()

app = Dash()

data = []
for offerta in root.iter('offerta'):
    company = offerta.find('IdentificativiOfferta/PIVA_UTENTE').text
    data.append({"company": company})
    

# Requires Dash 2.17.0 or later
app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(json.dumps(data), 'Company', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)

def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
