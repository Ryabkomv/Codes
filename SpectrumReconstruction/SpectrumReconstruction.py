   
#from PIL import Image
from matplotlib import pyplot as plt
import matplotlib.image as img
import numpy as np
import scipy as sp
import pickle
from scipy.interpolate import interp1d
from random import randint as rnd

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
    
#averaging window width
n=5
    

for j in range(0,8):
    x_ult=[]
    final_y=[]
    # peak positions
    peak=(([1459.16, 1661.97], "Actin"),  
          ([1659, 1448], "keratin"),  
          ([1448,1266], "collagen  type  III"),  
          ([1448,1301], "collagen type I"),  
          ([1006,1580], "hemoglobin_1"),  
          ([1450,1310], "phosphatidylcholine"),  
          ([1443.94, 1667,6], "triolein"),  
          ([1633,1360], "water"))
    file_name = (peak[j][1])
    peak1 = (peak[j][0][0])
    peak2 = (peak[j][0][1])
    
    
    image = img.imread(file_name+".png")
    #jpgfile = Image.open("1.png")
    plt.figure(1)
    #plt.plot(image[:,:,1])
    plt.imshow(image[:,:,1])
    size_x=np.shape(image[:,:,1])[0]
    size_y=np.shape(image[:,:,1])[1]
    
    a=np.array(range(0,size_x))
    x=np.array(range(0,size_y))
    f=[]
    
    for i in range(0,size_y):
        tmp = a[image[:,i,1]<1]
        
        f=np.append(f,tmp[0])
        
    new_y = sp.interpolate.interp1d(x, 1-f, kind='cubic')(x)
    plt.figure(2)
    
    
    
            
    #plt.plot(x,1-f)
    a = moving_average(new_y,n)
    a = a-np.min(a)
    a = a/np.max(a)
    #window width for peak detection
    peak_x=[]
    peak_y=[]
    w=50
    i=0
    while i < np.shape(a)[0]-w:
        flag=0
        cur_y = a[i:i+w]
        curr_max = np.max(cur_y)
        if (curr_max>a[i]) and (curr_max>a[i+w]):
            
            peak_x=np.append(peak_x,np.where(cur_y==curr_max)[0][0]+i)
            peak_y=np.append(peak_y,curr_max)
            flag=w
        
        i=i+flag+1
        
    a_x = x[0:(size_y-(n-1))]
    plt.plot(a_x,a)
    
    plt.plot(peak_x,peak_y,'g^')
    plt.grid() 
    tmp = np.sort(peak_y)
    spec_1_y = tmp[np.shape(tmp)[0]-1];
    spec_2_y = tmp[np.shape(tmp)[0]-2]
    spec_1_x = peak_x[peak_y==tmp[np.shape(tmp)[0]-1]]
    spec_2_x = peak_x[peak_y==tmp[np.shape(tmp)[0]-2]]
    
    x_ult = (peak1-peak2)*a_x/(spec_1_x-spec_2_x)+(peak2*spec_1_x-peak1*spec_2_x)/(spec_1_x-spec_2_x)
    
  
    
   # fig = plt.figure(3)  
   # ax = fig.gca()
   # ax.set_xticks(np.arange(400,1800,100))
    #ax.set_yticks(np.arange(0,1.,0.1))                          
   # l1=plt.plot(x_ult,a) 
    #first_legend = plt.legend(handles=[l1], loc=1)
    #ax = plt.gca().add_artist(first_legend)
   # plt.legend((l1),
            # (file_name,),
           #   loc='upper left',
            #  fontsize=18)
   # plt.grid()  
    #plt.show()                            
    
    final_x = np.array([[xx / 10.0 for xx in range(8500, 16801)]])
    f = sp.interpolate.interp1d(x_ult, a, kind='cubic')
    final_y = f(final_x)
    #plt.figure(4) 
    #plt.plot(final_x,final_y)
    
    if (j == 0):
         spectra = np.append(final_x,final_y,0)
         
    else:
        spectra = np.append(spectra,final_y,0)
        
    #with open('Raman Spectra/'+file_name + '.txt', 'wb') as f:
        #pickle.dump((final_x,final_y),f)
     
#spectra = np.append(spectra,final_x) 
with open('Raman Spectra/spectra.txt', 'wb') as f:
    pickle.dump(spectra,f)
    
    
    #f = open('text1.txt', 'w')
   #for i in final_y:
        #f.write(i.astype('str') + '\n')
    #f.close()
