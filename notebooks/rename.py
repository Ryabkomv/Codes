# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 10:11:37 2018

@author: ryabko
"""
import pickle
import numpy as np
import os


#os.rename("C:/WinPython-64bit-3.5.2.3Qt5/Code/Medicals/2nd_round/304.txt", "C:/WinPython-64bit-3.5.2.3Qt5/Code/Medicals/2nd_round/04.txt")
#f = os.listdir("C:/WinPython-64bit-3.5.2.3Qt5/Code/Medicals/1st_round")
#for g in f:
#    print(g.replace('64CH', ''))
#    os.rename("C:/WinPython-64bit-3.5.2.3Qt5/Code/Medicals/1st_round/" + g, "C:/WinPython-64bit-3.5.2.3Qt5/Code/Medicals/1st_round/"+g.lower())
#    

with open('data1.pickle', 'rb') as f:
     data = pickle.load(f)