'''
Author: your name
Date: 2021-10-24 12:21:34
LastEditTime: 2021-10-25 15:04:05
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /RA_interactive-pilco/examples/human/test.py
'''
import numpy as np

Xc = np.load('./examples/human/training_data_Xc.npy')
Yc = np.load('./examples/human/training_data_Yc.npy')
X = np.load('./examples/human/training_data_X.npy')
Y = np.load('./examples/human/training_data_Y.npy')

# print(Xc); 
# print(Yc); 
# print(X); 
print(Y)