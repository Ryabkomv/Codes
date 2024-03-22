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


from single_pixel import single_pixel

from substrate import substrate

def double_pixel(lumapi, model, parameters):
    
    
    substrate(lumapi, model, parameters)
    
    single_pixel(lumapi, model, parameters)
    
    parameters.x = 2*parameters.pixel_separation
    
    single_pixel(lumapi, model, parameters)
    
    parameters.x_span = 4*parameters.pixel_separation
    parameters.y_span = 2*parameters.pixel_separation