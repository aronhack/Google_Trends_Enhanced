

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
import os

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.exceptions import PreventUpdate
from dash import html, dcc, callback, Input, Output, State


import plotly.graph_objs as go


host = 0
# host = 1
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


# # 自動設定區 -------
# pd.set_option('display.max_columns', 30)
 

# # 新增工作資料夾
# path_resource = path + '/Resource'
# path_function = path + '/Function'
# path_temp = path + '/Temp'
# path_temp_user = path + '/Temp_User'
# path_export = path + '/Export'


# cbyz.os_create_folder(path=[path_resource, path_function, 
#                             path_temp, path_temp_user, path_export])





# Change root path
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
# os.chdir(os.path.dirname(path))
os.chdir(path)


# %% Application ----

# Running a Dash app within a Flask app
# https://stackoverflow.com/questions/45845872/running-a-dash-app-within-a-flask-app

import flask
server = flask.Flask(__name__)

external_stylesheets = [dbc.themes.BOOTSTRAP,
                        '/assets/style.css',
                        'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, server=server, 
                external_stylesheets=external_stylesheets,
                use_pages=True, 
                # pages_folder='Google_Trends_Enhanced'                
                )


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

        {%app_entry%}

        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


# 20221011 - Remove header ads
# <div align="center" class="mt-4">
#     <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3866010510626398"
#           crossorigin="anonymous"></script>
#     <!-- Trends Display Ad -->
#     <ins class="adsbygoogle"
#           style="display:block"
#           data-ad-client="ca-pub-3866010510626398"
#           data-ad-slot="5582539449"
#           data-ad-format="auto"
#           data-full-width-responsive="true"></ins>
#     <script>
#           (adsbygoogle = window.adsbygoogle || []).push({});
#     </script>    
# </div>


# <div align="center" class="mb-4">
#     <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3866010510626398"
#           crossorigin="anonymous"></script>
#     <!-- Trends Display Ad -->
#     <ins class="adsbygoogle"
#           style="display:block"
#           data-ad-client="ca-pub-3866010510626398"
#           data-ad-slot="5582539449"
#           data-ad-format="auto"
#           data-full-width-responsive="true"></ins>
#     <script>
#           (adsbygoogle = window.adsbygoogle || []).push({});
#     </script>  
# </div>



# %% Layout ------

app.layout = html.Div([

    html.Div(
        [html.Div() for page in dash.page_registry.values()]
    ),

	dash.page_container
])



# @app.after_request
# def apply_caching(response):
#     response.headers["X-Frame-Options"] = "SAMEORIGIN"
#     return response



# %% Execute ------


def version_note():
    '''
    主工作區
    '''
    
    # v1.0001
    
    
    # Bug
    # - Not Found
    #   The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.




    # Note
    # - 把zh的callback加進去後會stuck，可能是因為是用id，所以en的callback也對zh有用
    # - Modify for zh verion
    #   - Fix on en version
    #   - Comment callback
    #   - change the lang
        
    
    # Worklist
    # - bug
    #   if begin_date == None or end_date == None or len(words) == 0:
    #   TypeError: object of type 'NoneType' has no len()
    # - style.css not working, using inline css now
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


