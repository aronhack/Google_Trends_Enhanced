#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 23:00:50 2020

@author: Aron
"""


# % 讀取套件 -------
import pandas as pd
import numpy as np
import sys, time, os, gc

import pytrends

local = False
local = True


# Path .....
if local == True:
    path = '/Users/Aron/Documents/GitHub/Data/Stock_Analysis'
else:
    path = '/home/aronhack/stock_forecast/dashboard'
    # path = '/home/aronhack/stock_analysis_us/dashboard'


    
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




def load_data():
    '''
    讀取資料及重新整理
    '''
    
    
    
    
    return ''



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




from pytrends.request import TrendReq





pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

pytrends.interest_over_time()

pytrends = TrendReq(hl='zh-TW', tz=36)

kw_list = ["Blockchain", 'Crypto']

trend_results = pytrends \
    .get_historical_interest(kw_list, 
                            year_start=2019, month_start=1, 
                            day_start=1, year_end=2020, month_end=10, 
                            day_end=1, hour_end=0, 
                            cat=0, geo='', gprop='', sleep=0)
    
    


from pytrends import dailydata

df = dailydata.get_daily_data('cinema', 2019, 1, 2019, 10, geo = 'TW')




