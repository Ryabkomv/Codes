# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 14:59:42 2021

@author: m.ryabko
"""
from materials import materials

class SimulationBox:
        def __init__(self):
           
            self.x=0
            self.x_span=1e-6
            self.y=0
            self.y_span=1e-6
            self.z_min=0
            self.z_max=1e-6
            
class Parameters:
    def __init__(self, lumapi, model):
        self.x=0
        self.y=0
        self.z=0
        self.hole_in_resonator_radius = 0
        self.x_min = 0
        self.x_max = 0 
        self.y_min = 0
        self.y_max = 0
        self.z_min = 0
        self.z_max = 0
        self.x_span = 0
        self.y_span = 0
        self.z_span = 0
    #materials
        mat = materials(lumapi, model)
        self.Air = mat["Air"]
        self.SiO2 = mat["SiO2"]
        self.Si3N4 = mat["Si3N4"]
        self.Si = mat["Si"]
        self.Al = mat["Al"]
        
    #substrate
        self.substrate_width = 15e-6
        self.substrate_length = 15e-6
        self.substrate_height = 3e-6 
        
    #BOX
        self.box_height = 1e-6
        self.BOX_under_resonator_radius = 1.0e-6
        self.hole_radius = 7e-6
        
    #resonator
        self.resonator_inner_radius = self.hole_in_resonator_radius
        self.resonator_outer_radius = 4e-6
        
    #waveguide_width    
        self.gap1=200e-9
        self.gap2 = 200e-9
        self.waveguide_width = 0.45E-6
        
    #bridge    
        self.bridge_width = 100e-9
        self.bridge_height_Si = 90e-9
        
    #absorber
        self.absorber_height = 1.0e-6
        self.absorber_inner_radius = self.hole_in_resonator_radius

        
    #slab    
        self.slab_height = 220e-9 
        
    #undercut    
        self.undercut_radius1 = 7.4e-6
        self.undercut_radius2 = 1e-6
    #model specific            
        self.space_above_model = 2e-6
        self.pixel_separation=6e-6
    #air
        self.air_height = self.space_above_model+self.slab_height+self.absorber_height
    #FDTD
        self.FDTD_x = self.x
        self.FDTD_y = self.y
        
        self.FDTD_x_span = self.pixel_separation*2
        self.FDTD_y_span = self.pixel_separation*2
        self.FDTD_z_span = self.substrate_height + self.box_height + self.slab_height +self.absorber_height+self.space_above_model
        self.FDTD_z = self.z+self.FDTD_z_span/2
        
        self.FDTD_mesh_accuracy = 2
        
        self.midIR_wl_start = 8E-6
        self.midIR_wl_stop = 14E-6
        self.midIR_Nfreq = 100
        self.IR_power = 10E-5
        
        self.z_span = self.substrate_height + self.box_height + self.slab_height +self.absorber_height+self.space_above_model
        
        self.x_min = -self.pixel_separation
        self.y_min = -self.pixel_separation
        
    #Thermal
        self.min_edge_length = 0.01e-6
        self.max_edge_length = 1e-6
        
