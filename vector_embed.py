#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 16:35:55 2024

@author: Aditya K. Rao
"""
import requests as rq
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import cohere

def intialize_api():
    with open('keys.json', 'r') as f:
        API_KEYS = json.load(f)
        
    cohere_key = API_KEYS['cohere']
    co = cohere.ClientV2(cohere_key)
    
    return co

def load_data(f, engine='np'):
    if engine == 'np':
        return np.loadtxt(f)
        
    elif engine == 'pd':
        return pd.load_csv(f)
      
    elif engine == 'pure':
        with open(f, 'r') as file:
            lst = file.readlines()
        return lst

def get_embed(co, search_query):
    if type(search_query) != list:
        search_query = [search_query]
    
    response = co.embed(
        texts=search_query, 
        model="embed-english-v3.0", 
        input_type="classification", 
        embedding_types=["float"]
    )
    
    return response


if __name__ == "__main__":
    co = intialize_api()
    fake_query = load_data('user_data/71845_real_GPT_v4_1.0.txt', 'pure')
    real_query = load_data('user_data/71845_real.txt', 'pure')
    
    embeds = get_embed(co, [real_query[0], fake_query[0]])
    
    print(embeds)
    #print(fake_query)
    #print(real_query)
    
