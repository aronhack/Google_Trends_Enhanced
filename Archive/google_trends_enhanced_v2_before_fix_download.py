#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 17:48:32 2020

@author: Aron
"""


# -*- coding: utf-8 -*-
import os

import pandas as pd
import sys
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
# import dash_daq as daq
from dash.dependencies import Input, Output


from dash_extensions import Download
from dash_extensions.snippets import send_data_frame


#import re
# from flask_caching import Cache


# from pytrends.request import TrendReq


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
        

def master():
    '''
    主工作區
    '''
    
    return ''



def check():
    '''
    資料驗證
    '''    
    return ''



# %% Application ----


# Iniitialize
# trend_data = pd.DataFrame({'DATE':[], 'VALUE':[]}) 
# trend_words = []    


master()
app = dash.Dash()


# if local == False:
#     cache = Cache(app.server, config={
#         # try 'filesystem' if you don't want to setup redis
#         'CACHE_TYPE': 'redis',
#         'CACHE_REDIS_URL': os.environ.get('REDIS_URL', '')
#     })
#     app.config.suppress_callback_exceptions = True
    


# Style ......
colors = {
    'background': '#f5f5f5',
    'text': '#303030'
}


# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

date_picker = {
    'display': 'black'    
}


df_memory_dict = pd.DataFrame({'DATE':[], 'VALUE':[]}).to_dict()



app.layout = \
    html.Div([
        html.Div(id='debug'),
        dcc.Store(id='df_memory', data=df_memory_dict),

        dcc.DatePickerRange(id='calendar', display_format='Y-M-D', 
                            style=date_picker),
        dcc.Input(id="word_input", type="text", placeholder=""),
        html.Button('查詢', id='submit_btn', n_clicks=0, value=0),
        
        html.Button('下載', id='download_btn', n_clicks=0, value=0),   
        Download(id="download"),
        
        
        # dcc.Graph(id='line_chart'),
        html.Div(id="line_chart"),
    ],  
)



# Bug, 加這個output時會出錯


@app.callback(
    [Output('line_chart', 'children'),
      Output('debug', 'children'),
      Output('submit_btn', 'value'),
      Output('df_memory', 'data'),
      ],
    [Input('calendar', 'start_date'),
     Input('calendar', 'end_date'),
     Input('word_input', 'value'),
     Input('submit_btn', 'n_clicks'),
     Input('submit_btn', 'value')
      ]    
)



def update_output(begin_date, end_date, words, _submit_clicks, _submit_value):

    # 1. Add Loading icon
    
    
    
    # print(_submit_clicks)
    # if submit_clicks == 0:
    
    #     trend_data = pd.DataFrame({'DATE':[], 'VALUE':[]}) 
    #     trend_words = []    

    # words = ['疫苗', '確診', '陳時中', '家樂福', '大潤發', 'Uber Eats', 'Foodpanda',
    #           '全聯', '愛買', '全家', '好市多', '封城', '台股', '比特幣', '美股']
    
    return_switch = False
    
    if begin_date != None and end_date != None:
        
        if _submit_clicks > _submit_value and words != None:
            
            begin_date_lite = cbyz.date_simplify(begin_date)
            end_date_lite = cbyz.date_simplify(end_date)            
            
            # words = words.split(', ')
            words = words.split(',')
            
            trend_words, trend_data = load_data(begin_date=begin_date_lite, 
                      end_date=end_date_lite, 
                      words=words, debug=False)
        
            # trend_data = trend_data.to_dict()
        
        
            submit_clicks = _submit_clicks
            submit_value = _submit_clicks
            
            switch = True
            print(words)
        
    # else:
    #     trend_data = pd.DataFrame({'DATE':[], 'VALUE':[]}) 
    #     trend_words = []    
        

    # if not return_switch:
    if 'trend_data' not in locals():
        trend_data = pd.DataFrame({'DATE':[], 'VALUE':[]})
        trend_words = []    


    if 'submit_value' not in locals():
        submit_value = _submit_value


    df_memofy_data = trend_data.to_dict()


    # 待優化 .......
    # 參考share data between callback中的Output('memory-graph', 'figure'),
    # https://dash.plotly.com/dash-core-components/store
    
    
    # Bug, data1可能為None
    data1 = [{'x': trend_data[trend_data['VARIABLE']==i]['DATE'],
              'y': trend_data[trend_data['VARIABLE']==i]['VALUE'],
              'type': 'line',
              'name': i,
              } for i in trend_words]
              
    
    plot =  dcc.Graph(id='trend_plot',
                      figure={
                          'data': data1,
                          'layout': {
                              'plot_bgcolor': colors['background'],
                              'paper_bgcolor': colors['background'],
                              'font': {
                                  'color': colors['text']
                                  },
                              }
                          },
                      )

    figure = [plot]


    # # Debug
    # debug_dropdown = '_'.join(dropdown_value)


    if not return_switch:
        pass
        
    return figure, '', submit_value, data1




@app.callback(
    [Output('download', 'data'),
     Output('download_btn', 'value')
    ],
    [Input('download_btn', 'n_clicks'),
     Input('download_btn', 'value')
     ]    
)


def donwload_file(_download_clicks, _download_value):


    # 1. 20210607 - Download csv, not published yet
    # https://dash.plotly.com/dash-core-components/download    
    

    if _download_clicks > _download_value:
        
        _download_value = _download_clicks

        time_serial = cbyz.get_time_serial(with_time=True)
        
        send_frame = \
            send_data_frame(trend_data.to_csv, 
                            "goole_trends_enhanced" + time_serial \
                            + ".csv", index=False)    
    
    
        return _download_value, send_frame




if __name__ == '__main__':
    app.run_server()
    # app.run_server(debug=True)






