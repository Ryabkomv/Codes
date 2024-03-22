# -*- coding: utf-8 -*-
"""
Created on Fri May  7 09:36:23 2021

@author: m.ryabko
"""
import numpy as np
    
def materials(lumapi, model, modes = False):
    if(type(model) == lumapi.FDTD):
        Si = "Si (Silicon) - Palik"
        SiO2 = "SiO2 (Glass) - Palik"
        Si3N4 = "Si3N4 (Silicon Nitride) - Kischkat"    # Mid IR n,k data
        Air = "etch"
        Al = "Al (Aluminium) - Palik"
        if(modes):
            #print("true")
            # create new index perturbation material
            new_mat = model.addmaterial("Index perturbation");
            model.setmaterial(new_mat,"base material", Si);
            model.setmaterial(new_mat,"Include np density", True);
            model.setmaterial(new_mat,"Include temperature effects", False);
            model.setmaterial(new_mat,"np density model", "Soref and Bennett");
            # Si data - Table 4  https://arxiv.org/ftp/physics/papers/0606/0606168.pdf 
#            model.setmaterial(new_mat,"dn/dt", 1.87E-4);
#            model.setmaterial(new_mat,"dk/dt", 0.0);
            Si = "Si_dnp"
            model.setmaterial(new_mat,"name", Si);
#            model.setcolor(np.array([0.5,0.2,0.6,0.5]))
            
            # SiO2 data - Fig 1 https://sci-hub.do/https://doi.org/10.1088/0022-3727/16/5/002
            # dn/dT ~ 12.08E-6 @ 1.5 um
            
            # Nitride and oxide data https://www.osapublishing.org/ol/abstract.cfm?uri=ol-38-19-3878
            # from microring resonators
            # dn/dT (oxide) = 0.95E-5
            # dn/dT (nitride) = 2.45E-5
#            new_mat = model.addmaterial("Index perturbation");
#            model.setmaterial(new_mat,"base material", SiO2);
#            model.setmaterial(new_mat,"include np density", False);
#            model.setmaterial(new_mat,"dn/dt", 0.95E-5);
#            model.setmaterial(new_mat,"dk/dt", 0.0);
#            SiO2 = "SiO2_dT"
#            model.setmaterial(new_mat,"name", SiO2);
#            
#            new_mat = model.addmaterial("Index perturbation");
#            model.setmaterial(new_mat,"base material", Si3N4);
#            model.setmaterial(new_mat,"include np density", False);
#            model.setmaterial(new_mat,"dn/dt", 2.45E-5);
#            model.setmaterial(new_mat,"dk/dt", 0.0);
#            Si3N4 = "Si3N4_dT"
#            model.setmaterial(new_mat,"name", Si3N4);            
            
    elif(type(model) == lumapi.DEVICE):
        model.addmodelmaterial()
        model.set("name", "Si")
        model.addmaterialproperties("HT","Si (Silicon)")
        model.select("materials::Si")
        model.addmaterialproperties("CT","Si (Silicon)")
        model.set("recombination.trap assisted.taun.constant", 1e-7)
        model.set("recombination.trap assisted.taup.constant", 2e-7)
        Si = "Si"
        
        
        model.addmodelmaterial()
        model.set("name", "SiO2")
        model.addmaterialproperties("HT","SiO2 (Glass) - Sze")
        model.select("materials::SiO2")
        model.addmaterialproperties("CT","SiO2 (Glass) - Sze")
        SiO2 = "SiO2"
        
        
        model.addmodelmaterial()
        model.set("name", "Al")
        model.addmaterialproperties("HT","Al (Aluminium) - CRC")
        model.select("materials::Al")
        model.addmaterialproperties("CT","Al (Aluminium) - CRC")
        Al = "Al"
        
        
        model.addmodelmaterial()
        model.set("name", "Si3N4")
        model.set("color", np.array([0.5,0.2,0.6,0.5]))
        model.addmaterialproperties("HT","Si3N4 (Silicon nitride) - Sze")
        model.select("materials::Si3N4")
        model.addmaterialproperties("CT","Si3N4 (Silicon nitride) - Sze")
        Si3N4 = "Si3N4"
        
        model.addmodelmaterial()
        model.set("name", "Air")
        model.addmaterialproperties("HT","Air")
        model.select("materials::Air")
        model.addmaterialproperties("CT","Air")
        Air = "Air"
        
    materials = {"Air"   : Air,
                 "Si"    : Si,
                 "SiO2"  : SiO2,
                 "Si3N4" : Si3N4,
                 "Al"    : Al }
    return materials
        