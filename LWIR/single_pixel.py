# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 16:16:35 2021

@author: m.ryabko
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 17:56:24 2021

@author: m.ryabko
"""

import addgeometry
import bridge 

def single_pixel(lumapi, model, parameters):
    x=parameters.x
    y=parameters.y
    z=parameters.z_max
    parameters.x_span = 2*parameters.pixel_separation
    parameters.y_span = 2*parameters.pixel_separation
#Horizontal waveguide    
    waveguide_h= addgeometry.Rectangle(model)
    
    waveguide_h.name="Horizontal waveguide"
    waveguide_h.override_mesh_order = 1
    waveguide_h.mesh_order = 2
    waveguide_h.material = parameters.Si
            
    waveguide_h.x = x + parameters.resonator_outer_radius+parameters.waveguide_width/2+parameters.gap1
    waveguide_h.x_span = parameters.waveguide_width
    waveguide_h.y = y
    waveguide_h.y_span = parameters.substrate_length
    waveguide_h.z_min=z
    waveguide_h.z_max=z+parameters.slab_height
    

    
#Vertical waveguide 
    waveguide_v= addgeometry.Rectangle(model)
    
    waveguide_v.name="Vertical waveguide"
    waveguide_v.override_mesh_order = 1
    waveguide_v.mesh_order = 2
    waveguide_v.material = parameters.Si
            
    waveguide_v.x = x
    waveguide_v.x_span = parameters.substrate_length
    waveguide_v.y = y + parameters.resonator_outer_radius+parameters.waveguide_width/2+parameters.gap2
    waveguide_v.y_span = parameters.waveguide_width
    waveguide_v.z_min=z
    waveguide_v.z_max=z+parameters.slab_height
 
#Resonator
    resonator= addgeometry.Ring(model)
    resonator.name="Resonator"
    resonator.override_mesh_order = 1
    resonator.mesh_order = 2
    resonator.material = parameters.Si
    
    resonator.make_ellipsoid = 0
    resonator.inner_radius1 = parameters.resonator_inner_radius
    resonator.outer_radius1 = parameters.resonator_outer_radius
    resonator.x=x
    resonator.y=y
    resonator.z_min=z
    resonator.z_max=z+parameters.slab_height
    
#Absorber
    absorber= addgeometry.Ring(model)
    absorber.name="Absorber"
    absorber.override_mesh_order = 1
    absorber.mesh_order = 2
    absorber.material = parameters.Si3N4
    
    absorber.make_ellipsoid = 0
    absorber.inner_radius1 = 0
    absorber.outer_radius1 = parameters.resonator_outer_radius
    absorber.x=x
    absorber.y=y
    absorber.z_min=resonator.z_max
    absorber.z_max=resonator.z_max+parameters.absorber_height

##BOX hole
#    BOXHole= addgeometry.Ring(model)
#    BOXHole.name="BOX hole"
#    BOXHole.override_mesh_order = 1
#    BOXHole.mesh_order = 3
#    BOXHole.material = parameters.Air
#    
#    BOXHole.make_ellipsoid = 0
#    BOXHole.inner_radius1 = 0
#    BOXHole.outer_radius1 = parameters.hole_radius
#    BOXHole.x=x
#    BOXHole.y=y
#    BOXHole.z_min=parameters.substrate_height
#    BOXHole.z_max=parameters.substrate_height+parameters.box_height  
#    
##BOX under resonator
#    BOXUnderResonator= addgeometry.Ring(model)
#    BOXUnderResonator.name="BOX under resonator"
#    BOXUnderResonator.override_mesh_order = 1
#    BOXUnderResonator.mesh_order = 2
#    BOXUnderResonator.material = parameters.SiO2
#    
#    BOXUnderResonator.make_ellipsoid = 0
#    BOXUnderResonator.inner_radius1 = 0
#    BOXUnderResonator.outer_radius1 = parameters.BOX_under_resonator_radius
#    BOXUnderResonator.x=x
#    BOXUnderResonator.y=y
#    BOXUnderResonator.z_min=parameters.substrate_height
#    BOXUnderResonator.z_max=parameters.substrate_height+parameters.box_height 
    
#BOX oxide    
    BOX= addgeometry.Rectangle(model)
    
    BOX.name="Box oxide"
    BOX.override_mesh_order = 1
    BOX.mesh_order = 4
    BOX.material=parameters.SiO2
            
    BOX.x=x
    BOX.x_span=2*parameters.pixel_separation
    BOX.y=y
    BOX.y_span=2*parameters.pixel_separation
    BOX.z_min=z-parameters.box_height
    BOX.z_max=z
    BOX.add() 

#BOX hole    
    BOX_hole= addgeometry.Rectangle(model)
    
    BOX_hole.name="Box hole"
    BOX_hole.override_mesh_order = 1
    BOX_hole.mesh_order = 3
    BOX_hole.material=parameters.Air
            
    BOX_hole.x=x
    BOX_hole.x_span=2*parameters.pixel_separation-1e-6
    BOX_hole.y=y
    BOX_hole.y_span=2*parameters.pixel_separation-1e-6
    BOX_hole.z_min=z-parameters.box_height
    BOX_hole.z_max=z
    BOX_hole.add() 
    
#Bridges    
    bridge.bridge_Si_single(lumapi, model, parameters)


    
    
    waveguide_h.add()
    waveguide_v.add()
#    bridge1.add()
#    bridge2.add()
    resonator.add()
#    BOXHole.add()
#    BOXUnderResonator.add()
    absorber.add()


#Si undercut   
    model.addsphere()
    model.set("name","Undercut")
    model.set("override mesh order from material database",1)
    model.set("mesh order",5)
    model.set("make ellipsoid",1)
    model.set("x", x)
    model.set("radius", parameters.undercut_radius1)
    model.set("radius 2", parameters.undercut_radius1)
    model.set("radius 3", parameters.undercut_radius2)
    model.set("y", y)   
    model.set("z",parameters.substrate_height)
    model.set("material", parameters.Air)  
    

        
#    simulation_box = addgeometry.SimulationBox()
#    simulation_box.x = substrate.x               
#    simulation_box.x_span = substrate.x_span            
#    simulation_box.y = substrate.y            
#    simulation_box.y_span = substrate.y_span
#    simulation_box.z_min = substrate.z_min
#    simulation_box.z_max = absorber.z_max

       
    
    return absorber
