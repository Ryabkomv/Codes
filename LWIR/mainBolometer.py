# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 12:26:31 2021

@author: localuser
"""

import imp
import numpy as np
import matplotlib.pyplot as plt
import waveguide
import LWIRArray

print(__name__)

lumapi = imp.load_source("lumapi","C:\\Program Files\\Lumerical\\v202\\api\\python\\lumapi.py") 

#waveguide.waveguide(lumapi)

#    nm ='C:\\Users\\localuser\\Documents\\Interconnect\\filename_' + str(3000+(i-1)*10)+'.ldf'
laserNumber = 4
detectorNumber = 1
wl_start = 1548
wl_stop = 1557
N=30
power_o, power, power_e = LWIRArray.LWIRArray(lumapi, laserNumber, detectorNumber, wl_start, wl_stop, N)

for i in range(0,detectorNumber):
    for j in range(0,laserNumber):
        arg=np.argsort(power[i,j,1])
        power[i,j,1] = power[i,j,1][arg]
        power[i,j,0] = power[i,j,0][arg]
            
        power_o[i,j,1] = power_o[i,j,1][arg]
        power_o[i,j,0] = power_o[i,j,0][arg]
        
        power_e[i,j,1] = power_e[i,j,1][arg]
        power_e[i,j,0] = power_e[i,j,0][arg]


data_to_save=[power_o, power, power_e]
np.save('Result\\'+ str(laserNumber) + '_' + str(detectorNumber) + '_' + str(wl_start) + '_' + str(wl_stop) + '_' + str(N) + '_datafile.npy', data_to_save)

plt.figure()
for i in range(0,detectorNumber):
    for j in range(0,laserNumber):
        plt.plot(power_o[i,j,1]*1e6,power_o[i,j,0])
plt.show()
plt.savefig('Result\\Optical_power_' + str(laserNumber) + '_' + str(detectorNumber) + '_' + str(wl_start) + '_' + str(wl_stop) + '_' + str(N) + '.png')

plt.figure()
for i in range(0,detectorNumber):
    for j in range(0,laserNumber):
        plt.plot(power[i,j,1]*1e6,(power[i,j,0]))
plt.show()
plt.savefig('Result\\Electrical_power_' + str(laserNumber) + '_' + str(detectorNumber) + '_' + str(wl_start) + '_' + str(wl_stop) + '_' + str(N) + '.png')

plt.figure()
for i in range(0,detectorNumber):
    for j in range(0,laserNumber):
        plt.plot(power_e[i,j,1]*1e6,power_e[i,j,0])
plt.show()
plt.savefig('Result\\RF_power_' + str(laserNumber) + '_' + str(detectorNumber) + '_' + str(wl_start) + '_' + str(wl_stop) + '_' + str(N) + '.png')
        
