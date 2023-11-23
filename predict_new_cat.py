#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 00:20:52 2023

@author: dev
"""

from helpers import prep_data, recommend_best, print_cats, select_cats, DCAA
from sys import exit
import pandas as pd

filename = './Attributes.csv'
df = pd.read_csv(filename)
df = prep_data(df)
avbl_cats = [cat.strip() for cat in df['Topic'].unique()]

def user_view():
    global avbl_cats
    global df
    
    print_cats(avbl_cats, verbose=0)

    # If flag = 1, user can choose own categories
    selected_cats = select_cats(avbl_cats, flag=1)
    DCAA(selected_cats)   # Data Collection for Association analysis
    print_cats(selected_cats, verbose=1)
    sorted_keys = recommend_best(selected_cats, avbl_cats, df)
    print_cats(sorted_keys[:5], verbose=2)
    
    
def admin_view():
    global df
    global filename
    
    src_df = pd.read_csv(filename)
    options = [
            'Add new topic',
            'Remove topic',
            'Update topic info',
            'Add new attribute',
            'View entire table'
        ]
    print('Choose an option [1-4]')
    print_cats(options, verbose=4)
    opt = int(input('Enter number corresponding to option: '))
    if opt == 1:
        topic = input('Enter Topic name: ')
        print('Now enter the attributes in the following format, if there are multiple values for same attribute, use slashes (/) to separate them')
        print('----------------------------------------FORMAT--------------------------------------')
        print('Domain ; Education level ; Expertise required ; Industry relevance ; Possible career')
        attr = input().split(';')
        line = [topic]
        for i in attr:
            line.append(i)
        line = pd.DataFrame([line], columns=src_df.columns)
        src_df = pd.concat([src_df, line], ignore_index=True)
        src_df.to_csv(filename, index=False)
        
    elif opt == 2:
        pass
    elif opt == 3:
        pass
    elif opt == 4:
        pass
    elif opt == 5:
        print(src_df)
    else:
        print('Bad input!')
        exit()

if __name__ == "__main__":
    user_view()




