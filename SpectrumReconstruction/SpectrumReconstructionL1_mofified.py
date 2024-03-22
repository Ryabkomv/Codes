# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 10:44:47 2017

@author: ryabko
"""



import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy.interpolate as sp
import random

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

result = np.array(list(csv.reader(open("Spectrums.csv", "rt"), delimiter=";"))).astype("float")

filterRes = 0.004

filterStep = 0.001
kernelRes = 0.002
kernalStep = 0.002

x = result[:,3]
lambd = np.array([10000/result[:,0]])




Wlambda = lambd[0][0]-lambd[0][-1]
# number of measurements
#N=int(round(Wlambda/kernalStep))+1


#kernalStep = Wlambda/N
N = (1*int(round(Wlambda/kernalStep))+1) 

# number of filters
M=(1*int(round(Wlambda/filterStep))+10) 
deltaLambdaN = Wlambda/N

N1 = N*10
lambdNew = np.array([np.linspace(lambd[0][-1], lambd[0][0],N)])
lambdNew1 = np.array([np.linspace(lambd[0][-1], lambd[0][0],N1)])
#lambdNew = lambd

for i in range(0,N):
    tmp = np.transpose((np.exp(-((lambdNew-(lambdNew[0][-1]-kernalStep*i))/(kernelRes))**2)))
 
    if (i>0):
        Psi = np.append(Psi,tmp,1)
    else:
        Psi = tmp

for i in range(0,M):
    tmp=np.zeros(shape=(1,N))
    tmp1=np.zeros(shape=(1,N*10))
    for j in range(0,20):
        k = random.randint(0,M)-5
#        k=i
        tmp = tmp+(np.exp(-((lambdNew-(lambdNew[0][-1]-filterStep*k))/(filterRes*1))**2))
        tmp1 = tmp1+(np.exp(-((lambdNew1-(lambdNew1[0][-1]-filterStep*k))/(filterRes*1))**2))
    if (i>0):
        D = np.append(D,tmp,0)
        D1 = np.append(D1,tmp1,0)
    else:
        D = tmp
        D1 = tmp1
#D=D[:,:]/np.max(D)
        #ff = (np.exp(-((lambdNew[0]-(lambdNew[0][-1]-filterStep*20.5))/(0.01*1))**2)).transpose()   
new_x = sp.interpolate.interp1d(lambd[0], x, kind='cubic')(lambdNew[0])
#new_x = D[:,120] +0.2*D[:,10]+ff
new_x1 = sp.interpolate.interp1d(lambd[0], x, kind='cubic')(lambdNew1[0])
#new_x=D[106,:] + 0.3*D[16,:]
y = np.dot(D,new_x)

y1 = (np.dot(D1,new_x1)*(lambdNew1[0][1]-lambdNew1[0][0])/(lambdNew[0][1]-lambdNew[0][0]))#*np.sum(D1, axis=1)/np.max(np.sum(D1, axis=1))
y = y1 + np.max(y1)*0*np.random.rand(M)/100

#k=np.sum(D1, axis=1)
A = np.dot(D,Psi)

plt.figure(1)
plt.plot(lambdNew[0],np.transpose(Psi))
plt.show()
#
plt.figure(3)
plt.plot(lambdNew1[0],np.transpose(D1[1,:]))
plt.show()


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

plt.figure(2)
plt.plot(lambdNew[0], new_x)
plt.plot(lambdNew[0], xx)
plt.show()
print(np.std(new_x-xx))