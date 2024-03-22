# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 13:27:54 2021

@author: anton
"""

import os.path
import copy
import numpy as np
from geometry import geometry

def heat(lumapi, recalc = True):
    
    #check if previous calculations were made
    if(not (os.path.isfile('geometry.npy') and os.path.isfile('heat_distr.npy') and os.path.isfile('absorbed_fraction.npy') )):
        return 0,0
  
    IR_power = 10E-3        # Watts    
  
    if(not recalc):
        if(os.path.isfile('thermal.npy')):
            box = np.load('geometry.npy',  allow_pickle = True)
            box = box.item()
            
            thermal = np.load('thermal.npy',  allow_pickle = True)
            thermal = thermal.item()
            
            Pabs_total = np.load('absorbed_fraction.npy', allow_pickle = True)
            Pabs_total = Pabs_total.item()
                        
            midIR_wls = Pabs_total['lambda'][:,0]
               
            dl = np.diff(midIR_wls)
            dl = np.abs(np.concatenate([dl, np.array([dl[-1]])]))
         
            coef = IR_power / np.sum(dl/(midIR_wls**5 * ( np.exp(4.348E-5/midIR_wls) - 1)))
            
            bf = 0
            for i in range(np.size(midIR_wls)):
                bf = bf + Pabs_total['Pabs_total'][i] * dl[i] * coef / (midIR_wls[i]**5 * ( np.exp(4.348E-5/midIR_wls[i]) - 1))
                
            P_mr = bf # power absorbed in MR for thermal conductance calculation
            
            x = np.copy(thermal['x'][:,0,0])
            y = np.copy(thermal['y'][:,0,0])
            z = np.copy(thermal['z'][:,0,0])
            T = np.copy(thermal['T'][:,0,0])
            mask = ((x**2 + y**2)<box['r']**2 ) & (z < box['z_max']) & (z > box['z_max'] - 0.5E-6)
            
            T_av = np.mean(T[mask])
            G = P_mr/(T_av - 300)
            
            return T_av, G
                    

    
    model = lumapi.DEVICE()

    model.addmodelmaterial()
    model.set("name", "Air")
    model.addmaterialproperties("HT","Air")
    Air = "Air"
    
    box = geometry(lumapi,model)
    
    model.addrect()
    model.set("name","Air")
    model.set("alpha",0.3)
    model.set("x",0)
    model.set("x span",  box['x_span'])
    model.set("y",0)
    model.set("y span", box['y_span'])
    model.set("z min",0)
    model.set("z max", box['z_max']+0.5E-6)
    model.set("material", "Air")
    model.set("mesh order", 20)
    
    model.select("simulation region")
    model.set("dimension", "3D")
    model.set("x", 0)
    model.set("x span", box['x_span'])
    model.set("y",0)
    model.set("y span", box['y_span'])
    model.set("z min", 0)
    model.set("z max", box['z_max'])
    
    
    Pabs = np.load('heat_distr.npy', allow_pickle = True)
    Pabs = Pabs.item()
    
    Pabs_total = np.load('absorbed_fraction.npy', allow_pickle = True)
    Pabs_total = Pabs_total.item()

        
    midIR_wls = Pabs['lambda'][:,0]
       
    dl = np.diff(Pabs['lambda'][:,0])
    dl = np.abs(np.concatenate([dl, np.array([dl[-1]])]))
 
    coef = IR_power / np.sum(dl/(midIR_wls**5 * ( np.exp(4.348E-5/midIR_wls) - 1)))
    
    buf = Pabs['Pabs'][:,:,:,0]*0
    bf = 0
    for i in range(np.size(midIR_wls)):
        buf = buf + Pabs['Pabs'][:,:,:,i] * dl[i] * coef / (midIR_wls[i]**5 * ( np.exp(4.348E-5/midIR_wls[i]) - 1))
        bf = bf + Pabs_total['Pabs_total'][i] * dl[i] * coef / (midIR_wls[i]**5 * ( np.exp(4.348E-5/midIR_wls[i]) - 1))
        
    P_mr = bf # power absorbed in MR for thermal conductance calculation
    
    
    Pabs_int = copy.deepcopy(Pabs)
    
    Pabs_int['Pabs'] = buf
    del Pabs_int['f']
    del Pabs_int['lambda']
    del Pabs_int['Lumerical_dataset']['parameters']
    
    model.addheatsolver()
    
    model.addimportheat("HEAT")
    model.importdataset(Pabs_int)
    model.set("selected attribute", "Pabs")
    
    model.addtemperaturebc("HEAT")
    model.set("name","T_trans")
    model.set("bc mode","steady state")
    model.set("sweep type","single")
    model.set("Temperature",300)
    model.set("surface type","solid:simulation region")
    model.set("solid","Substrate")
    model.set("z min",1)
    
    model.addtemperaturemonitor("HEAT")
    model.set("name","Tmap")
    model.set("monitor type", "2D x-normal")  # 2D z-normal
    model.set("x",0)
    model.set("y span", box['y_span'])
    model.set("y",0)
    model.set("z min", 0)
    model.set("z max", box['z_max']) 
    
    model.save("test_heat.ldev")
    model.run()
    
    thermal = model.getresult("HEAT","thermal")
    np.save('thermal.npy', thermal, allow_pickle = True)
    
    x = np.copy(thermal['x'][:,0,0])
    y = np.copy(thermal['y'][:,0,0])
    z = np.copy(thermal['z'][:,0,0])
    T = np.copy(thermal['T'][:,0,0])
    mask = ((x**2 + y**2)<box['r']**2 ) & (z < box['z_max']) & (z > box['z_max'] - 0.5E-6)
    
    T_av = np.mean(T[mask])
    G = P_mr/(T_av - 300)
    
    return T_av, G