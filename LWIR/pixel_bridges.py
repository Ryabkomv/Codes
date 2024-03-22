# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 17:56:24 2021

@author: m.ryabko
"""

import addgeometry

def pixel_bridges(lumapi, model, mat, x=0,y=0,z=0):
    

    Air = mat["Air"]
    SiO2 = mat["SiO2"]
    Si3N4 = mat["Si3N4"]
    Si = mat["Si"]
    Al = mat["Al"]
    
    waveguide_width = 0.45E-6
    resonator_inner_radius = 3.6e-6
    resonator_outer_radius = 4e-6
    BOX_under_resonator_radius = 1.0e-6
    gap1=200e-9
    gap2 = 200e-9
    hole_radius = 7.4e-6
    bridge_width = 100e-9
    
    substrate_width = 15e-6
    substrate_length = 15e-6
    
    substrate_height = 3e-6   
    box_height = 2e-6
    slab_height = 220e-9    
    
    absorber_width = 1.0e-6
    
    space_above_model = 2e-6
#Substarte    
    substrate = addgeometry.Rectangle(model)
    
    substrate.name="Substrate"
    substrate.override_mesh_order = 1
    substrate.mesh_order = 6
    substrate.material=Si
            
    substrate.x=x
    substrate.x_span=substrate_width
    substrate.y=y
    substrate.y_span=substrate_length
    substrate.z_min=z
    substrate.z_max=substrate_height


#BOX oxide    
    BOX= addgeometry.Rectangle(model)
    
    BOX.name="Box oxide"
    BOX.override_mesh_order = 1
    BOX.mesh_order = 4
    BOX.material=SiO2
            
    BOX.x=x
    BOX.x_span=substrate_width
    BOX.y=y
    BOX.y_span=substrate_length
    BOX.z_min=substrate.z_max
    BOX.z_max=substrate.z_max+box_height

#Air    
    air = addgeometry.Rectangle(model)
    
    air.name="Air"
    air.override_mesh_order = 1
    air.mesh_order = 3
    air.material=Air
            
    air.x=x
    air.x_span=substrate_width
    air.y=y
    air.y_span=substrate_length
    air.z_min=BOX.z_max
    air.z_max=BOX.z_max+space_above_model+slab_height+absorber_width
    
#Horizontal waveguide    
    waveguide_h= addgeometry.Rectangle(model)
    
    waveguide_h.name="Horizontal waveguide"
    waveguide_h.override_mesh_order = 1
    waveguide_h.mesh_order = 2
    waveguide_h.material = Si
            
    waveguide_h.x = x + resonator_outer_radius+waveguide_width/2+gap1
    waveguide_h.x_span = waveguide_width
    waveguide_h.y = y
    waveguide_h.y_span = substrate_length
    waveguide_h.z_min=BOX.z_max
    waveguide_h.z_max=BOX.z_max+slab_height
    

    
#Vertical waveguide 
    waveguide_v= addgeometry.Rectangle(model)
    
    waveguide_v.name="Vertical waveguide"
    waveguide_v.override_mesh_order = 1
    waveguide_v.mesh_order = 2
    waveguide_v.material = Si
            
    waveguide_v.x = x
    waveguide_v.x_span = substrate_length
    waveguide_v.y = y + resonator_outer_radius+waveguide_width/2+gap2
    waveguide_v.y_span = waveguide_width
    waveguide_v.z_min=BOX.z_max
    waveguide_v.z_max=BOX.z_max+slab_height
 
#Resonator
    resonator= addgeometry.Ring(model)
    resonator.name="Resonator"
    resonator.override_mesh_order = 1
    resonator.mesh_order = 2
    resonator.material = Si
    
    resonator.make_ellipsoid = 0
    resonator.inner_radius1 = 0
    resonator.outer_radius1 = resonator_outer_radius
    resonator.x=x
    resonator.y=y
    resonator.z_min=BOX.z_max
    resonator.z_max=BOX.z_max+slab_height
    
#Absorber
    absorber= addgeometry.Ring(model)
    absorber.name="Absorber"
    absorber.override_mesh_order = 1
    absorber.mesh_order = 2
    absorber.material = Si3N4
    
    absorber.make_ellipsoid = 0
    absorber.inner_radius1 = 0
    absorber.outer_radius1 = resonator_outer_radius
    absorber.x=x
    absorber.y=y
    absorber.z_min=resonator.z_max
    absorber.z_max=resonator.z_max+absorber_width

#BOX hole
    BOXHole= addgeometry.Ring(model)
    BOXHole.name="BOX hole"
    BOXHole.override_mesh_order = 1
    BOXHole.mesh_order = 3
    BOXHole.material = Air
    
    BOXHole.make_ellipsoid = 0
    BOXHole.inner_radius1 = 0
    BOXHole.outer_radius1 = hole_radius
    BOXHole.x=x
    BOXHole.y=y
    BOXHole.z_min=BOX.z_min
    BOXHole.z_max=BOX.z_max 
    
#BOX under resonator
    BOXUnderResonator= addgeometry.Ring(model)
    BOXUnderResonator.name="BOX under resonator"
    BOXUnderResonator.override_mesh_order = 1
    BOXUnderResonator.mesh_order = 2
    BOXUnderResonator.material = SiO2
    
    BOXUnderResonator.make_ellipsoid = 0
    BOXUnderResonator.inner_radius1 = 0
    BOXUnderResonator.outer_radius1 = BOX_under_resonator_radius
    BOXUnderResonator.x=x
    BOXUnderResonator.y=y
    BOXUnderResonator.z_min=BOX.z_min
    BOXUnderResonator.z_max=BOX.z_max 

#Bridge1    
    bridge1= addgeometry.Rectangle(model)
    
    bridge1.name="bridge1"
    bridge1.override_mesh_order = 1
    bridge1.mesh_order = 2
    bridge1.material = SiO2
            
    bridge1.x = x
    bridge1.x_span = bridge_width
    bridge1.y = y
    bridge1.y_span = substrate_length*1.4
    bridge1.z_min=BOX.z_min
    bridge1.z_max=BOX.z_max
    bridge1.axis1 = "z"
    bridge1.rotation_angle1 = 45
    
#Bridge2
    bridge2= addgeometry.Rectangle(model)
    
    bridge2.name="bridge2"
    bridge2.override_mesh_order = 1
    bridge2.mesh_order = 2
    bridge2.material = SiO2
            
    bridge2.x = x
    bridge2.x_span = substrate_length*1.4
    bridge2.y = y
    bridge2.y_span = bridge_width
    bridge2.z_min=BOX.z_min
    bridge2.z_max=BOX.z_max
    bridge2.axis1 = "z"
    bridge2.rotation_angle1 = 45
    
    

    substrate.add()
    air.add()
    BOX.add()
    waveguide_h.add()
    waveguide_v.add()
    bridge1.add()
    bridge2.add()
    resonator.add()
    BOXHole.add()
    BOXUnderResonator.add()
    absorber.add()


#Si undercut   
    model.addsphere()
    model.set("name","Undercut")
    model.set("override mesh order from material database",1)
    model.set("mesh order",5)
    model.set("make ellipsoid",1)
    model.set("x", substrate.x)
    model.set("radius", hole_radius)
    model.set("radius 2", hole_radius)
    model.set("radius 3", 2e-6)
    model.set("y", substrate.y)   
    model.set("z",substrate.z_max)
    model.set("material", Air)  
    

        
    simulation_box = addgeometry.SimulationBox()
    simulation_box.x = substrate.x               
    simulation_box.x_span = substrate.x_span            
    simulation_box.y = substrate.y            
    simulation_box.y_span = substrate.y_span
    simulation_box.z_min = substrate.z_min
    simulation_box.z_max = absorber.z_max

       
    
    return simulation_box, absorber
