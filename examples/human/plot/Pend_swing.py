'''
Author: your name
Date: 2021-11-03 11:41:25
LastEditTime: 2021-11-03 19:10:21
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /RA_interactive-pilco/examples/human/plot/Pend_swing.py
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

X = np.load('./examples/human/plot/Comb_swing_pend_X.npy')
Y = np.load('./examples/human/plot/Comb_swing_pend_Y.npy')
Yn = np.load('./examples/human/plot/Comb_swing_pend_Yn.npy')
X1 = np.load('./examples/human/plot/Comb_swing_pend_X1.npy')
Y1 = np.load('./examples/human/plot/Comb_swing_pend_Y1.npy')
Yn1 = np.load('./examples/human/plot/Comb_swing_pend_Yn1.npy')
X2 = np.load('./examples/human/plot/Comb_swing_pend_X2.npy')
Y2 = np.load('./examples/human/plot/Comb_swing_pend_Y2.npy')
Yn2 = np.load('./examples/human/plot/Comb_swing_pend_Yn2.npy')

X_a = np.mean( np.array([X, X1, X2]), axis=0 )
Y_a = np.mean( np.array([Y, Y1, Y2]), axis=0 )
Yn_a = np.mean( np.array([Yn, Yn1, Yn2]), axis=0 )

X_o = np.load('./examples/human/plot/swing_pend_X.npy')
Y_o = np.load('./examples/human/plot/swing_pend_Y.npy')
Yn_o = np.load('./examples/human/plot/swing_pend_Yn.npy')
X_o1 = np.load('./examples/human/plot/swing_pend_X.npy1.npy')
Y_o1 = np.load('./examples/human/plot/swing_pend_Y.npy1.npy')
Yn_o1 = np.load('./examples/human/plot/swing_pend_Yn.npy1.npy')
X_o2 = np.load('./examples/human/plot/swing_pend_X.npy2.npy')
Y_o2 = np.load('./examples/human/plot/swing_pend_Y.npy2.npy')
Yn_o2 = np.load('./examples/human/plot/swing_pend_Yn.npy2.npy')
X_o3 = np.load('./examples/human/plot/swing_pend_X.npy3.npy')
Y_o3 = np.load('./examples/human/plot/swing_pend_Y.npy3.npy')
Yn_o3 = np.load('./examples/human/plot/swing_pend_Yn.npy3.npy')
X_o4 = np.load('./examples/human/plot/swing_pend_X.npy4.npy')
Y_o4 = np.load('./examples/human/plot/swing_pend_Y.npy4.npy')
Yn_o4 = np.load('./examples/human/plot/swing_pend_Yn.npy4.npy')

X_oa = np.mean( np.array([X_o, X_o1, X_o2, X_o3, X_o4]), axis=0 )
Y_oa = np.mean( np.array([Y_o, Y_o1, Y_o2, Y_o3, Y_o4]), axis=0 )
Yn_oa = np.mean( np.array([Yn_o, Yn_o1, Yn_o2, Yn_o3, Yn_o4]), axis=0 )

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
