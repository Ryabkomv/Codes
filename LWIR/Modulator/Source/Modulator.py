# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 14:05:04 2021

@author: m.ryabko
"""

import imp
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from  FDTD import FDTD
from  Charge import Charge

diameter=190
period = 290
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

lumapi = imp.load_source("lumapi","C:\\Program Files\\Lumerical\\v211\\api\\python\\lumapi.py")

#Charge(lumapi,period, diameter)

fig, ax = plt.subplots()  # Create a figure and an axes.



  # Add a title to the axes.
 # Add a legend.
for b in range(6, 12):
    f, T = FDTD(lumapi, period, diameter,b)
    ax.plot(T['lambda']*1e9, T['T'], label='Voltage: '+ str((b-1)*0.12))  # Plot some data on the axes.

    
ax.set_xlabel('wavelength, nm')  # Add an x-label to the axes.
ax.set_ylabel('Transmittance')  # Add a y-label to the axes.    
ax.set_title("Dependence on voltage")
ax.legend() 

fig.savefig('..\\Results\\voltage_variation.png')