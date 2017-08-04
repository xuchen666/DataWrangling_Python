#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 11:06:39 2017

@author: xuchenwang
"""


"""
This file downloads data with certain carrier and airport and extracts the flight data 
from that table as a list of dictionaries, each dictionary containing relevant data from 
the file and table row. 
"""

import requests
from bs4 import BeautifulSoup


def get_info(soup, params):
    add_info = []
    for param in params:
        add_info.append((param, soup.find(id=param)['value']))
    
    return tuple(add_info)
              
        

def get_classvalue(soup, class_name):        
    table_data = []        
    rows_tag = soup.find_all(class_ = class_name)[2].find_all('tr')
    
    for i in range(1,len(rows_tag)-1):
        tags = rows_tag[i].find_all('td')
        
        if tags[1].text == 'TOTAL':
            continue
        
        info = {'year':'',
                'month':'',
                'flights':{'domestic':'',
                           'international':''}
                }
                
        info['year'] = int(tags[0].text)
        info['month'] = int(tags[1].text)
        info['flights']['domestic'] = int(tags[2].text)

        table_data.append(info)
    
    return table_data



if __name__ == '__main__':
    url = 'https://www.transtats.bts.gov/Data_Elements.aspx?Data=2'
    
    # Send requests to get certain information  
    s = requests.Session()
    r = s.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    
    # Set up all parameters we are interested in and scrape it from website
    data = (
        ('__EVENTTARGET',''),
        ('__EVENTARGUMENT',''),
        ('CarrierList','VX'),
        ('AirportList','BOS'),
        ('Submit','Submit')
        )
    params = ['__VIEWSTATE', '__EVENTVALIDATION','__VIEWSTATEGENERATOR']
    new_data = data + get_info(soup, params)   
    
    # Post requests to validate data and download locally
    r = s.post(url, data=new_data)
    with open('/Users/xuchenwang/temp.html','w') as f:
        f.write(r.text)
        
    with open('/Users/xuchenwang/temp.html','r') as f:
        soup = BeautifulSoup(f, 'lxml')
        table_info = get_classvalue(soup, "dataTDRight")
    
    

    
    
    
    
    
    
    