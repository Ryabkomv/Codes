# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 15:59:47 2017

@author: ryabko
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import struct
from PIL import Image
import csv
import scipy.interpolate as sp

def calcC(A,y,At,s):
    return At@(y-np.dot(A,s))
    
def calcSV1(s,v):
    return np.sum(np.dot(np.diag(s),np.diag(v)),1)  

def calcF(A,y,At,s,v,tau):
    return np.append(np.ones(np.shape(s)[0]) - v - tau*calcC(A,y,At,s),calcSV1(s,v))
    
def checkDecrease(A,y,At,s,v,tau, alpha, deltaS, deltaV):
    val1 = v + alpha*deltaV
    val2 = s + alpha*deltaS
    return ((sum(val1>0)==np.shape(val1))&(sum(val2>0)==np.shape(val2))&(sum(calcF(A,y,At,s,v,tau)**2) > sum(calcF(A,y,At,s + alpha*deltaS,v + alpha*deltaV,tau)**2)))
   

def clear_all():
    """Clears all the variables from the workspace of the spyder application."""
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue

        del globals()[var]   
        
if __name__ == "__main__":
    clear_all()    

from array import *
    

buf_size=(2**10)*2
#buf=ctypes.create_string_buffer(buf_size)
new_buf=[]
A=[]
endian='<h'
path = 'C://WinPython-64bit-3.5.2.3Qt5/SpectrumReconstruction/SAIT/871.000000_1474.raw'
with open(path,'rb') as f:
    while True:
        st=f.read(buf_size)
        l=len(st)
        if l==0: 
            break
        fmt=endian[0]+str(int(l/2))+endian[1]
        
        new_buf+=(struct.unpack_from(fmt,st))

na=np.array(new_buf) 

#th = 50       
#na[na<th]=0
#na[na>th-1]=1000
nb = na.reshape(480,640)
nc=nb*0
#nd=nb*0
#ne=nb*0
#nc[235:285, 312:362]=100
#nd[15:65, 312:362]=100
#nd[180:230, 202:252]=100


#im=Image.fromarray(nb).rotate(0.65, expand=1)
#im.show()

#nc = np.array(im.getdata()).reshape(np.size(im))

for i in range(0,8):
    for j in range(0,11):
        tmp = nb[(15+55*i):(55*i+50+15),(37+55*j):(55*j+50+37)]
        mx = np.max(tmp)
        tmp[tmp<mx/2]=0

        A=np.append(A,np.mean(tmp))
        nc[(15+55*i):(55*i+50+15),(37+55*j):(55*j+50+37)]=100
A = A.reshape(8,11)
B = A[0:4,0:8]+A[4:8,0:8]
y = np.append(B[1:4,:].reshape(1,24), B[0:1,:])
plt.figure(1)
plt.imshow(nc+nb)
plt.show()

data = np.loadtxt('filters.txt')
plt.figure(2)
plt.plot(np.linspace(800, 900, np.size(data,0)),data[:,:])
plt.show()
#with open('SAIT/800.000000_55.raw', mode='rb') as f:
#        spectra = f.read() 
###        
###S=spectra[1:9,:]for i
#for i in range(0,20):
#    B= np.append(B,struct.unpack('bb', spectra[i:i+2]))
#i=0
#bytes_read = open(path, "rb").read()
#for b in bytes_read:
#    B=np.append(B,b)
#    i=i+1


result = np.array(list(csv.reader(open("Spectrums.csv", "rt"), delimiter=";"))).astype("float")

wl = np.array([np.linspace(800, 900, np.size(result,0))])

D = np.transpose(np.loadtxt('filters.txt'))
D=D[:,:]/np.max(D)
#filterRes = 0.003

#filterStep = 0.001
kernelRes = 0.5
kernalStep = 0.5

spectrum = (np.array([result[:,3]]))[0]
waveLength = (np.array([np.linspace(800, 900, 201)]))






Wlambda = waveLength[0][-1]-waveLength[0][0]
# number of measurements
N=int(round(Wlambda/kernalStep))+1




kernalStep = Wlambda/N
# number of filters
M=np.size(D,0)

deltaLambdaN = Wlambda/N



#lambdNew = lambd
Psi=np.array([])
for i in range(0,N):
    tmp = np.transpose((np.exp(-((waveLength-(waveLength[0][-1]-kernalStep*i))/(kernelRes))**2)))
 
    if (i>0):
        Psi = np.append(Psi,tmp,1)
    else:
        Psi = tmp
        
#plt.figure(1)
#plt.plot(waveLength[0],(Psi))
#plt.show()
#
plt.figure(3)
plt.plot(waveLength[0],np.transpose(D))
plt.show()
#for i in range(0,M):
#    tmp = (np.exp(-((lambdNew-(lambdNew[0][-1]-filterStep*i))/(filterRes*1))**2))
#    tmp1 = (np.exp(-((lambdNew1-(lambdNew1[0][-1]-filterStep*i))/(filterRes*1))**2))
#    if (i>0):
#        D = np.append(D,tmp,0)
#        D1 = np.append(D1,tmp1,0)
#    else:
#        D = tmp
#        D1 = tmp1
        
#new_x = sp.interpolate.interp1d(wl[0], spectrum, kind='cubic')(waveLength[0])


#y = np.dot(D, new_x)
#
y = y + np.max(y)*5*np.random.rand(M)/100


A = np.dot(D, Psi)




gamma = 0.99
tau = 20.5

alpha0 = 100
betta = 2

v = np.ones(N)
s = np.ones(N)
At = np.transpose(A)
j=0
delta = 10
while delta > 1e-15:
    j=j+1
    c = calcC(A,y,At,s)
    S = np.diag(s)
    V = np.diag(v)
    T1 = V+tau*np.dot(np.dot(S,At),A)
    T2 = tau*np.dot(S,c)+np.dot(S,v) - s - calcSV1(s,v)
    deltaS = np.dot(np.linalg.inv(T1),T2)
    deltaV = tau*(np.dot(np.dot(At,A),deltaS) -c)-v+np.ones(N)
    res = False
    i=0
    while ~ res:
        alpha = alpha0*gamma**i
        res = checkDecrease(A,y,At,s,v,tau, alpha, deltaS, deltaV)
#        print("i= " + str(i)+"  result:" + str(res) + "alpha= " + str(alpha))
        i=i+1
    v = v + alpha*deltaV
    s = s + alpha*deltaS 
    tau = betta*tau
    delta = sum((alpha*deltaS)**2)
    print(" j= " + str(j) + "  result: " +str(delta))
#T2 = np.linalg.inv(T1)
xx = np.dot(Psi,s)

plt.figure(5)
#plt.plot(waveLength[0], new_x)
plt.plot(waveLength[0], xx)
plt.show()
#print(np.std(new_x-xx))