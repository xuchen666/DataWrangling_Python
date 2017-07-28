#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 10:21:45 2017

@author: xuchenwang
"""


"""
This procedure processes the supplied file and use the csv module to extract data from it.
The data '745090' comes from NREL (National Renewable Energy Laboratory) website. Each file
contains information from one meteorological station, in particular - about amount of
solar and wind energy for each hour of day.

Note that the first line of the datafile is neither data entry, nor header. It is a line
describing the data source. And it extracst the name of the station from it.

The second line is names of each colunm. It simply skips it.

The data is returned as a list of lists. It uses the csv modules "reader" method to get data 
in such format.
"""

import csv
import os

DATADIR = "/Users/xuchenwang/python/"
DATAFILE = "745090.csv"


def parse_file(datafile):
    with open(datafile,newline='') as f:
        reader = csv.reader(f)
        # extract the station name from the first line
        name = next(reader)[1]
        # skip the second line
        next(reader)
        data = list(reader)

    return (name, data)


def test():
    datafile = os.path.join(DATADIR, DATAFILE)
    name, data = parse_file(datafile)

    assert name == "MOUNTAIN VIEW MOFFETT FLD NAS"
    assert data[0][1] == "01:00"
    assert data[2][0] == "01/01/2005"
    assert data[2][5] == "2"


if __name__ == "__main__":
    test()