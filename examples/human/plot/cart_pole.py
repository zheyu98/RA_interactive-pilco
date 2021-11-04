'''
Author: your name
Date: 2021-11-03 22:22:27
LastEditTime: 2021-11-04 22:27:35
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /RA_interactive-pilco/examples/human/plot/cart_pole.py
'''


import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

X1 = np.load('./examples/human/plot/Comb_cart_pole_X1.npy')
Y1 = np.load('./examples/human/plot/Comb_cart_pole_Y1.npy')
Yn1 = np.load('./examples/human/plot/Comb_cart_pole_Yn1.npy')
X2 = np.load('./examples/human/plot/Comb_cart_pole_X2.npy')
Y2 = np.load('./examples/human/plot/Comb_cart_pole_Y2.npy')
Yn2 = np.load('./examples/human/plot/Comb_cart_pole_Yn2.npy')
X3 = np.load('./examples/human/plot/Comb_cart_pole_X3.npy')
Y3 = np.load('./examples/human/plot/Comb_cart_pole_Y3.npy')
Yn3 = np.load('./examples/human/plot/Comb_cart_pole_Yn3.npy')

X_a = np.mean( np.array([X2, X3]), axis=0 )
Y_a = np.mean( np.array([Y2, Y3]), axis=0 )
Yn_a = np.mean( np.array([Yn2, Yn3]), axis=0 )

# X_a = X3
# Y_a = Y3
# Yn_a = Yn3

X_o = np.load('./examples/human/plot/cart_pole_X.npy')
Y_o = np.load('./examples/human/plot/cart_pole_Y.npy')
Yn_o = np.load('./examples/human/plot/cart_pole_Yn.npy')


X_oa = X_o
Y_oa = Y_o
Yn_oa = Yn_o

# 300 represents number of points to make between T.min and T.max
xnew = np.linspace(X_a.min(), X_a.max(), 300) 
spl = make_interp_spline(X_a, Y_a.flatten())  
spl2 = make_interp_spline(X_a, Yn_a.flatten())  
Y_smooth = spl(xnew)
Yn_smooth = spl2(xnew)

xonew = np.linspace(X_oa.min(), X_oa.max(), 300) 
spl3 = make_interp_spline(X_oa, Y_oa.flatten())  # type: BSpline
spl4 = make_interp_spline(X_oa, Yn_oa.flatten())  # type: BSpline
Yo_smooth = spl3(xonew)
Yno_smooth = spl4(xonew)

plt.plot(xnew, Y_smooth, 'r', label='Real reward with human')
plt.plot(xnew, Yn_smooth, 'r--', label='Predictive reward with human')
plt.plot(xonew, Yo_smooth, 'b', label='Real reward without human')
plt.plot(xonew, Yno_smooth, 'b--', label='Predictive reward without human')
plt.xlabel('Iterations')
plt.ylabel('Rewards')
plt.legend(loc=0)
plt.show()

# plt.plot(X, Y)
# plt.plot(X, Yn.flatten())
# plt.plot(X_o, Y_o)
# plt.plot(X_o, Yn_o.flatten())
# plt.xlabel('Iterations')
# plt.ylabel('Rewards')
# plt.show()

