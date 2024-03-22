# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 11:01:30 2017

@author: ryabko
"""
import  matplotlib.pyplot as plt
import numpy as np

def Lorentz(R,R0,G):
    F = np.zeros(R.size)
    F = np.real(-1j*G/(R-R0-1j*G))
    return F

def GlSpectrum(R):
    F = 3*Lorentz(R,436.4,10)+3*Lorentz(R,456.1,10)+4.5*Lorentz(R,525.7,25)
    F = F + 0.6*Lorentz(R,854.9,15)+Lorentz(R,911.7,15)+3*Lorentz(R,1065,10)+4*Lorentz(R,1126.4,14)
    F = F + 0.4*Lorentz(R,1270.0,14)+1.3*Lorentz(R,1365.1,25)+Lorentz(R,1456.2,10)+0.25*Lorentz(R,1645.0,10) 
    F = F + 0.2 + (1800**2-R**2)/(2*1800**2)
    M = F.max()
    F = F/M
    return F
    
wl = np.array([np.linspace(100, 1600, 1000)])
K = GlSpectrum(wl)
plt.plot(wl[0],K[0])
plt.show()


import numpy as np
import cv2
from matplotlib import pyplot as plt
imgL = cv2.imread('tsukuba_l.png',0)
imgR = cv2.imread('tsukuba_r.png',0)
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
plt.show()