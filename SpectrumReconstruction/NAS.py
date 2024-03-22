# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 15:59:47 2017

@author: ryabko
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

import pickle

j=3

plt.figure(1) 
    
with open('Raman Spectra/spectra.txt', 'rb') as f:
        spectra = pickle.load(f)
S=spectra[1:9,:]

vec = np.append(np.array(range(0,j)),np.array(range(j+1,8)))


c0 = np.diag(np.array([2,1,4,3,5,6,3,2]))

c = np.diag(np.array([1,2,7,24,1,4,2,3]))
d = np.dot(c,S)
d1 = np.random.rand(np.shape(d)[0],np.shape(d)[1])*30
d = d+d1
A = c0.dot(S).transpose()

aj = A[:,j]
Aj = A[:,vec]
Aj_inv = np.linalg.pinv(Aj)
aj_star = np.dot(np.eye(np.shape(Aj)[0]) - np.dot(Aj,Aj_inv),aj)

#for j in range(1,np.shape(spectra)[0]):
#    plt.plot(spectra[0,].transpose(),A[:,j])

A_inv = np.linalg.pinv(A)
Proj = np.eye(10)

cj = c0[j]*np.dot(d,aj_star)/(np.dot(aj_star.transpose(),aj_star))
#print(np.append(np.array(range(0,j)),np.array(range(j+1,9))))