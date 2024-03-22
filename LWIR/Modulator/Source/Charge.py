# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 16:05:54 2021

@author: m.ryabko
"""

from geom import geometry


def Charge(lumapi,period, diameter):
    model = lumapi.DEVICE()

    s_m, box, P_diffusion, N_diffusion = geometry(lumapi, model, period, diameter, False)
    
    model.addchargesolver()
    model.set("solver type", "newton")
    model.set("fermi statistics", 1)
    model.set("global iteration limit", 100)
    
    model.select("simulation region")
    model.set("dimension" ,4)
    model.set("x",0)
    model.set("y",0)
    model.set("z min",0)
#    model.set("background material" , "Air")
    
    model.set("x span",15e-6)
    model.set("y span",6e-6)
    model.set("z max",3e-6)
    
    model.adddope()
    model.set("name","whole")
    model.set("dopant type","p")
    model. set("concentration",1e21) # SI unit (/m3)
    model.set("x",box['x'])
    model.set("x span",box['x_span'])
    model.set("y",box['y'])
    model.set("y span",box['y_span'])
    model.set("z",box['z'])
    model.set("z span",box['z_span'])
    
    model.adddiffusion()
    model.set("name","pplus")
    model.set("dopant type","p")
    model.set("source face","upper z")
    model.set("junction width",0.1e-6)
    model.set("distribution function", "gaussian")
    model.set("concentration",2e24) # SI unit (/m3)
    model.set("ref concentration",1e14) 
    model.set("x",P_diffusion['x'])
    model.set("x span",P_diffusion['length'])
    model.set("y min",(s_m['y_span_monitor']-1e-6)/2+2e-7)
    model.set("y max",box['y_span']/2+2e-7)
    model.set("z",P_diffusion['z'])
    model.set("z span",P_diffusion['height']+2e-6)
    
    model.adddiffusion()
    model.set("name","nplus")
    model.set("dopant type","n")
    model.set("source face","upper z")
    model.set("junction width",0.1e-6)
    model.set("distribution function", "gaussian")
    model.set("concentration",2e24) # SI unit (/m3)
    model.set("ref concentration",1e14) 
    model.set("x",N_diffusion['x'])
    model.set("x span",N_diffusion['length'])
    model.set("y max",-(s_m['y_span_monitor']-1e-6)/2-2e-7)
    model.set("y min",-box['y_span']/2-2e-7)
    model.set("z",N_diffusion['z'])
    model.set("z span",N_diffusion['height']+2e-6)
    
    model.adddiffusion()
    model.set("name","pwell")
    model.set("dopant type","p")
    model.set("source face","upper z")
    model.set("junction width",0.2e-6)
    model.set("distribution function", "gaussian")
    model.set("concentration",5e26) # SI unit (/m3)
    model.set("ref concentration",1e14) 
    model.set("x",P_diffusion['x'])
    model.set("x span",P_diffusion['length'])
    model.set("y",P_diffusion['y'])
    model.set("y span",P_diffusion['width'])
    model.set("z",P_diffusion['z'])
    model.set("z span",P_diffusion['height']+2e-9)
 
    model.adddiffusion()
    model.set("name","nwell")
    model.set("dopant type","n")
    model.set("source face","upper z")
    model.set("junction width",0.2e-6)
    model.set("distribution function", "gaussian")
    model.set("concentration",5e26) # SI unit (/m3)
    model.set("ref concentration",1e14) 
    model.set("x",N_diffusion['x'])
    model.set("x span",N_diffusion['length'])
    model.set("y",N_diffusion['y'])
    model.set("y span",N_diffusion['width'])
    model.set("z",N_diffusion['z'])
    model.set("z span",N_diffusion['height']+2e-9)
    
    
    
    
    
    model.addelectricalcontact()
    model.set("name", "P_contact")
    model.set("surface type", "solid")
    model.set("solid", "pwell_contact")
    model.set("sweep type", "range")
    model.set("range start", 0)
    model.set("range stop", 1.2)
    model.set("range num points", 11)
    
    
    model.addelectricalcontact()
    model.set("name", "N_contact")
    model.set("surface type", "solid")
    model.set("solid", "nwell_contact")
    
    model.addsurfacerecombinationbc()
    model.set("name", "sr_AL_Si")
    model.set("electron velocity", 1e5)
    model.set("hole velocity", 1e5)
    model.set("surface type", "material:material")
    model.set("material 1", "Si")
    model.set("material 2", "Al")
    
    model.addsurfacerecombinationbc()
    model.set("name", "sr_SiO2_Si")
    model.set("electron velocity", 0.1)
    model.set("hole velocity", 0.1)
    model.set("surface type", "material:material")
    model.set("material 1", "Si")
    model.set("material 2", "SiO2")
    
    model.addrect()
    model.set("name", "sox")
    model.set("x",0)
    model.set("x span", box["x_span"]+1e-6)
    model.set("y",0)
    model.set("y span", box["y_span"]+1e-6)
    model.set("z",0+2e-6)
    model.set("z span", box["z_span"])
    model.set("material", "SiO2")
    model.set("mesh order", 5)
    model.set("alpha", 0.1)
    
    
    model.addchargemonitor()
    model.set("name", "charge_monitor")
    model.set("monitor type", "3D")
    model.set("x",box['x'])
    model.set("x span",box['x_span'])
    model.set("y",box['y'])
    model.set("y span",box['y_span'])
    model.set("z",box['z'])
    model.set("z span",box['z_span'])
    model.set("save data", 1)
    model.set("filename", "charge")
    
    model.addchargemonitor()
    model.set("name", "charge_monitor_small")
    model.set("monitor type", "2D x-normal")
    model.set("x",s_m['x_monitor'])
#    model.set("x span",s_m['x_span_monitor'])
    model.set("y",s_m['y_monitor'])
    model.set("y span",s_m['y_span_monitor'])
    model.set("z",s_m['z_monitor'])
    model.set("z span",s_m['z_span_monitor'])
#    model.set("save data", 1)
#    model.set("filename", "charge")
    
    model.save("Charge.ldev")
    model.run()
    