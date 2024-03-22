import gzip
import sys
import pickle
import numpy as np
from matplotlib import pylab as plt
#f = gzip.open('mnist.pkl.gz', 'rb')
#if sys.version_info < (3,):
#    data = pickle.load(f)
#else:
#    data = pickle.load(f, encoding='bytes')
#f.close()
#(x_train, y_train), (x_test, y_test) = data

# the data, split between train and test sets
#(x_train, y_train), (x_test, y_test) = np.load('mnist.npz')



A = np.fromfile('Medicals\Diabetes\Bearil_00.raw', dtype='int16', sep="")
A = A.reshape([1960, 2608])
plt.imshow(A)
#B = np.array(A)
#th=100
#super_threshold_indices = A < 400
#A[super_threshold_indices]= 0
#super_threshold_indices = A >= 400
#A[super_threshold_indices]=1
#plt.imshow(A)
##C = B[B>400]=1
#plt.imshow(B)