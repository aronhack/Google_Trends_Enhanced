#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 17:48:32 2020

@author: Aron
"""



# Worklist
# 1. Add loading icon



# -*- coding: utf-8 -*-
import os

import pandas as pd
import sys
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
# import dash_daq as daq
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame

import plotly.graph_objs as go

local = False
local = True


# Path .....
if local == True:
    path = '/Users/Aron/Documents/GitHub/Data/Google_Trends_Enhanced'
else:
    path = '/home/aronhack/google_trends_enhanced'
    # path = '/home/aronhack/stock_analysis_us/dashboard'


# Codebase ......
path_codebase = [r'/Users/Aron/Documents/GitHub/Arsenal/',
                 r'/Users/Aron/Documents/GitHub/Codebase_YZ',
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


# Iniitialize ......
app = dash.Dash()
df_memory = pd.DataFrame({'DATE':[], 'VALUE':[]})
df_memory_dict = df_memory.to_dict()


# fig = go.Figure(go.Scatter(x=df_memory['DATE'], 
#                    y=df_memory['VALUE'],
#                    mode='lines',
#                    name=''))





# %% Style ------
colors = {
    'background': '#f5f5f5',
    'text': '#303030'
}



# Style ......

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

        dcc.DatePickerRange(id='calendar', display_format='Y-M-D', 
                            style=date_picker),
        
        dcc.Input(id="word_input", type="text", 
                  placeholder="使用逗號分隔關鍵字，如「台股,美股,比特幣」",
                  style=word_input_style),
        
        html.Button('Search', id='submit_btn', 
                    n_clicks=0, value=0, style=btn_style),
        
        html.Button('Download', id='download_btn', 
                    n_clicks=0, value=0, style=btn_style),
        
        Download(id="download"),
        dcc.Graph(id="graph"),
        
    ],  
)



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
    
    # 1. Add Loading icon
    
    if begin_date == None or end_date == None or words == None:
        raise PreventUpdate

       
    # Query        
    begin_date_lite = cbyz.date_simplify(begin_date)
    end_date_lite = cbyz.date_simplify(end_date)            
    
    # words = words.split(', ')
    words = words.split(',')
    
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
        

    return fig, trend_data_dict


# .................


@app.callback(
    Output('download', 'data'),
    Input('download_btn', 'n_clicks'),
    State('df_memory', 'data'),
    prevent_initial_call=True,        
)


def donwload_file(_download_clicks, _df_memory):
    # 1. 20210607 - Download csv, not published yet
    # https://dash.plotly.com/dash-core-components/download    
    
    # if _download_clicks > _download_value:
        
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
    send_frame = \
        send_data_frame(results.to_excel, 
                        "goole_trends_enhanced" + time_serial \
                        + ".xlsx", index=False) 
    
    return send_frame
    




if __name__ == '__main__':
    app.run_server()
    # app.run_server(debug=True)






