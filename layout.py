from dash import Dash, html, dash_table, dcc, callback_context
import dash_bootstrap_components as dbc

layout = html.Div(
    [
        html.H1('Signifyd Account History Report', style=dict(textAlign='center', padding='1rem')),
        html.Div(
            [
                dbc.Button('Generate User Data', style=dict(marginLeft='0.5rem'), id='generate')
            ], 
            style=dict(display='flex', justifyContent='center')
        ),
        html.Div([
                html.Div([
                    html.H3('Mock Data', style=dict(textAlign='left', margin='1rem')),
                    html.H3('Report', style=dict(textAlign='left', margin='1rem'))
                ], style=dict(display='flex', alignItems='center', justifyContent='space-around')),
                
                html.Div([
                    dcc.Loading(dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} 
                                for i in ['Date', 'Email', 'Event']],
                        css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                        style_cell=dict(textAlign='center', width='40%'),
                        style_header=dict(backgroundColor='black', fontSize='20px', fontFamily='Arial', fontWeight='bold'),
                        style_data=dict(backgroundColor='black', fontSize='16px', fontFamily='Arial', fontWeight='thin'),
                        style_table=dict(padding='1rem')
                    )),
                    dcc.Loading(dash_table.DataTable(
                        id='table-1',
                        columns=[{"name": i, "id": i} 
                                for i in ['Date', 'Email', 'Status']],
                        css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                        style_cell=dict(textAlign='center', width='40%'),
                        style_header=dict(backgroundColor='black', fontSize='20px', fontFamily='Arial', fontWeight='bold'),
                        style_data=dict(backgroundColor='black', fontSize='16px', fontFamily='Arial', fontWeight='thin'),
                        style_table=dict(padding='1rem'),
                        style_data_conditional=[
                            {
                                'if': {
                                    'filter_query': '{Status} contains "FRAUD_HISTORY"'
                                },
                                'backgroundColor': 'red',
                                'color': 'white'
                            },
                            {
                                'if': {
                                    'filter_query': '{Status} contains "GOOD HISTORY"'
                                },
                                'backgroundColor': 'green',
                                'color': 'white'
                            },
                            {
                                'if': {
                                    'filter_query': '{Status} contains "UNCONFIRMED_HISTORY"'
                                },
                                'backgroundColor': 'darkGray',
                                'color': 'white'
                            }
                        ]
                    )),
                ], style=dict(display='flex', alignItems='flex-start'))
        ], style=dict(display='flex', flexDirection='column', alignItems='flex', justifyContent='center')),
        

        dcc.Store(id='store')
    ]
)