# -*- coding: utf-8 -*-
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
from dash.dependencies import Input, Output
from flask import send_from_directory
import os

from functions import *
json_filename = '2018.1_SA.json'
ical_filename = '2018.1_SA_ical.json'
column_widths = [100, 300, 160, 90, 65] + [160]*7 + [300]*2
df_selected   = pd.DataFrame([{}])

with open(json_filename, 'r') as file:
    json_data = json.load(file)
    df = convertJSONtoSheet(json_data).reset_index()

    app = dash.Dash(__name__, static_folder='static')
    server = app.server

    @server.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(server.root_path, 'static'),'logo.png', mimetype='image/png')
    html.Title('UFABC PDF 2 Sheets')

    app.scripts.append_script({
        "external_url": 'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js'
    })
    app.scripts.append_script({
        "external_url": '/static/scripts/dashboard.js'
    })
    app.css.append_css({
        "external_url": 'https://afeld.github.io/emoji-css/emoji.css'
    })
    app.css.append_css({
        "external_url": '/static/stylesheets/dashboard.css'
    })

    app.layout = html.Div([
        # html.Link(
        #     href = '/static/stylesheets/dashboard.css',
        #     rel  = 'stylesheet'
        # ),

        html.H1(
            'UFABC',
            id = 'title'
        ),
        html.H2(
            'Turmas e Salas',
            id = 'subtitle'
        ),

        dt.DataTable(
            id                   = 'select-table',
            rows                 = df.to_dict('records'),
            editable             = False,
            filterable           = True,
            row_selectable       = True,
            column_widths        = column_widths,
            row_height           = 30,
            max_rows_in_viewport = 20
        ),

        html.P(
            'Disciplinas selecionadas',
            className = 'centerDiv'
        ),
        dt.DataTable(
            id                   = 'list-table',
            columns              = df.columns,
            rows                 = [{}],
            editable             = False,
            column_widths        = column_widths,
            row_height           = 30,
            max_rows_in_viewport = 20
        ),

        html.Div([
            html.Button(
                'Exportar para o calendário',
                id = 'export-button'
            ),
        ], className = 'centerDiv'),

        html.Div(
            id    = 'footer',
            style = {'height': 75}
        ),
    ], className='container')

    @app.callback(
        Output('list-table', 'rows'),
        [Input('select-table', 'selected_row_indices')])
    def update_selected_row_indices(selected_row_indices):
        if selected_row_indices is None:
            return [{}]
        else:
            selected_row_indices.sort()
            global df_selected
            df_selected = df.iloc[selected_row_indices]
            return df_selected.to_dict('records')

    @app.callback(
        Output('footer', 'children'),
        [Input('export-button', 'n_clicks')])
    def export_button_click(n_clicks):
        # with open(ical_filename, 'w') as file:
        #     import json
        #     json.dump(df_selected.to_dict('records'), file)
        
        # with open(ical_filename, 'r') as file:
        #     import json
        #     json_data = json.load(file)
        #     from pprint import pprint
        #     pprint(json_data)
        #     pprint(json_data[0]['Subcódigo'])
        return None

    if __name__ == '__main__':
        app.run_server(debug=True)#, port=8080)
