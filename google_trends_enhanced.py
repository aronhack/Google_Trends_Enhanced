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
from dash.dependencies import Input, Output


from dash_extensions import Download
from dash_extensions.snippets import send_data_frame


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


# Iniitialize ......
app = dash.Dash()
df_memory_dict = pd.DataFrame({'DATE':[], 'VALUE':[]}).to_dict()



# Style ......
colors = {
    'background': '#f5f5f5',
    'text': '#303030'
}



# Style ......
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


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
        
        html.Button('查詢', id='submit_btn', 
                    n_clicks=0, value=0, style=btn_style),
        
        html.Button('下載', id='download_btn', 
                    n_clicks=0, value=0, style=btn_style),
        
        Download(id="download"),
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
     Input('submit_btn', 'value'),
     Input('df_memory', 'data'),
      ]    
)



def update_output(begin_date, end_date, words, _submit_clicks, _submit_value, 
                  _df_memory):
    
    # 1. Add Loading icon

    trend_data_dict = _df_memory
    

    # begin_date_lite = 20210301
    # end_date_lite = 20210310
    # words = ['台股', '比特幣', '美股']
    
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
        
            
            trend_data_dict = \
                [{'x': trend_data[trend_data['VARIABLE']==i]['DATE'],
                  'y': trend_data[trend_data['VARIABLE']==i]['VALUE'],
                  'type': 'line',
                  'name': i,
                  } for i in trend_words]            
        
        
            submit_clicks = _submit_clicks
            submit_value = _submit_clicks
            
            switch = True
            print(words)
        


    if 'submit_value' not in locals():
        submit_value = _submit_value



    # 待優化 .......
    # 參考share data between callback中的Output('memory-graph', 'figure'),
    # https://dash.plotly.com/dash-core-components/store
    
    
    plot =  dcc.Graph(id='trend_plot',
                      figure={
                          'data': trend_data_dict,
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

    return figure, '', submit_value, trend_data_dict




@app.callback(
    [Output('download', 'data'),
     Output('download_btn', 'value')
    ],
    [Input('download_btn', 'n_clicks'),
     Input('download_btn', 'value'), 
     Input('df_memory', 'data'),
     ]    
)


def donwload_file(_download_clicks, _download_value, _df_memory):
    # 1. 20210607 - Download csv, not published yet
    # https://dash.plotly.com/dash-core-components/download    
    
    if _download_clicks > _download_value:
        
        _download_value = _download_clicks
        time_serial = cbyz.get_time_serial(with_time=True)
        
        # Convert nested dict to dataframe ......
        results = pd.DataFrame()
        
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
    
        return send_frame, _download_value




if __name__ == '__main__':
    app.run_server()
    # app.run_server(debug=True)






