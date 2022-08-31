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


host = 0
host = 1
# host = 5


# Path .....
if host == 0:
    path = r'/Users/aron/Documents/GitHub/Google_Trends_Enhanced'
elif host == 1:
    path = '/home/aronhack/google_trends_enhanced'
    # path = '/home/aronhack/stock_analysis_us/dashboard'
elif host == 5:
    path= '/Users/aronwu/Documents/AH/GitHub/Google_Trends_Enhanced'



# Codebase ......
path_codebase = [r'/Users/Aron/Documents/GitHub/Arsenal/',
                 r'/Users/Aron/Documents/GitHub/Codebase',
                 r'/Users/aronwu/Documents/AH/GitHub/Arsenal',
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
                        '/assets/style.css',
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



# Bug
# - Cannot embed style.css, so insert css in the head

# https://stackoverflow.com/questions/61305223/how-to-add-google-analytics-gtag-to-my-python-dash-app
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-ZCY778133M"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
        
          gtag('config', 'G-ZCY778133M');
        </script>
    
        <!-- Google AdSense -->
        <script data-ad-client="ca-pub-3866010510626398" async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
        
        <!-- AdSense AMP Auto Ad -->
        <script async custom-element="amp-auto-ads"
                src="https://cdn.ampproject.org/v0/amp-auto-ads-0.1.js">
        </script>
        {%metas%}
        <title>Google Trends Enhanced 搜尋趨勢分析威力加強版</title>
        {%favicon%}
        {%css%}
        
        
        <style>
            #dropdown .Select-menu-outer{
              display: none !important;
              # font-size: 30px !important;
              # background-color: #000000;
            }
        </style>
        
    </head>
    <body>

        <div align="center" class="mt-4">
            <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3866010510626398"
                 crossorigin="anonymous"></script>
            <!-- Trends Display Ad -->
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-3866010510626398"
                 data-ad-slot="5582539449"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>
                 (adsbygoogle = window.adsbygoogle || []).push({});
            </script>    
        </div>

        {%app_entry%}

        <div align="center" class="mb-4">
            <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3866010510626398"
                 crossorigin="anonymous"></script>
            <!-- Trends Display Ad -->
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-3866010510626398"
                 data-ad-slot="5582539449"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>
                 (adsbygoogle = window.adsbygoogle || []).push({});
            </script>  
        </div>


        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''





# %% Style ------
colors = {
    'background': '#f5f5f5',
    'text': '#303030'
}


# CSS ......


word_input_style = {
    'height': '35px',
    'display': 'block',
    'margin': '16px 0'
    }

btn_style = {
    'margin-right': '10px',
    'margin-bottom': '16px'
    }

footer_style = {
    'font-size':'14px'
    }


ah_logo = r'https://aronhack.com/wp-content/themes/aronhack/assets/header/logo_v2_wide.png'

app.layout = html.Div([
    
    html.Div( 
        html.Div([
            html.Div(html.A(html.Img(src=ah_logo,
                                     style={'width':'110px'},
                                     className='my-4 ',),
                            href='https://trends.aronhack.com/',
                            ),
                     className='col-6'
                     ),
            
            html.Div(html.Nav([html.A('首頁', 
                                      className="nav-item nav-link text-dark",
                                      href='https://aronhack.com/zh/home-zh/'),
                               html.A('說明', 
                                      className="nav-item nav-link text-dark", 
                                      href='https://aronhack.com/zh/google-trends-enhanced-guide-zh/')
                               ],
                              className = 'nav nav-pills ', 
                ),
                className='col-6',
                style={'justify-content':'right',
                       'align-items':'center',
                       'display': 'flex'},
                ),
            ],
            className='row'
            ),
        className=''
    ),    
    
    
    
    html.H1('Google Trends Enhanced 搜尋趨勢分析威力加強版',
        style={'font-size':'1.8em',
               'margin':'30px 0'}),

    dcc.Store(id='df_memory', data=df_memory_dict),

    dcc.DatePickerRange(id='calendar', 
                        start_date=date(2022, 1, 1),
                        end_date=date(2022, 1, 10),
                        min_date_allowed=date(2001, 1, 1),
                        max_date_allowed=date(2025, 12, 31),
                        display_format='Y-M-D', 
                        # with_portal=True, 
                        className='col-12 col-sm-12 col-md-6 d-block'),
    
    # dcc.Textarea(id="word_input",
    #              placeholder="換行以區分關鍵字",
    #              style=word_input_style),
    
    
    dcc.Dropdown(
        id='dropdown',
        placeholder="輸入關鍵字",
        options=[],
        style=word_input_style,
        className='col-12 col-sm-12 col-md-6',
        multi=True
    ),    
    
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
                               className='text-decoration-none'),
                        ' - '
                        ]),
              html.Span(['© 2022 ',
                        html.A('ARON HACK 亞倫害的.', 
                               href='https://aronhack.studio/aronhack_dash_footer',
                               target='_blank',
                               className='text-decoration-none'),
                        ' All Rights Reserved'],
                        className=''),
             ],
             className='text-center',
             style=footer_style)
        
    ],  
    className='p-4',
)


# @app.after_request
# def apply_caching(response):
#     response.headers["X-Frame-Options"] = "SAMEORIGIN"
#     return response


# %% Callback ------


@app.callback(
    Output('dropdown', 'options'),
    Input('dropdown', 'search_value'), 
    State('dropdown', 'options'),
)

def callback(new_value, cur_options):
    
    if not new_value or new_value in cur_options:
        return cur_options

    cur_options.append({'label': new_value, 'value': new_value})
    return cur_options



@app.callback(
    Output('graph', 'figure'),
    Output('df_memory', 'data'),
    Input('submit_btn', 'n_clicks'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown', 'value')
)


def update_output(_submit_clicks, begin_date, end_date, words):
    
    
    if begin_date == None or end_date == None or len(words) == 0:    
        raise PreventUpdate


    # Query        
    begin_date_lite = cbyz.date_simplify(begin_date)
    end_date_lite = cbyz.date_simplify(end_date)            
    
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
    # - Add all rights reserved
    # - Give up to add X-Frame-Options, but add affiliate link to the footer 
    #   of dashboards.
    # v3.0200
    # - Redirection versoin
    # - Add Adsense code
    # v3.0300
    # - Replace input with dropdown
    # v3.0400
    # - Add GA4

    # v3.0500
    # - Add multilingual

    
    # style.css not working
    
    
    # Worklist
    # - Dash will automatically embedb resource under assets folder, but
    #   I load stlye.css manually not
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






