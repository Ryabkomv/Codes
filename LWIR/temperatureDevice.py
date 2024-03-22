# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 15:45:38 2021

@author: m.ryabko
"""

import numpy as np
import copy
from double_pixel import double_pixel
from single_pixel import single_pixel
from substrate import substrate
import model_parameters

def temperatureDevice(lumapi,single_pix):

    model = lumapi.DEVICE()

    
    parameters=model_parameters.Parameters(lumapi, model)
    
    if (single_pix):
        substrate(lumapi, model, parameters)
        single_pixel(lumapi, model, parameters)
    else:
        double_pixel(lumapi, model, parameters)
    
    
    model.select("simulation region")
    model.set("dimension", "3D")
    model.set("x min", parameters.x_min)
    model.set("y min", parameters.y_min)
    model.set("x max", parameters.x_min+parameters.x_span)
    model.set("y max", parameters.x_min+parameters.y_span)
    model.set("z min", parameters.z)
    model.set("z max", parameters.z+parameters.z_span)
    Pabs = np.load('data\\resonator_absorption.npy', allow_pickle = True)
    Pabs = Pabs.item()
    
    Pabs_total = np.load('data\\total_absorption.npy', allow_pickle = True)
    Pabs_total = Pabs_total.item()

        
    midIR_wls = Pabs['lambda'][:,0]
       
    dl = np.diff(Pabs['lambda'][:,0])
    dl = np.abs(np.concatenate([dl, np.array([dl[-1]])]))
 
    coef = parameters.IR_power / np.sum(dl/(midIR_wls**5 * ( np.exp(4.348E-5/midIR_wls) - 1)))
    
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
    model.set("volume meshing", "advancing front")
    model.set("min edge length", parameters.min_edge_length)
    model.set("max edge length", parameters.max_edge_length)
    
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
    model.set("monitor type", "3D")  
    model.set("x min", parameters.x_min)
    model.set("y min", parameters.y_min)
    model.set("x max", parameters.x_min+parameters.x_span)
    model.set("y max", parameters.x_min+parameters.y_span)
    model.set("z min", parameters.z)
    model.set("z max", parameters.z+parameters.z_span)
    
    model.addtemperaturemonitor("HEAT")
    model.set("name","T_Res_1")
    model.set("monitor type", "2d z-normal")  
    model.set("x min", parameters.x_min)
    model.set("x max", parameters.x_min+parameters.x_span)
    model.set("y min", parameters.y_min)
    model.set("y max", parameters.y_min+parameters.y_span)
    model.set("z", parameters.substrate_height + parameters.box_height + parameters.slab_height/2)
    
    model.addtemperaturemonitor("HEAT")
    model.set("name","T_Res_2")
    model.set("monitor type", "linear x")  
    model.set("x min", parameters.x_min)
    model.set("x max", parameters.x_min+parameters.x_span)
    model.set("y", parameters.y)

    model.set("z", parameters.substrate_height + parameters.box_height + parameters.slab_height/2)
    
    model.save("temperatureDevice.ldev")
    model.run()
