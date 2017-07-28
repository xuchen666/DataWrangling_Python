#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 21:23:11 2017

@author: xuchenwang
"""

'''
This file extracts data from xml on authors of an article
and add it to a list, one item for an author.
The tags for first name, surname and email should map directly
to the dictionary keys
'''

import xml.etree.ElementTree as ET

article_file = '/Users/xuchenwang/python/exampleresearcharticle.xml'


def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def get_title(root):
    title = root.find('./fm/bibl/title')
    for p in title:
        print('\nTitle:\n',p.text)



def get_authors(root):
    authors = []
    for author in root.findall('./fm/bibl/aug/au'):
        data = {
                "fnm": None,
                "snm": None,
                "email": None,
                "insr": []
        }

        data['fnm'] = author.find('./fnm').text
        data['snm'] = author.find('./snm').text
        data['email'] = author.find('./email').text
        for insr in author.findall('./insr'):
            data['insr'].append(insr.attrib['iid'])

        authors.append(data)

    return authors


def test():
    solution = [{'insr': ['I1'], 'fnm': 'Omer', 'snm': 'Mei-Dan', 'email': 'omer@extremegate.com'},
                {'insr': ['I2'], 'fnm': 'Mike', 'snm': 'Carmont', 'email': 'mcarmont@hotmail.com'},
                {'insr': ['I3', 'I4'], 'fnm': 'Lior', 'snm': 'Laver', 'email': 'laver17@gmail.com'},
                {'insr': ['I3'], 'fnm': 'Meir', 'snm': 'Nyska', 'email': 'nyska@internet-zahav.net'},
                {'insr': ['I8'], 'fnm': 'Hagay', 'snm': 'Kammar', 'email': 'kammarh@gmail.com'},
                {'insr': ['I3', 'I5'], 'fnm': 'Gideon', 'snm': 'Mann', 'email': 'gideon.mann.md@gmail.com'},
                {'insr': ['I6'], 'fnm': 'Barnaby', 'snm': 'Clarck', 'email': 'barns.nz@gmail.com'},
                {'insr': ['I7'], 'fnm': 'Eugene', 'snm': 'Kots', 'email': 'eukots@gmail.com'}]

    root = get_root(article_file)
    data = get_authors(root)

    assert data[0] == solution[0]
    assert data[1]["insr"] == solution[1]["insr"]


if __name__ == 'main':
    test()