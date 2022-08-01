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
import dash_daq as daq
from dash.dependencies import Input, Output

#import re
#import numpy as np
# from flask import Flask, request
from flask_caching import Cache




local = False
local = True


# Path .....
if local == True:
    path = '/Users/Aron/Documents/GitHub/Data/Google_Trends_Enhanced/google_trends_enchanced.py'
else:
    path = '/home/aronhack/google_trends_enhanced'
    # path = '/home/aronhack/stock_analysis_us/dashboard'


# Codebase ......
path_codebase = [r'/Users/Aron/Documents/GitHub/Arsenal/',
                 r'/Users/Aron/Documents/GitHub/Codebase_YZ']


for i in path_codebase:    
    if i not in sys.path:
        sys.path = [i] + sys.path


import codebase_yz as cbyz
import arsenal as ar



# 自動設定區 -------
pd.set_option('display.max_columns', 30)
 


def initialize(path):

    # 新增工作資料夾
    global path_resource, path_function, path_temp, path_export
    path_resource = path + '/Resource'
    path_function = path + '/Function'
    path_temp = path + '/Temp'
    path_export = path + '/Export'
    
    
    cbyz.create_folder(path=[path_resource, path_function, 
                             path_temp, path_export])        
    return ''




def load_data(words=[]):
    '''
    讀取資料及重新整理
    '''
    
    words = cbyz.conv_to_list(words)
    
    # Pytrend .....
    global trend_words, trend_data    
    trend_words = ['疫苗', '確診', '陳時中', '家樂福', '大潤發', 'Uber Eats', 'Foodpanda',
             '全聯', '愛買', '全家', '好市多', '封城', '台股', '比特幣', '美股']
    
    if 'trend_data' not in globals():
        trend_data = cbyz.pytrends_multi(begin_date=20210401, end_date=20210430, 
                                         words=words, hl='zh-TW', geo='TW')
        


def master():
    '''
    主工作區
    '''
    
    load_data()
    
    return ''




def check():
    '''
    資料驗證
    '''    
    return ''




master()


# %% Application ----

app = dash.Dash()


if local == False:
    cache = Cache(app.server, config={
        # try 'filesystem' if you don't want to setup redis
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': os.environ.get('REDIS_URL', '')
    })
    app.config.suppress_callback_exceptions = True
    

              
data1 = [{'x': trend_data[trend_data['VARIABLE']==i]['DATE'],
          'y': trend_data[trend_data['VARIABLE']==i]['VALUE'],
          'type': 'line',
          'name': i,
          } for i in trend_words]
          
          


historical_plot =  dcc.Graph(
                        id='example-graph',
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



app.layout = html.Div([
        

    html.Div([
        html.P('半年資料'),
        daq.ToggleSwitch(
            id='btn_max',
            value=False,
            style={'padding':'0 10px'}
        ),
        html.P('三年資料'),
    ],style=btn_max_style),        
    
    
    
    html.Div(id='debug',
              style = debug_style),
    
    
    html.Div(id="line_chart"),
    historical_plot
    # html.P('Data Source'),
    ],  
    
    style=container_style
)


@app.callback(
    
    [Output('line_chart', 'children'),
      Output('debug', 'children')
      ],
    [Input("name_dropdown", "value"),
      Input('btn_max', 'value')
      ]
    
)


def update_output():

    global pytrends_data
  
        
    # data1 = [{'x': plot_data[(plot_data['STOCK_SYMBOL'] == \
    #                           selected_list['STOCK_SYMBOL'][i]) & \
    #                   (plot_data['TYPE'] == 'HISTORICAL')]['WORK_DATE'],
    #           'y': plot_data[(plot_data['STOCK_SYMBOL'] == \
    #                           selected_list['STOCK_SYMBOL'][i]) & \
    #                   (plot_data['TYPE'] == 'HISTORICAL')]['CLOSE'],
    #           'type': 'line',
    #           'name': selected_list['STOCK'][i],
    #           } for i in range(0, len(selected_list))]
        

    # historical_plot =  dcc.Graph(
    #                         id='example-graph',
    #                         figure={
    #                             'data': data1,
    #                             'layout': {
    #                                 'plot_bgcolor': colors['background'],
    #                                 'paper_bgcolor': colors['background'],
    #                                 'font': {
    #                                     'color': colors['text']
    #                                 },
    #             #                    'title': 'DASH'
    #                             }
    #                         },
    #                     )

    # # data5 = [{'x': df[df[1] == val][0],
    # #               'y': df[df[1] == val][6],
    # #               'type': 'line',
    # #               'name': val + " - 交易量",
    # #               } for val in dropdown_value]
        

    # # figure = [historical_plot, historical_plot]
    # figure = [historical_plot]


    # # Debug
    # debug_dropdown = '_'.join(dropdown_value)
    

    return 'OK'
    # return figure, 'ID_'+debug_dropdown+'_MAX_'+str(btn_max)+'_'



if __name__ == '__main__':
    app.run_server()
    # app.run_server(debug=True)






