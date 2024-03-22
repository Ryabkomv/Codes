# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 11:03:09 2020

@author: m.ryabko
"""


import requests
import random

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

BadCat=[]

def getRandomCategory(t):
    

    PARAMS = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": t,
        "cmlimit": 500,
        "format": "json"
    }
    
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    return random.choice(DATA['query']['categorymembers'])['title']

def getCategory():
    t = "Category: Technology by type"
    while "Category:" in t:
        t = getRandomCategory(t)
    return t 



try:
    t=getCategory()
except:
    t=getCategory()
    
    
PARAMS = {
    "action": "query",
    "titles": t,
    "prop": "info",
    "inprop" : "url",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

#print(DATA['query']['pages'][list(DATA['query']['pages'].keys())[0]]['extract'])
print(DATA['query']['pages'][list(DATA['query']['pages'].keys())[0]]['fullurl'])