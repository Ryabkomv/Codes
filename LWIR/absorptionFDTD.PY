# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 13:54:28 2021

@author: m.ryabko
"""
import numpy as np
from single_pixel import single_pixel
import time
import model_parameters
from substrate import substrate

def absorptionFDTD(lumapi):
    model = lumapi.FDTD()
    parameters=model_parameters.Parameters(lumapi, model)
    
    substrate(lumapi, model, parameters)
    
    ab = single_pixel(lumapi, model, parameters)

    
    model.addfdtd()
    model.set("dimension", "3D")
    model.set("x", parameters.FDTD_x)
    model.set("y", parameters.FDTD_y)
    model.set("z", parameters.FDTD_z)
    model.set("x span", parameters.FDTD_x_span)
    model.set("y span", parameters.FDTD_y_span)
    model.set("z span", parameters.FDTD_z_span)
  
    model.set("mesh accuracy", parameters.FDTD_mesh_accuracy)
    model.set("x min bc", "Periodic")
    model.set("y min bc", "Periodic")
    model.set("z min bc", "PML")
    model.set("z max bc", "PML")
    model.set("background material","<Object defined dielectric>");
    model.set("index", 1);
    
    model.addobject("pabs_adv")
    model.set("name", "absorbtion_resonator")
    model.set("x", ab.x)
    model.set("y", ab.y)
    model.set("x span", ab.outer_radius1*2)
    model.set("y span", ab.outer_radius1*2)
    model.set("z", (ab.z_min+ab.z_max )/2)
    model.set("z span", ab.z_max - (ab.z_min))
    
    model.addmesh()
    model.set("name", "mesh")
    model.set("x", ab.x)
    model.set("y", ab.y)
    model.set("x span", ab.outer_radius1*2)
    model.set("y span", ab.outer_radius1*2)
    model.set("z", (ab.z_min+ab.z_max )/2)
    model.set("z span", ab.z_max - (ab.z_min))
    model.set("override x mesh",1)
    model.set("override y mesh",1)
    model.set("override z mesh",1)
    model.set("dx",ab.outer_radius1*2/100)
    model.set("dy",ab.outer_radius1*2/100)
    model.set("dz",(ab.z_max - ab.z_min)/20)
          
    model.addobject("pabs_adv")
    model.set("name", "absorbtion_whole")
    model.set("x", parameters.FDTD_x)
    model.set("y", parameters.FDTD_y)
    model.set("x span", parameters.FDTD_x_span)
    model.set("y span", parameters.FDTD_y_span)
    model.set("z", parameters.FDTD_z)
    model.set("z span", parameters.FDTD_z_span)
       
    model.setglobalmonitor("frequency points",parameters.midIR_Nfreq)
    model.addplane()
    model.set("injection axis", "z")
    model.set("direction", "backward")
    model.set("x", parameters.FDTD_x)
    model.set("x span", parameters.FDTD_x_span+2e-6)   
    model.set("y", parameters.FDTD_y);
    model.set("y span", parameters.FDTD_x_span+2e-6)   
    model.set("z", parameters.z + parameters.FDTD_z_span-parameters.space_above_model+1E-6);
    model.set("wavelength start", parameters.midIR_wl_start);
    model.set("wavelength stop", parameters.midIR_wl_stop);
    
    model.save("absorption_fdtd.fsp")
    time.sleep(3)
    model.run()
    time.sleep(3)
    
    
    Pabs = model.getresult("absorbtion_resonator","Pabs")
    
    Pabs_total = model.getresult("absorbtion_whole","Pabs_total")
        
    np.save('data\\resonator_absorption.npy', Pabs, allow_pickle = True)
    np.save('data\\total_absorption.npy', Pabs_total, allow_pickle = True)