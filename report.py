from dash import Dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from helper import generate_data, get_report
from layout import layout

import time
import json
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


app.layout = layout
server = app.server


@app.callback([Output('table', 'data'), Output('store', 'data')], [Input('generate', 'n_clicks')])
def generate(n_clicks):
    records = generate_data()
    store_data = json.dumps(records)

    time.sleep(1)
    return records, store_data

@app.callback(Output('table-1', 'data'), [Input('store', 'data')])
def report(data):
    if not data:
        raise PreventUpdate

    time.sleep(1)
    store_data = json.loads(data)

    records = get_report(store_data)

    return records

    


if __name__ == '__main__':
    app.run_server(debug=True)