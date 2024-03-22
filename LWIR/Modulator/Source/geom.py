# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 14:07:32 2021

@author: m.ryabko
"""

from materials import materials

def geometry(lumapi, model, period, diameter, modes = False):
    mat = materials(lumapi, model, modes)
    

    Air = mat["Air"]
    SiO2 = mat["SiO2"]
    Si3N4 = mat["Si3N4"]
    Si = mat["Si"]
    Al = mat["Al"]
    slab_height=50e-9
    waveguide_height = 0.25E-6
    waveguide_width = 0.45E-6
    waveguide_length = 2.51E-6
    hole_d = diameter*1e-9
    hole_spacing = period*1e-9
    diffusion_length = 2e-6
    diffusion_width = 1.2e-6
    diffusion_offset = 1e-6                #distance from center of the waveguide
    contact_width = 1e-6
    contact_length = diffusion_length
    contact_offset = diffusion_offset
    contact_height = 0.5e-6

    substrate ={   
                   "width"         : 5e-6,
                   "length"        : 15e-6,
                   "height"        : 2e-6,
                   "x"             : 0,
                   "y"             : 0,
                   "m"             : SiO2
                }
     
    slab ={   
                   "width"         : substrate["width"],
                   "length"        : substrate["length"],
                   "height"        : slab_height,
                   "x"             : 0,
                   "y"             : 0,
                   "m"             : Si
                }
     
    waveguide ={   
                   "width"         : waveguide_width,
                   "length"        : substrate["length"],
                   "height"        : waveguide_height,
                   "x"             : 0,
                   "y"             : 0,
                   "m"             : Si
                }
     
    P_diffusion={   
                   "width"         : diffusion_width,
                   "length"        : diffusion_length,
                   "height"        : slab_height,
                   "x"             : 0,
                   "y"             : diffusion_width/2+waveguide_width/2+diffusion_offset,
                   "z"             : slab_height/2 + substrate["height"],
                   "m"             : Si
                }
     
    N_diffusion={   
                   "width"         : diffusion_width,
                   "length"        : diffusion_length,
                   "height"        : slab_height,
                   "x"             : 0,
                   "y"             : -(diffusion_width/2+waveguide_width/2+diffusion_offset),
                   "z"             : slab_height/2 + substrate["height"],
                   "m"             : Si
                }
     
    Hole={   
                   "diameter"      : hole_d,
                   "length"        : diffusion_length,
                   "height"        : slab_height,
                   "x"             : waveguide_length/2+hole_d/2,
                   "y"             : 0,
                   "m"             : SiO2
                }
    P_contact ={   
                   "width"         : contact_width,
                   "length"        : contact_length,
                   "height"        : contact_height,
                   "x"             : 0,
                   "y"             : waveguide_width/2+contact_offset+contact_width/2,
                   "m"             : Al
                }
    
    N_contact ={   
                   "width"         : contact_width,
                   "length"        : contact_length,
                   "height"        : contact_height,
                   "x"             : 0,
                   "y"             : -waveguide_width/2-contact_offset-contact_width/2,
                   "m"             : Al
                }    
    
    current_height=0 
    
    model.addrect();
    model.set("name","Substrate")
    model.set("x", substrate["x"])
    model.set("x span", substrate["length"])
    model.set("y", substrate["y"])
    model.set("y span", substrate["width"])
    model.set("z min",current_height)
    model.set("z max", substrate["height"])
    model.set("material", substrate["m"])
    current_height+=substrate["height"]
    
    model.addrect();
    model.set("name","Slab")
    model.set("x", slab["x"])
    model.set("x span", slab["length"])
    model.set("y", slab["y"])
    model.set("y span", slab["width"])
    model.set("z min",current_height)
    model.set("z max", slab["height"]+current_height)
    model.set("material", slab["m"])
    current_height+=slab["height"]
    
    model.addrect();
    model.set("name","Waveguide")
    model.set("x", waveguide["x"])
    model.set("x span", waveguide["length"])
    model.set("y", waveguide["y"])
    model.set("y span", waveguide["width"])
    model.set("z min",current_height)
    model.set("z max", waveguide["height"]+current_height)
    model.set("material", waveguide["m"])
    
    model.addrect()
    model.set("name","pwell_contact")
    model.set("x",P_contact['x'])
    model.set("x span",P_contact['length'])
    model.set("y",P_contact['y'])
    model.set("y span",P_contact['width'])
    model.set("z min",current_height)
    model.set("z max",P_contact['height']+current_height)
    model.set("material", P_contact['m'])
 
    model.addrect()
    model.set("name","nwell_contact")
    model.set("x",N_contact['x'])
    model.set("x span",N_contact['length'])
    model.set("y",N_contact['y'])
    model.set("y span",N_contact['width'])
    model.set("z min",current_height)
    model.set("z max",N_contact['height']+current_height)
    model.set("material", N_contact['m'])
    
    for j in range(5):
        model.addcircle();
        model.set("name","Hole_r_"+str(j))
        model.set("x", Hole["x"]+hole_spacing*j)
        model.set("radius", Hole["diameter"]/2)
        model.set("y", Hole["y"])
        model.set("z min",waveguide["height"]+current_height-160e-9)
        model.set("z max", waveguide["height"]+current_height)
        model.set("material", Hole["m"])
        
    for i in range(5):
        model.addcircle();
        model.set("name","Hole_l_"+str(i))
        model.set("x", -Hole["x"]-hole_spacing*i)
        model.set("radius", Hole["diameter"]/2)
        model.set("y", Hole["y"])
        model.set("z min",waveguide["height"]+current_height-160e-9)
        model.set("z max", waveguide["height"]+current_height)
        model.set("material", Hole["m"])       
    
    
    
    simulation_box ={
                     'x': substrate["x"],               
                     'x_span': substrate["length"],               
                     'y': substrate["y"],              
                     'y_span': substrate["width"], 
                     'z': (current_height + 0)/2,              
                     'z_span': current_height + 2e-6, 
                     'z_min': 0,
                     'z_max': current_height + 2e-6,
                 
                    }
    
    model.select("Hole_l_"+str(i))
    c=model.get("x")-1e-6
    model.select("Hole_r_"+str(j))
    c1=model.get("x")+1e-6
    model.select("Waveguide")
    c2 =  model.get("z")
    source_monitor = {
                        "x_mode"        : c,
                        "y_mode"        : waveguide["y"],
                        "z_mode"        : c2,
                        "y_span_mode"   : waveguide["width"]+1e-6,
                        "z_span_mode"   : waveguide["height"]+1e-6,
                        
                        "x_monitor"     : c1,
                        "y_monitor"     : waveguide["y"],
                        "z_monitor"     : c2,
                        "y_span_monitor": waveguide["width"]+1e-6,
                        "z_span_monitor": waveguide["height"]+1e-6,
                        
                        "x_gmonitor"     : substrate["x"],
                        "y_gmonitor"     : substrate["y"],
                        "z_gmonitor"     : c2,
                        "x_span_gmonitor": substrate["length"],
                        "y_span_gmonitor": substrate["width"],
                        
                        "x_tmonitor"     : substrate["x"],
                        "y_tmonitor"     : substrate["y"],
                        "z_tmonitor"     : c2,

                        
                        
                        
            }
    
    return (source_monitor, simulation_box, P_diffusion, N_diffusion)