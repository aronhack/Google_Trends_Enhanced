



# -*- coding: utf-8 -*-
import pandas as pd
import sys
import time
from datetime import date

import dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from dash import html, dcc, callback, Input, Output, State

import codebase_yz as cbyz
lang = 0



# %% Dictdionnay

dictionary = {}
dictionary['aronhack'] = ['ARON HACK',
                          'ARON HACK 亞倫害的']
dictionary['title'] = ['Google Trends Enhanced',
                        'Google Trends Enhanced 搜尋趨勢分析威力加強版']

dictionary['description'] = ['Whether you apply Google Trends through the website or writing a program to call the API, as long as you use the service of Google Trends, you can only search for up to five keywords at a time. This is a restriction set by Google and cannot be changed. Then why can the Google Trends Enhanced search multiple keywords at once? The task Google Trends Enhanced does is to group all keywords, obtain each search interest, then merge the data, and export it into a Excel file.',
                             '不論你是使用網頁版的Google Trends，或是寫程式呼叫API，只要你使用Google Trends的服務，一次最多只能搜尋五組關鍵字。這是Google設下的限制，沒辦法更動。那為什麼威力加強版可以一次搜尋多組關鍵字？實際上，威力加強版執行的任務是將所有關鍵字分組，分別取得每一次的搜尋熱度後再合併資料，並且匯出成Excel檔。']


dictionary['keywords'] = ['Input A Keyword, Then Press Enter.',
                          '輸入關鍵字後按Enter']
dictionary['search'] = ['Search', '搜尋']
dictionary['download'] = ['Download', '下載']
dictionary['home'] = ['Home', '首頁']
dictionary['home_link'] = ['https://aronhack.com/', 
                           'https://aronhack.com/zh/home-zh/']

dictionary['documentation'] = ['Documentation', '說明']
dictionary['doc_link'] = ['https://aronhack.com/zh/google-trends-enhanced-guide/', 
                          'https://aronhack.com/zh/google-trends-enhanced-guide-zh/']

dictionary['language'] = ['Language', '語言']


df_memory_dict = pd.DataFrame({'DATE':[], 'VALUE':[]}).to_dict()


# ..............


if lang == 0:
    dash.register_page(__name__, title=dictionary['title'][lang],
                       description=dictionary['description'][lang], path='/')
elif lang == 1:
    dash.register_page(__name__, title=dictionary['title'][lang],
                       description=dictionary['description'][lang], path='/zh')



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
        


# %% Style ------
colors = {
    'background': '#f5f5f5',
    'text': '#303030'
}


# CSS ......
word_input_style = {
    'height': '35px',
    'display': 'block',
    'margin': '16px 0',
    'font-size': '16px'
    }

btn_style = {
    'margin-right': '10px',
    'margin-bottom': '16px'
    }

footer_style = {
    'font-size':'14px'
    }


ah_logo = r'https://aronhack.com/wp-content/themes/aronhack/assets/header/logo_v2_wide.png'


layout = html.Div([
    
    html.Div(id="debug"),
    dcc.Location(id='url'),
    
    html.Div( 
        html.Div([
            html.Div(html.A(html.Img(src=ah_logo,
                                      style={'width':'110px'},
                                      className='my-4 ',),
                            href=dictionary['home'][lang],
                            ),
                      className='col-6'
                      ),
            
            
            html.Div(html.Nav([html.A(dictionary['home'][lang], 
                                      className="nav-item nav-link text-dark",
                                      href=dictionary['home_link'][lang]),
                                html.A(dictionary['documentation'][lang], 
                                      className="nav-item nav-link text-dark", 
                                      href=dictionary['doc_link'][lang])
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
    
    
    html.H1(dictionary['title'][lang],
        style={'font-size':'1.8em',
                'margin':'30px 0'}),

    dcc.Store(id='df_memory', data=df_memory_dict),

    dcc.DatePickerRange(id='calendar', 
                        start_date=date(2022, 1, 1),
                        end_date=date(2022, 1, 10),
                        min_date_allowed=date(2001, 1, 1),
                        max_date_allowed=date(2025, 12, 31),
                        display_format='Y-M-D', 
                        className='col-12 col-sm-12 col-md-6 d-block'),
    
    dcc.Dropdown(
        id='dropdown',
        placeholder=dictionary['keywords'][lang],
        options=[],
        style=word_input_style,
        className='col-12 col-sm-12 col-md-6',
        multi=True
    ),    
    
    html.Button(dictionary['search'][lang],
                id='submit_btn', 
                n_clicks=0, value=0,
                style=btn_style),
    
    html.Button(dictionary['download'][lang],
                id='download_btn', 
                n_clicks=0, value=0,
                style=btn_style),
    
    dcc.Download(id="download"),
    
    dcc.Loading(
        id="loading-1",
        type="default",
        children=dcc.Graph(id="graph")
    ),
    
    html.Div(
        [html.Div(dcc.Dropdown(
                    id='lang_dropdown',
                    placeholder=dictionary['language'][lang],
                    options=[{'label': 'English', 'value': ''},
                             {'label': '正體中文', 'value': 'zh'}],
                    style={'width':'150px'}
                    # style=word_input_style,
                    # className='col-12 col-sm-12 col-md-6',
                    ),  
                    className='col-3'),            
        html.Div(
                [html.Span(['Powered by ',
                        html.A('PythonAnywhere', 
                               href='https://aronhack.studio/pythonanywhere_dash',
                               target='_blank',
                               className='text-decoration-none'),
                        ' - '
                        ]),
             html.Span(['© 2022 ',
                        html.A(dictionary['aronhack'][lang] + '.', 
                               href='https://aronhack.studio/aronhack_dash_footer',
                               target='_blank',
                               className='text-decoration-none'),
                    ' All Rights Reserved'],
                       className=''),
              ],
               # className='text-center',
              className='col-6 d-flex align-items-center justify-content-center',
              style=footer_style),
        
        html.Div(className='col-3'),          
            ],
        className='row',
        ),
    
    ],
    id='container',
    className='p-4',
)



# %% Callback ------

@dash.callback(
    Output('dropdown', 'options'),
    Input('dropdown', 'search_value'), 
    State('dropdown', 'options'),
)

def callback_fun(new_value, cur_options):
    
    print('Is it possible to detect press Enter in the input')
    
    if not new_value or new_value in cur_options:
        return cur_options
    
    print(new_value)
    if new_value == '1':
        global lang
        lang = 1
        print('lang = 1')
    

    cur_options.append({'label': new_value, 'value': new_value})
    return cur_options


@dash.callback(
    Output('graph', 'figure'),
    Output('df_memory', 'data'),
    Input('submit_btn', 'n_clicks'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown', 'value')
)


def update_output(_submit_clicks, begin_date, end_date, words):
    
    
    if begin_date == None or end_date == None or words == None:
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


@dash.callback(
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


@dash.callback(
    Output('url', 'pathname'),
    Input('lang_dropdown', 'value'), 
    State('url', 'pathname'),
)

def lang(lang_option, url_value):
    if lang_option != None:
        return '/' + lang_option
    else:
        return url_value

