# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 15:10:12 2021

@author: m.ryabko
"""
from geom import geometry

def FDTD(lumapi,period, diameter,b):
    model = lumapi.FDTD()
    
    s_m, box, P_diffusion, N_diffusion = geometry(lumapi, model, period, diameter, True)
    
    wl_start=1.4e-6
    wl_stop=2.e-6
    N_freq=1000
    
    model.addfdtd()
    model.set("dimension", "3D")
    model.set("simulation time", 5000e-15)
    model.set("x", box["x"])
    model.set("x span", box['x_span']-5e-6)
    model.set("y", box["y"])
    model.set("y span", box['y_span']-3e-6)
    model.set("z min", box["z_min"] + 1e-6)
    model.set("z max", box['z_max'] + 1E-6)
    model.set("background material","<Object defined dielectric>");
    model.set("index", 1.4);
    model.set("mesh accuracy", 1);
    model.set("x min bc", "PML")
    model.set("y min bc", "PML")
    model.set("x max bc", "PML")
    model.set("y max bc", "PML")
    model.set("z min bc", "PML")
    model.set("z max bc", "PML")
    
    model.addmode()
    model.set("name", "mode_source")
    model.set("injection axis", "x-axis")
    model.set("Direction", "Forward")
    model.set("x", s_m['x_mode'])
    model.set("y", s_m['y_mode'])
    model.set("z", s_m['z_mode'])
    model.set("y span", s_m['y_span_mode'])
    model.set("z span", s_m['z_span_mode'])
    model.set("wavelength start", wl_start)
    model.set("wavelength stop", wl_stop)
    model.set("optimize for short pulse", 0)
    
    model.addpower();
    model.set("name", "mode_monitor")
    model.set("monitor type","2D X-normal")
    model.set("y span", s_m['y_span_monitor'])
    model.set("z span", s_m['z_span_monitor'])
    model.set("x", s_m['x_monitor'])
    model.set("y", s_m['y_monitor'])
    model.set("z", s_m['z_monitor'])
    model.setglobalmonitor("frequency points",N_freq)
    
    model.addpower();
    model.set("name", "power_monitor")
    model.set("monitor type","2D Z-normal")
    model.set("x span", s_m['x_span_gmonitor'])
    model.set("y span", s_m['y_span_gmonitor'])
    model.set("x", s_m['x_gmonitor'])
    model.set("y", s_m['y_gmonitor'])
    model.set("z", s_m['z_gmonitor'])
    model.setglobalmonitor("frequency points",N_freq)
    
    model.addtime();
    model.set("name", "time_monitor")

    model.set("x", s_m['x_tmonitor'])
    model.set("y", s_m['y_tmonitor'])
    model.set("z", s_m['z_tmonitor'])

    model.matlabload("charge")
    model.addgridattribute("np Density", model.getv("charge"))
    model.set("name", "charge_density")
    model.set("V_P_contact_index", b)
#    model.set("z", 2.15e-6)
    
    model.save("FDTD.fsp")
    model.run()
    
    T = model.getresult("mode_monitor", "T")
    f = model.getresult("mode_monitor", "f")
    
    return (f,T)
    
