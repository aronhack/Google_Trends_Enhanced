

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
import time
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup



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


black_box = r'/Users/aron/Documents/GitHub/Black_Box'


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
path_resource = path + '/Resource'
path_function = path + '/Function'
path_temp = path + '/Temp'
path_export = path + '/Export'


cbyz.os_create_folder(path=[path_resource, path_function, 
                         path_temp, path_export])     

pd.set_option('display.max_columns', 30)
 



def master():
    
    # - 20220904, geo value not showed in the HTML. You can view the resource 
    #   folder
    
    url = 'https://trends.google.com/trends/?geo=TW'
    driver = webdriver.Firefox(executable_path=black_box + '/geckodriver')
    driver.get(url)
        
    # Define elements
    dropdown = driver.find_element(By.ID, value='select_2')
    geo_options = driver.find_elements(
            By.CSS_SELECTOR, 
            '#select_container_3 md-option > div'
        )
    
    
    from selenium.webdriver.common.action_chains import ActionChains
    actions = ActionChains(driver)    
    
    
    # Loop ------
    li = []

    for i in range(len(geo_options)):
    # for i in range(10):        
        
        # Display the option
        dropdown.click()
        
        cur_geo = geo_options[i]
        country = cur_geo.text

        # Scroll to the element
        actions.move_to_element(cur_geo).perform()    
        cur_geo.click()
        
        li = li + [[country, driver.current_url]]
        print('crawler -', i, '/', len(geo_options))
        time.sleep(random.uniform(2, 3))
        

    # MoveTargetOutOfBoundsException: (973, 744) is out of bounds of viewport width (1280) and height (726)                       
    # https://stackoverflow.com/questions/44777053/selenium-movetargetoutofboundsexception-with-firefox        
        
    
    result = pd.DataFrame(li, columns=['country', 'link'])
    result = result.drop_duplicates()
    result.to_csv(path_resource + '/geo.csv', index=False)



if __name__ == '__main__':
    
    master()

