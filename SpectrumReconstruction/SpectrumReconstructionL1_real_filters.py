import numpy as np
import matplotlib.pyplot as plt
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


result = np.array(list(csv.reader(open("Spectrums.csv", "rt"), delimiter=";"))).astype("float")

wl = np.array([np.linspace(800, 900, np.size(result,0))])

D = np.transpose(np.loadtxt('filters1.txt'))
D=D[:,:]/np.max(D)
#filterRes = 0.003

#filterStep = 0.001
kernelRes = 4
kernalStep = 1

spectrum = (np.array([result[:,3]]))[0]
waveLength = (np.array([np.linspace(800, 900, 201)]))






Wlambda = waveLength[0][-1]-waveLength[0][0]
# number of measurements
N=int(round(Wlambda/kernalStep))+1




#kernalStep = Wlambda/N
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
        
plt.figure(1)
plt.plot(waveLength[0],(Psi))
plt.show()

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
        
new_x = sp.interpolate.interp1d(wl[0], spectrum, kind='cubic')(waveLength[0])

#new_x = D[60,:]+D[10,:]
y = np.dot(D, new_x)

y = y + np.max(y)*0*np.random.rand(M)/100


A = np.dot(D, Psi)




gamma = 0.99
tau = 2.5

alpha0 = 100
betta = 2

v = np.ones(N)
s = np.ones(N)
At = np.transpose(A)
j=0
delta = 10
BB = calcF(A,y,At,s,v,tau)
print(BB)
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
plt.plot(waveLength[0], new_x)
plt.plot(waveLength[0], xx)
plt.show()
print(np.std(new_x-xx))
