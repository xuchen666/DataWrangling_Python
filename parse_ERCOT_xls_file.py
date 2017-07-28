#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 17:48:53 2017

@author: xuchenwang
"""

"""
In this file, we do:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

"""

import xlrd
import os
from zipfile import ZipFile
import numpy as np


DATADIR = '/Users/xuchenwang/python/'
DATAFILE = '2013_ERCOT_Hourly_Load_Data.xls'

datafile = os.path.join(DATADIR, DATAFILE)


def open_zip(datafile):
    datafile = datafile.replace('xls','zip')
    with ZipFile(datafile, 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):    
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    
    data = {
                'maxtime': (0, 0, 0, 0, 0, 0),
                'maxvalue': 0,
                'mintime': (0, 0, 0, 0, 0, 0),
                'minvalue': 0,
                'avgcoast': 0
        }
    
    # slice the second column and return its statistics
    coast = sheet.col_values(1,start_rowx=1,end_rowx=None)
    data['maxvalue'] = max(coast)
    data['minvalue'] = min(coast)
    data['avgcoast'] = np.mean(coast)
    
    # find the position of maxvalue and minvalue
    maxpos = coast.index(data['maxvalue'])+1
    minpos = coast.index(data['minvalue'])+1
    
    # find the corresponding value in the first column and convert it to tuple.
    data['mintime'] = xlrd.xldate_as_tuple(sheet.cell_value(minpos,0),0)
    data['maxtime'] = xlrd.xldate_as_tuple(sheet.cell_value(maxpos,0),0)
    
    return data


def test():
    open_zip(datafile)
    data = parse_file(datafile)

    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)

if __name__ == '__main__':
    test()








