# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 12:38:24 2021

@author: m.ryabko
"""


"""

"""
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 14:48:04 2021

@author: m.ryabko
"""
import addgeometry

def bridge_Si_cross(lumapi, model, parameters):
    x=parameters.x
    y=parameters.y
    z=parameters.z_max
#Bridge1    
    bridge1= addgeometry.Rectangle(model)
    
    bridge1.name="bridge1"
    bridge1.override_mesh_order = 1
    bridge1.mesh_order = 2
    bridge1.material = parameters.Si
            
    bridge1.x = x
    bridge1.x_span = parameters.bridge_width
    bridge1.y = y
    bridge1.y_span = parameters.substrate_length*1.4
    bridge1.z_min=z #parameters.substrate_height
    bridge1.z_max=z+parameters.bridge_height_Si #parameters.substrate_height+parameters.box_height 
    bridge1.axis1 = "z"
    bridge1.rotation_angle1 = 55
    
#Bridge2
    bridge2= addgeometry.Rectangle(model)
    
    bridge2.name="bridge2"
    bridge2.override_mesh_order = 1
    bridge2.mesh_order = 2
    bridge2.material = parameters.Si
            
    bridge2.x = x
    bridge2.x_span = parameters.substrate_length*1.4
    bridge2.y = y
    bridge2.y_span = parameters.bridge_width
    bridge2.z_min=z#parameters.substrate_height
    bridge2.z_max=z+parameters.bridge_height_Si#parameters.substrate_height+parameters.box_height 
    bridge2.axis1 = "z"
    bridge2.rotation_angle1 = 35
    
    
    bridge1.add()
    bridge2.add()
    
def bridge_SiO2_cross(lumapi, model, parameters):
    x=parameters.x
    y=parameters.y
    z=parameters.z_max
#Bridge1    
    bridge1= addgeometry.Rectangle(model)
    
    bridge1.name="bridge1"
    bridge1.override_mesh_order = 1
    bridge1.mesh_order = 2
    bridge1.material = parameters.SiO2
            
    bridge1.x = x
    bridge1.x_span = parameters.bridge_width
    bridge1.y = y
    bridge1.y_span = parameters.substrate_length*1.4
    bridge1.z_min=parameters.substrate_height
    bridge1.z_max=parameters.substrate_height+parameters.box_height 
    bridge1.axis1 = "z"
    bridge1.rotation_angle1 = 45
    
#Bridge2
    bridge2= addgeometry.Rectangle(model)
    
    bridge2.name="bridge2"
    bridge2.override_mesh_order = 1
    bridge2.mesh_order = 2
    bridge2.material = parameters.SiO2
            
    bridge2.x = x
    bridge2.x_span = parameters.substrate_length*1.4
    bridge2.y = y
    bridge2.y_span = parameters.bridge_width
    bridge2.z_min=parameters.substrate_height
    bridge2.z_max=parameters.substrate_height+parameters.box_height 
    bridge2.axis1 = "z"
    bridge2.rotation_angle1 = 45
    
    
    bridge1.add()
    bridge2.add()
    
def bridge_Si_single(lumapi, model, parameters):
    x=parameters.x
    y=parameters.y
    z=parameters.z_max

    
#Bridge2
    bridge2= addgeometry.Rectangle(model)
    
    bridge2.name="bridge2"
    bridge2.override_mesh_order = 1
    bridge2.mesh_order = 2
    bridge2.material = parameters.Si
            
    bridge2.x = x-parameters.substrate_length/4
    bridge2.x_span = parameters.substrate_length*1.4/2
    bridge2.y = y-parameters.substrate_width/4
    bridge2.y_span = parameters.bridge_width
    bridge2.z_min=z#parameters.substrate_height
    bridge2.z_max=z+parameters.bridge_height_Si#parameters.substrate_height+parameters.box_height 
    bridge2.axis1 = "z"
    bridge2.rotation_angle1 = 45
    
    

    bridge2.add()

    
def bridge_Si_triple(lumapi, model, parameters):
    x=parameters.x
    y=parameters.y
    z=parameters.z_max
#Bridge1    
    bridge1= addgeometry.Rectangle(model)
    
    bridge1.name="bridge1"
    bridge1.override_mesh_order = 1
    bridge1.mesh_order = 2
    bridge1.material = parameters.Si
            
    bridge1.x = x  - parameters.resonator_outer_radius/2
    bridge1.x_span = parameters.bridge_width
    bridge1.y = y + parameters.resonator_outer_radius - 0.5e-6
    bridge1.y_span = parameters.substrate_length/2
    bridge1.z_min=z #parameters.substrate_height
    bridge1.z_max=z+parameters.bridge_height_Si #parameters.substrate_height+parameters.box_height 
    bridge1.axis1 = "z"
    bridge1.rotation_angle1 = 90
    
#Bridge3    
    bridge3= addgeometry.Rectangle(model)
    
    bridge3.name="bridge3"
    bridge3.override_mesh_order = 1
    bridge3.mesh_order = 2
    bridge3.material = parameters.Si
            
    bridge3.x = x + parameters.resonator_outer_radius - 0.5e-6
    bridge3.x_span = parameters.substrate_length/2
    bridge3.y = y - parameters.resonator_outer_radius/2
    bridge3.y_span = parameters.bridge_width
    bridge3.z_min=z #parameters.substrate_height
    bridge3.z_max=z+parameters.bridge_height_Si #parameters.substrate_height+parameters.box_height 
    bridge3.axis1 = "z"
    bridge3.rotation_angle1 = 90
    
#Bridge2
    bridge2= addgeometry.Rectangle(model)
    
    bridge2.name="bridge2"
    bridge2.override_mesh_order = 1
    bridge2.mesh_order = 2
    bridge2.material = parameters.Si
            
    bridge2.x = x-parameters.substrate_length/4
    bridge2.x_span = parameters.substrate_length*1.4/2
    bridge2.y = y-parameters.substrate_width/4
    bridge2.y_span = parameters.bridge_width
    bridge2.z_min=z#parameters.substrate_height
    bridge2.z_max=z+parameters.bridge_height_Si#parameters.substrate_height+parameters.box_height 
    bridge2.axis1 = "z"
    bridge2.rotation_angle1 = 45
    
    
    bridge1.add()
    bridge2.add()
    bridge3.add()