#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 12:07:06 2017

@author: xuchenwang
"""


'''
In this file, find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.
'''

import xlrd
import os
import csv
from zipfile import ZipFile

DATADIR = '/Users/xuchenwang/python/'
DATAFILE = "2013_ERCOT_Hourly_Load_Data.xls"

datafile = os.path.join(DATADIR,DATAFILE)
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    '''
    This function is used to open .zip file.
    '''
    datafile = datafile.replace('xls','zip')
    with ZipFile(datafile, 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    '''
    This function uses xlrd module to parse .xls file and returns a list of dictionary.
    Each dictionary is the value of 'Station','Year','Month','Day','Hour','Max Load' for each station.
    '''
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []

    for i in range(1,sheet.ncols-1):
        dic = {}    
        dic['Station'] = sheet.cell_value(0,i)
        
        col = sheet.col_values(i,start_rowx=1,end_rowx=None)
        max_load = max(col)
        
        maxpos = col.index(max_load)+1
        max_time = xlrd.xldate_as_tuple(sheet.cell_value(maxpos,0),0)
        
        dic['Year'] = max_time[0]
        dic['Month'] = max_time[1]
        dic['Day'] = max_time[2]
        dic['Hour'] = max_time[3]
        dic['Max Load'] = max_load
        
        data.append(dic)
    
    return data


def save_file(data, filename): 
    '''
    This functon save the data (a list of dict) in a .csv file, uses '|' as a delimiter.
    '''
    with open(filename,'w') as of:
        fieldnames = ['Station','Year','Month','Day','Hour','Max Load']
        writer = csv.DictWriter(of, delimiter='|', fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    
def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)

        
if __name__ == "__main__":
    test()
