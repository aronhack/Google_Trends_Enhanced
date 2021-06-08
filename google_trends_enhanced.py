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
# from flask import Flask, request
from flask_caching import Cache


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
    global trend_words, trend_data    
    
    if 'trend_data' not in globals() or debug == False:
        
        print(words)
        
        trend_words = words
        trend_data = cbyz.pytrends_multi(begin_date=begin_date, 
                                         end_date=end_date, 
                                         chunk=180, unit='d',
                                         words=words, hl='zh-TW', geo='TW')
        
        # return trend_words, trend_data


def master():
    '''
    主工作區
    '''
    
    global submit_clicks, download_clicks
    submit_clicks = 0
    download_clicks = 0
    
    
    global trend_words, trend_data
    trend_data = pd.DataFrame({'DATE':[], 'VALUE':[]}) 
    trend_words = []
    
    return ''



def check():
    '''
    資料驗證
    '''    
    return ''




# %% Application ----

master()
app = dash.Dash()


if local == False:
    cache = Cache(app.server, config={
        # try 'filesystem' if you don't want to setup redis
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': os.environ.get('REDIS_URL', '')
    })
    app.config.suppress_callback_exceptions = True
    


# Style ......
colors = {
    'background': '#f5f5f5',
    'text': '#303030'
}


file_path = path_temp_user + '/file_20210607_221318.csv'


date_picker = {
    'display': 'black'    
}


app.layout = \
    html.Div([
        html.Div(id='debug'),

        dcc.DatePickerRange(id='calendar', display_format='Y-M-D', 
                            style=date_picker),
        dcc.Input(id="word_input", type="text", placeholder=""),
        html.Button('Submit', id='submit_btn', n_clicks=0),
        
        html.Button('Download', id='download_btn', n_clicks=0),   
        Download(id="download"),
        
        
        html.Div(id="line_chart"),
    ],  
)



@app.callback(
    [Output('line_chart', 'children'),
      Output('debug', 'children')
      ],
    [Input('calendar', 'start_date'),
     Input('calendar', 'end_date'),
     Input('word_input', 'value'),
     Input('submit_btn', 'n_clicks')
      ]    
)



def update_output(begin_date, end_date, words, _submit_clicks):

    # 1. Loading 

    
    
    global trend_data, trend_wods, submit_clicks
    

    # words = ['疫苗', '確診', '陳時中', '家樂福', '大潤發', 'Uber Eats', 'Foodpanda',
    #           '全聯', '愛買', '全家', '好市多', '封城', '台股', '比特幣', '美股']
    
    
    if begin_date != None and end_date != None:
        
        begin_date_lite = cbyz.date_simplify(begin_date)
        end_date_lite = cbyz.date_simplify(end_date)
    
        if _submit_clicks > submit_clicks and words != None:
            
            
            print(begin_date_lite, end_date_lite)
            
            words = words.split(',')
            print(words)
            
            load_data(begin_date=begin_date_lite, end_date=end_date_lite, 
                      words=words, debug=False)
            
            submit_clicks = _submit_clicks
            
        # else:
        #     words, data = load_data(begin_date=begin_date_lite, 
        #                             end_date=end_date_lite, 
        #                             words=words, debug=True)




    data1 = [{'x': trend_data[trend_data['VARIABLE']==i]['DATE'],
              'y': trend_data[trend_data['VARIABLE']==i]['VALUE'],
              'type': 'line',
              'name': i,
              } for i in trend_words]
              
    
    plot =  dcc.Graph(
                            id='trend_plot',
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


    return figure, words





@app.callback(
    Output('download', 'data'),
    [Input('download_btn', 'n_clicks')]    
)


def donwload_file(_download_clicks):


    # 1. 20210607 - Download csv, not published yet
    # https://dash.plotly.com/dash-core-components/download    
    
    global trend_data, download_clicks

    if _download_clicks > download_clicks:

    # df = pd.DataFrame({'a': [1, 2, 3, 4], 'b': [2, 1, 5, 6], 'c': ['x', 'x', 'y', 'y']})        
        
    #     serial = cbyz.get_time_serial(with_time=True)
    #     # trend_data.to_csv(path_user_temp + '/file_' + serial + '.csv',
    #     #                   index=False, encoding='utf-8-sig')
        
    #     # file_path = path_temp_user + '/file_20210607_221318.csv'
        
    #     # dcc.send_data_frame(trend_data.to_csv, 
    #     #                     path_temp_user + '/file_' + serial + '.csv')
    #     print('download')    
    #     download_clicks = _download_clicks    
    
        return send_data_frame(trend_data.to_csv, "mydf.csv", index=False)




if __name__ == '__main__':
    app.run_server()
    # app.run_server(debug=True)






