# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 17:32:30 2021

@author: m.ryabko
"""
class Ring:
        def __init__(self, model):
            self.name="Ring"
            self.override_mesh_order = 1
            self.mesh_order = 2
            self.material="Si (Silicon) - Palik"
            
            self.make_ellipsoid = 0
            self.inner_radius1 = 0
            self.inner_radius2 = 0
            self.outer_radius1 = 1e-6
            self.outer_radius2 = 1e-6
            self.x=0
            self.y=0
            self.z_min=0
            self.z_max=1e-6
            
            self.theta_start=0
            self.theta_finish=360
            
            self.axis1 = "none"
            self.axis2 = "none"
            self.axis3 = "none"
            self.rotation_angle1 = 0
            self.rotation_angle2 = 0
            self.rotation_angle3 = 0
            
            self.model = model
            
        def add(self):
            model = self.model
            model.addring()
            model.set("name",self.name)
        #material
            model.set("override mesh order from material database",self.override_mesh_order)
            model.set("mesh order", self.mesh_order)
            model.set("material", self.material)
        #geometry
            model.set("make ellipsoid",self.make_ellipsoid)
            
            model.set("x", self.x)
            model.set("y", self.y)
            model.set("z min",self.z_min)
            model.set("z max", self.z_max)
        
            model.set("outer radius", self.outer_radius1)
            model.set("inner radius", self.inner_radius1)
            
            if (self.make_ellipsoid):
                model.set("outer radius 2", self.outer_radius2)
                model.set("inner radius 2", self.inner_radius2)    
        #rotations    
            if (self.axis1 != "none"):    
                model.set("first axis", self.axis1)
                model.set("rotation 1", self.rotation_angle1)
            if (self.axis2 != "none"): 
                model.set("second axis", self.axis2)
                model.set("rotation 1", self.rotation_angle2)
            if (self.axis3 != "none"): 
                model.set("third axis", self.axis3)
                model.set("rotation 1", self.rotation_angle3)
            
class Rectangle:
        def __init__(self, model):
            self.name="Rectangle"
            self.override_mesh_order = 1
            self.mesh_order = 2
            self.material="Si (Silicon) - Palik"
            
            self.x=0
            self.x_span=1e-6
            self.y=0
            self.y_span=1e-6
            self.z_min=0
            self.z_max=1e-6

            self.axis1 = "none"
            self.axis2 = "none"
            self.axis3 = "none"
            self.rotation_angle1 = 0
            self.rotation_angle2 = 0
            self.rotation_angle3 = 0
            
            self.model = model    
    
    
        def add(self):
            model = self.model
            model.addrect()
            model.set("name",self.name)
        #material
            model.set("override mesh order from material database",self.override_mesh_order)
            model.set("mesh order", self.mesh_order)
            model.set("material", self.material)
        #geometry
            model.set("x", self.x)
            model.set("x span", self.x_span)
            model.set("y", self.y)
            model.set("y span", self.y_span)
            model.set("z min",self.z_min)
            model.set("z max", self.z_max)
        #rotations
            if (self.axis1 != "none"):    
                model.set("first axis", self.axis1)
                model.set("rotation 1", self.rotation_angle1)
            if (self.axis2 != "none"): 
                model.set("second axis", self.axis2)
                model.set("rotation 1", self.rotation_angle2)
            if (self.axis3 != "none"): 
                model.set("third axis", self.axis3)
                model.set("rotation 1", self.rotation_angle3)


