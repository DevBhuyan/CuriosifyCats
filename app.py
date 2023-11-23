#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 02:13:54 2023

@author: dev
"""

from flask import Flask, jsonify, request
from helpers import select_cats, recommend_best, prep_data, DCAA
import pandas as pd
from firebase_admin import credentials, storage, initialize_app, firestore


def init(bucket=True):
    """


    Returns
    -------
    bucket : TYPE
        DESCRIPTION.

    """
    cred = credentials.Certificate("curiosify-57e88-95095680c021.json")
    if bucket:
        try:
            initialize_app(cred, {"storageBucket": "curiosify-57e88.appspot.com"})
        except:
            pass

        bucket = storage.bucket()

        return bucket

    else:
        try:
            initialize_app(cred)

        except:
            pass

        db = firestore.client()

        return db
    

app = Flask(__name__)

@app.route('/admin')
def admin_view():
    pass


@app.route('/view_cats')
def view_cats():
    filename = './Attributes.csv'
    dct = []
    
    db = init(bucket=False)
    collection = 'videos'
    
    collection_ref = db.collection(collection)
    
    docs = collection_ref.list_documents()
    
    for i, doc in enumerate(docs):
        data = doc.get().to_dict()['category']
        if data not in dct:
            dct.append(data)
        
    new_dct = {}
    for i, cat in enumerate(dct):
        new_dct["Category "+str(i+1)] = cat
    
    return jsonify({"Available Categories": new_dct})


@app.route('/view_videocats')
def view_videocats():
    db = init(bucket=False)
    collection = "videos"

    collection_ref = db.collection(collection)

    docs = collection_ref.list_documents()

    videocats = {}
    for doc in docs:
        try:
            cat = doc.get().to_dict()['category']
            if cat not in videocats.keys():
                videocats[cat] = 1
            else:
                videocats[cat] += 1
        except:
            pass
    
    return jsonify({"Video categories available": videocats})
   

@app.route('/user_api', methods=['POST'])
def user_view():
    json_data = request.get_json()

    selected_cats = [value for key, value in json_data.items()]
    # print(selected_cats)
        
    filename = './Attributes.csv'
    df = pd.read_csv(filename)
    df = prep_data(df)
    avbl_cats = [cat.strip() for cat in df['Topic'].unique()]

    # If flag = 1, user can choose own categories
    DCAA(selected_cats)   # Data Collection for Association analysis
    # raise Exception(selected_cats, avbl_cats)
    sorted_keys = recommend_best(selected_cats, avbl_cats, df)
    
    new_cats = {}
    for i, cat in enumerate(selected_cats):
        new_cats["Category "+str(i+1)] = cat
    for i, cat in enumerate(sorted_keys[:5]):
        new_cats["Category "+str(i+1+len(selected_cats))] = cat
    
    return jsonify({"Recommended categories": new_cats})


@app.route('/test')
def return_randomly_chosen():
    filename = './Attributes.csv'
    df = pd.read_csv(filename)
    df = prep_data(df)
    avbl_cats = [cat.strip() for cat in df['Topic'].unique()]
    
    selected_cats = select_cats(avbl_cats)
    sorted_keys = recommend_best(selected_cats, avbl_cats, df)
    
    return jsonify({"Available Categories": avbl_cats, "Selected categories": selected_cats, "Recommended categories": sorted_keys[:5]})

if __name__ == "__main__":
    app.run(debug=True)
