# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:54:21 2017

@author: ryabko
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

import pickle

data = np.loadtxt('filters.txt')
plt.plot(data)
plt.show()
