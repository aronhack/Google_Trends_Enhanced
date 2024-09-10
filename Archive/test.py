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



local = False
# local = True


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



app = dash.Dash()

app.layout = \
    html.Div([
        html.Div('Text', id='debug'),
        html.Div(id="line_chart"),
    ],
)




if __name__ == '__main__':
    app.run_server()
