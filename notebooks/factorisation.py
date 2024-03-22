## -*- coding: utf-8 -*-
#"""
#Created on Wed Jul  8 14:20:23 2020
#
#@author: m.ryabko
#"""
import math 
import time
import matplotlib.pyplot as plt
import numpy as np
#N = 7779674673564589
#step=math.floor(N/100)
#elapsed=[]
#for j in range(2,N,step):
#    NN=j
#    n = math.ceil(NN**0.5)
#
#    
#    primeArray=[]
#    t = time.time()
#    for i in range(2,n):
#    
#        while (NN%i==0):
#            if ( (len(primeArray)==0) or (primeArray[-1][0] !=i) ):
#                primeArray.append([i,0])
#            primeArray[-1][1]=primeArray[-1][1]+1
#            NN=NN/i
#            
#    if (NN>1):
#        primeArray.append([math.ceil(NN),0])
#        
#    elapsed.append(time.time() - t)
#y = np.array(range(2,N,step))
#plt.plot(range(2,N,step), elapsed, range(2,N,step), 5.5e-9*np.log(y)*y**0.5)  
y=[]
z=[]
t=range(1,60)
for i in t:
    y.append(math.log(math.factorial(i)))
    z.append(math.log(i)*i/1.4)
plt.plot(t, y, t, z)
    