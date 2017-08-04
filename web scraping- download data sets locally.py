#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 10:36:32 2017

@author: xuchenwang
"""

'''
This file downloads data from different carrier-airport combination.
Firstly, it extracts carrier list and airport list of all carriers and airports.
Then it make requests to scraping these data set and downloads it locally and save
them as "{}-{}.html".format(carrier, airport), for example "FL-ATL.html".
'''


import requests
from bs4 import BeautifulSoup


# Get CarrierList and AirportList
def options(soup, id_name):
    '''
    This function finds list of values in the option tag in a tag with the targeted id. 
    And returns a list of values.
    '''
    option_values = []
    target_root = soup.find(id=id_name)
    for option in target_root.find_all('option'):
        option_values.append(option['value'])
    return option_values

    
# Download the data set locally  
def find_value(soup, id_name):
    return soup.find(id=id_name)['value']

def download_file(soup, data, carrier, airport):
    add_data = (('CarrierList', carrier),
                 ('AirportList', airport))
    new_data = data+add_data
    r = s.post(url, data=new_data)
    print(r.status_code)
    with open("/Users/xuchenwang/python/{}-{}.html".format(carrier, airport),'w') as g:
        g.write(r.text)

        

if __name__ == '__main__':
    url = 'https://www.transtats.bts.gov/Data_Elements.aspx?Data=2'
    
    # Get information of certain request
    s = requests.Session()
    r = s.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    
    carrier_list = options(soup, 'CarrierList')
    airport_list = options(soup, 'AirportList')
    
    viewstate = find_value(soup, "__VIEWSTATE")
    viewstategenerator = find_value(soup, "__VIEWSTATEGENERATOR")
    eventvalidation = find_value(soup, "__EVENTVALIDATION")
    
    data = (
                   ("__EVENTTARGET", ""),
                   ("__EVENTARGUMENT", ""),
                   ("__VIEWSTATE", viewstate),
                   ("__VIEWSTATEGENERATOR",viewstategenerator),
                   ("__EVENTVALIDATION", eventvalidation),
                   ("Submit", "Submit")
                  )
    
    # Post the request to assess to certain data and download data locally
    
    for carrier in carrier_list:
        for airport in airport_list:
            download_file(soup, data, carrier, airport)
    
    
    
    












