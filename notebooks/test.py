# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 13:53:06 2017

@author: ryabko
"""

import numpy as np
import time
a = np.random.rand(1000000)
b = np.random.rand(1000000)
tic = time.time()
c = np.dot(a,b)
toc=time.time()
print(str(1000*(toc-tic)))

tic = time.time()
for i in range(1000000):
    c+= a[i]*b[i]
toc=time.time()
print(str(1000*(toc-tic)))

a = np.random.rand(3,3)
b = np.random.rand(3,1)
c = a*b


for l in (range(1,4)):
    print(l)