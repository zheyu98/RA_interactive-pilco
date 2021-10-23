import numpy as np

a = np.arange(24).reshape(2,3,4) 
b = np.arange(8).reshape(2,4,1) 
print(np.matmul(a,b).shape)