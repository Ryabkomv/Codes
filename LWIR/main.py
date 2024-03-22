import imp
import numpy as np
import matplotlib.pyplot as plt
import absorptionFDTD
import temperatureDevice




print(__name__)


lumapi = imp.load_source("lumapi","C:\\Program Files\\Lumerical\\v212\\api\\python\\lumapi.py") 
#model = lumapi.FDTD()
#model.addfdtd()
#model.set("x span", 15e-6)
#model.set("y span", 15e-6)
#model.set("z span", 11e-6)
#model.addindex()
#model.set("x span", 15e-6)
#model.set("y span", 15e-6)
#model.set("z min", 0)
#model.set("z max", 5.05e-6)
#model = lumapi.DEVICE()
# 
#model.addheatsolver()
#model.select("simulation region")
#model.set("dimension", "3D")
#model.set("x span", 15e-6)
#model.set("y span", 15e-6)
#model.set("z span", 11e-6)

single_pixel=0

#absorptionFDTD.absorptionFDTD(lumapi)

temperatureDevice.temperatureDevice(lumapi,single_pixel)


#model.run()