#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 23:41:53 2023

@author: dev
"""

import pandas as pd
pd.set_option('display.max_columns', None)
from random import choice
import pickle
import os

def prep_data(df):
    '''
    

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    '''
    df = df.replace(regex={'/': ' ; ', ',': ' ; '})
    
    term_mapping = {}
    for col in df.columns[1:]:
        unique_terms = set()
        for entry in df[col]:
            terms = entry.split(';')
            unique_terms.update(term.strip() for term in terms)
        
        term_mapping[col] = {term: i for i, term in enumerate(unique_terms)}
        for term, value in term_mapping[col].items():
            # print(f'Replaced {term} with {value}')
            df[col] = df[col].str.replace(term, str(value), regex=True)
    return df


def to_list(vect):
    # Send vectors w/o Topic
    for i, element in enumerate(vect):
        try:
            vect[i] = int(element)
        except:
            vect[i] = [int(j) for j in element.split(';')]
    return vect


def l1_distance(v1, v2):
    '''
    

    Parameters
    ----------
    v1 : TYPE
        DESCRIPTION.
    v2 : TYPE
        DESCRIPTION.

    Returns
    -------
    diff : TYPE
        DESCRIPTION.

    '''
    # Send vectors w/o Topic
    diff = 0
    w = [0.4, 0.1, 0.2, 0.3, 1.0]
    v1 = to_list(v1)
    v2 = to_list(v2)
    for i, (e1, e2) in enumerate(zip(v1, v2)):
        if isinstance(e1, int) and isinstance(e2, int):
            diff += w[i]*abs(e1-e2)
        elif isinstance(e1, int) and isinstance(e2, list):
            distances = [abs(e1-j) for j in e2]
            diff += w[i]*min(distances)
        elif isinstance(e1, list) and isinstance(e2, int):
            distances = [abs(e2-j) for j in e1]
            diff += w[i]*min(distances)
        else:
            # Both are lists
            distances = [abs(j-k) for j in e1 for k in e2]
            diff += w[i]*min(distances)
    return diff


def recommend_best(selected_cats, avbl_cats, df):
    '''
    

    Parameters
    ----------
    selected_cats : TYPE
        DESCRIPTION.
    avbl_cats : TYPE
        DESCRIPTION.
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    keys : TYPE
        DESCRIPTION.

    '''
    distances = {}

    for i in selected_cats:
        for j in avbl_cats:
            if j in selected_cats:
                continue
            v1 = df.loc[df['Topic'] == i].iloc[:, 1:].values.tolist()[0]
            v2 = df.loc[df['Topic'] == j].iloc[:, 1:].values.tolist()[0]
            dist = l1_distance(v1, v2)
            cmp = i + ' vs ' + j
            distances[cmp] = dist

    sorted_keys = [i.split('vs')[1].strip() for i in sorted(distances, key=lambda x: distances[x])]
    
    keys = read_AA(selected_cats)
    for i in sorted_keys:
        if i not in keys:
            keys.append(i)
    
    return keys


def select_cats(avbl_cats, flag=0, cats=None):
    '''
    

    Parameters
    ----------
    avbl_cats : TYPE
        DESCRIPTION.
    flag : TYPE, optional
        DESCRIPTION. The default is 0.

    Returns
    -------
    selected_cats : TYPE
        DESCRIPTION.

    '''
    selected_cats = []
    if flag:
        # User chooses their own
        if cats == None:
            cats = input('Enter the numbers corresponding to the categories you want to follow. Separated by spaces\n')
        cats = cats.split()
        selected_cats = [avbl_cats[int(i)-1] for i in cats]        
    else:
        while len(selected_cats) < 5:
            cat = choice(avbl_cats)
            if cat not in selected_cats:
                selected_cats.append(cat)
    return selected_cats


def print_cats(avbl_cats, verbose):
    '''
    

    Parameters
    ----------
    avbl_cats : TYPE
        DESCRIPTION.
    verbose : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    print()
    if verbose == 0:
        print('Available categories')
        print('--------------------')
    elif verbose == 1:
        print('Selected categories')
        print('-------------------')
    elif verbose == 2:
        print('Recommended categories')
        print('----------------------')
    else:
        print('--------------------')
    for i, cat in enumerate(avbl_cats):
        print(str(i+1)+'. '+cat)
    print()
        
    return


def DCAA(selected_cats):
    '''
    Data collection for Association Analysis. Writes information about occurrence of pairs of categories into a file.

    Parameters
    ----------
    selected_cats : list
        The list of categories chosen by a user/instance.

    Returns
    -------
    None.

    '''
    if os.path.exists('AA.pkl'):
        with open('AA.pkl', 'rb') as f:
            dct = pickle.load(f)
    else:
        dct = {}

    for i in selected_cats:
        for j in selected_cats:
            if i != j:
                pair_key = tuple(sorted([i, j]))
                dct[pair_key] = dct.get(pair_key, 0) + 1

    dct = dict(sorted(dct.items(), key=lambda item: item[1], reverse=True))
    with open('AA.pkl', 'wb') as f:
        pickle.dump(dct, f)

    return


def read_AA(selected_cats):
    '''
    Reads from the pickle file made by DCAA and returns the most commonly associated categories with each of the selected categories.

    Parameters
    ----------
    selected_cats : TYPE
        DESCRIPTION.

    Returns
    -------
    l : TYPE
        Most common categories with the selected categories.

    '''
    with open('AA.pkl', 'rb') as f:
        dct = pickle.load(f)
        
    l = []
    for cat in selected_cats:
        for (key, value) in dct.items():
            if cat in key:
                if key[0] not in selected_cats and key[0] not in l:
                        l.append(key[0])
                if key[1] not in selected_cats and key[1] not in l:
                        l.append(key[1])
            
    return l
