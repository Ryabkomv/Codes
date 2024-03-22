# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 14:48:04 2021

@author: m.ryabko
"""
import addgeometry

def substrate(lumapi, model, parameters):
    
#Substarte    
    substrate = addgeometry.Rectangle(model)
    
    substrate.name="Substrate"
    substrate.override_mesh_order = 1
    substrate.mesh_order = 6
    substrate.material=parameters.Si
            
    substrate.x=parameters.pixel_separation
    substrate.x_span=2*parameters.pixel_separation*2
    substrate.y=parameters.y
    substrate.y_span=parameters.pixel_separation*2
    substrate.z_min=parameters.z
    substrate.z_max=parameters.substrate_height
    substrate.add()



#Air    
    air = addgeometry.Rectangle(model)
    
    air.name="Air"
    air.override_mesh_order = 1
    air.mesh_order = 3
    air.material=parameters.Air
            
    air.x=substrate.x
    air.x_span=substrate.x_span
    air.y=substrate.y
    air.y_span=substrate.y_span
    air.z_min=substrate.z_max+parameters.box_height
    air.z_max=substrate.z_max+parameters.box_height+parameters.air_height
    air.add()
    parameters.z_max = substrate.z_max+parameters.box_height