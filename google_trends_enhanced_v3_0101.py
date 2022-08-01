#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 17:48:32 2020

@author: Aron
"""

# Worklist
# 1. Add loading icon


# -*- coding: utf-8 -*-
import pandas as pd
import sys
import time
from datetime import date

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


import plotly.graph_objs as go

local = False
# local = True


# Path .....
if local:
    path = r'/Users/aron/Documents/GitHub/Google_Trends_Enhanced'
else:
    path = '/home/aronhack/google_trends_enhanced'
    # path = '/home/aronhack/stock_analysis_us/dashboard'


# Codebase ......
path_codebase = [r'/Users/Aron/Documents/GitHub/Arsenal/',
                 r'/Users/Aron/Documents/GitHub/Codebase',
                 path + '/Function']


for i in path_codebase:    
    if i not in sys.path:
        sys.path = [i] + sys.path


import codebase_yz as cbyz
import arsenal as ar


# 自動設定區 -------
pd.set_option('display.max_columns', 30)
 

# 新增工作資料夾
path_resource = path + '/Resource'
path_function = path + '/Function'
path_temp = path + '/Temp'
path_temp_user = path + '/Temp_User'
path_export = path + '/Export'


cbyz.os_create_folder(path=[path_resource, path_function, 
                            path_temp, path_temp_user, path_export])




def load_data(begin_date, end_date, words=[], debug=False):
    '''
    讀取資料及重新整理
    '''
    
    words = cbyz.conv_to_list(words)
    

    # Pytrend .....
    
    if debug == False:
        trend_words = words
        trend_data = cbyz.pytrends_multi(begin_date=begin_date, 
                                         end_date=end_date, 
                                         chunk=180, unit='d',
                                         words=words, hl='zh-TW', geo='TW')
        
        return trend_words, trend_data
        


# %% Application ----

# Running a Dash app within a Flask app
# https://stackoverflow.com/questions/45845872/running-a-dash-app-within-a-flask-app

import flask
server = flask.Flask(__name__)

external_stylesheets = [dbc.themes.BOOTSTRAP,
                        'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, server=server, 
                external_stylesheets=external_stylesheets)

df_memory_dict = pd.DataFrame({'DATE':[], 'VALUE':[]}).to_dict()


# @server.after_request
# def apply_caching(response):
#     # response.headers["X-Frame-Options"] = "SAMEORIGIN"
#     response.headers["X-Frame-Options"] = "DENY"
#     # response.headers["X-Frame-Options"] = "ALLOW-FROM aronhack.com"
#     # response.headers["X-Frame-Options"] = "ALLOW-FROM aronhack.studio"
    
#     # response.headers["Access-Control-Allow-Origin"] = "*"
#     return response



# %% Style ------
colors = {
    'background': '#f5f5f5',
    'text': '#303030'
}


# CSS ......
date_picker = {
    'display': 'block'    
    }

word_input_style = {
    'height': '35px',
    'width': '40%',
    'display': 'block',
    'margin': '16px 0'
    }

btn_style = {
    'margin-right': '10px',
    'margin-bottom': '16px'
    }


app.layout = \
    html.Div([
        html.Div(id='debug'),
        dcc.Store(id='df_memory', data=df_memory_dict),

        dcc.DatePickerRange(id='calendar', 
                            start_date=date(2022, 1, 16),
                            end_date=date(2022, 1, 20),
                            min_date_allowed=date(2011, 1, 1),
                            max_date_allowed=date(2025, 12, 31),
                            display_format='Y-M-D', 
                            # with_portal=True, 
                            style=date_picker),
        
        dcc.Textarea(id="word_input",
                     placeholder="換行以區分關鍵字",
                     style=word_input_style),
        
        html.Button('Search', id='submit_btn', 
                    n_clicks=0, value=0, style=btn_style),
        
        html.Button('Download', id='download_btn', 
                    n_clicks=0, value=0, style=btn_style),
        
        dcc.Download(id="download"),
        
        dcc.Loading(
            id="loading-1",
            type="default",
            children=dcc.Graph(id="graph")
        ),
        
        html.Div([html.Span(['Powered by ',
                            html.A('PythonAnywhere', 
                                   href='https://aronhack.studio/pythonanywhere_dash',
                                   target='_blank',
                                   className='text-decoration-none')
                            ]),
                 ],
                 className='text-center')
        
    ],  
)


# @app.after_request
# def apply_caching(response):
#     response.headers["X-Frame-Options"] = "SAMEORIGIN"
#     return response


# %% Callback ------

@app.callback(
    Output('graph', 'figure'),
    Output('df_memory', 'data'),
    Input('submit_btn', 'n_clicks'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('word_input', 'value')
)


def update_output(_submit_clicks, begin_date, end_date, words):
    
    
    if begin_date == None or end_date == None or words == None:
        raise PreventUpdate


    # Query        
    begin_date_lite = cbyz.date_simplify(begin_date)
    end_date_lite = cbyz.date_simplify(end_date)            
    
    words = words.split('\n')
    trend_words, trend_data = load_data(begin_date=begin_date_lite, 
                                        end_date=end_date_lite, 
                                        words=words, debug=False)

    # Cache ......
    trend_data_dict = \
        [{'date': trend_data[trend_data['VARIABLE']==i]['DATE'],
          'value': trend_data[trend_data['VARIABLE']==i]['VALUE'],
          'type': 'line',
          'name': i,
          } for i in trend_words]            

  
    # Figure ......
    fig = go.Figure()
    
    for w in trend_words:
        temp_date = trend_data[trend_data['VARIABLE']==w]
        trace = go.Scatter(x=temp_date['DATE'], 
                           y=temp_date['VALUE'],
                           mode='lines',
                           name=w)

        fig.add_trace(trace)
        

    time.sleep(1)
    return fig, trend_data_dict


# .................


@app.callback(
    Output('download', 'data'),
    Input('download_btn', 'n_clicks'),
    State('df_memory', 'data'),
    prevent_initial_call=True,        
)


def donwload_file(_download_clicks, _df_memory):
    
        
    time_serial = cbyz.get_time_serial(with_time=True)
    
    # Convert nested dict to dataframe ......
    results = pd.DataFrame()

    
    # Prevent errors
    if len(_df_memory[0]['date']) == 0:
        raise PreventUpdate    
    
    
    for i in _df_memory:
        temp = pd.DataFrame(i)
        results = results.append(temp)
    
    results.columns = ['Date', 'Value', 'Type', 'Word']
    results = results[['Date', 'Word', 'Value']]
 
    # Export ......        
    send_frame = dcc.send_data_frame(
        results.to_excel, 
        "aron_hack-goole_trends_enhanced_" + time_serial + ".xlsx"
        )    
    
    return send_frame


# %% Execute ------

def version_note():
    '''
    主工作區
    '''
    # v3.0100
    # - Add PythonAnywhere affiliate link
    # v3.0101
    # - Replace Download with new function
    # - Replace input as textarea, and split by enter
    # - Add X-Frame-Options
    
    
    # Worklist
    # - Disable embeding
    #  https://stackoverflow.com/questions/30717152/python-flask-how-to-set-response-header-for-all-responses
    #  https://stackoverflow.com/questions/40937527/disable-iframe-embedding-for-other-websites

    # - pytrends.exceptions.ResponseError: The request failed: Google returned
    #   a response with code 400.
    #   https://stackoverflow.com/questions/70529087/getting-google-returned-a-response-with-code-400-error-in-pytrend
    pass




if __name__ == '__main__':
    app.run_server()
    # app.run_server(debug=True)






