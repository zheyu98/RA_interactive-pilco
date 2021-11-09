'''
Author: your name
Date: 2021-11-03 11:41:25
LastEditTime: 2021-11-09 12:23:19
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /RA_interactive-pilco/examples/human/plot/Pend_swing.py
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

X = np.load('./examples/human/plot/Comb_cart_swing_X.npy')
Y = np.load('./examples/human/plot/Comb_cart_swing_Y.npy')
Yn = np.load('./examples/human/plot/Comb_cart_swing_Yn.npy')
X1 = np.load('./examples/human/plot/Comb_cart_swing_X1.npy')
Y1 = np.load('./examples/human/plot/Comb_cart_swing_Y1.npy')
Yn1 = np.load('./examples/human/plot/Comb_cart_swing_Yn1.npy')
X2 = np.load('./examples/human/plot/Comb_cart_swing_X2.npy')
Y2 = np.load('./examples/human/plot/Comb_cart_swing_Y2.npy')
Yn2 = np.load('./examples/human/plot/Comb_cart_swing_Yn2.npy')
# X3 = np.load('./examples/human/plot/Comb_swing_pend_X3.npy')
# Y3 = np.load('./examples/human/plot/Comb_swing_pend_Y3.npy')
# Yn3 = np.load('./examples/human/plot/Comb_swing_pend_Yn3.npy')
# X4 = np.load('./examples/human/plot/Comb_swing_pend_X4.npy')
# Y4 = np.load('./examples/human/plot/Comb_swing_pend_Y4.npy')
# Yn4 = np.load('./examples/human/plot/Comb_swing_pend_Yn4.npy')

X_a = np.mean( np.array([X, X1, X2]), axis=0 )
Y_a = np.mean( np.array([Y, Y1, Y2]), axis=0 )
Yn_a = np.mean( np.array([Yn, Yn1, Yn2]), axis=0 )

Y_max = np.maximum.reduce([Y, Y1, Y2])
Yn_max = np.maximum.reduce([Yn, Yn1, Yn2])

Y_min = np.minimum.reduce([Y, Y1, Y2])
Yn_min = np.minimum.reduce([Yn, Yn1, Yn2])

# Y_v = np.var([Y, Y1, Y2],axis=0).flatten()

X_o = np.load('./examples/human/plot/cart_swing_X.npy')
Y_o = np.load('./examples/human/plot/cart_swing_Y.npy')
Yn_o = np.load('./examples/human/plot/cart_swing_Yn.npy')
X_o1 = np.load('./examples/human/plot/cart_swing_X1.npy')
Y_o1 = np.load('./examples/human/plot/cart_swing_Y1.npy')
Yn_o1 = np.load('./examples/human/plot/cart_swing_Yn1.npy')
X_o2 = np.load('./examples/human/plot/cart_swing_X3.npy')
Y_o2 = np.load('./examples/human/plot/cart_swing_Y3.npy')
Yn_o2 = np.load('./examples/human/plot/cart_swing_Yn3.npy')
# X_o3 = np.load('./examples/human/plot/swing_pend_X3.npy')
# Y_o3 = np.load('./examples/human/plot/swing_pend_Y3.npy')
# Yn_o3 = np.load('./examples/human/plot/swing_pend_Yn3.npy')
# X_o4 = np.load('./examples/human/plot/swing_pend_X4.npy')
# Y_o4 = np.load('./examples/human/plot/swing_pend_Y4.npy')
# Yn_o4 = np.load('./examples/human/plot/swing_pend_Yn4.npy')

X_oa = np.mean( np.array([X_o, X_o1, X_o2]), axis=0 )
Y_oa = np.mean( np.array([Y_o, Y_o1, Y_o2]), axis=0 )
Yn_oa = np.mean( np.array([Yn_o, Yn_o1, Yn_o2]), axis=0 )

Y_omax = np.maximum.reduce([Y_o, Y_o1, Y_o2])
Yn_omax = np.maximum.reduce([Yn_o, Yn_o1, Yn_o2])

Y_omin = np.minimum.reduce([Y_o, Y_o1, Y_o2])
Yn_omin = np.minimum.reduce([Yn_o, Yn_o1, Yn_o2])

# # 300 represents number of points to make between T.min and T.max
# X_f = np.load('./examples/human/plot/Feed_swing_pend_X.npy')
# Y_f = np.load('./examples/human/plot/Feed_pend_Y.npy')
# Yn_f = np.load('./examples/human/plot/Feed_pend_Yn.npy')
# X_f1 = np.load('./examples/human/plot/Feed_swing_pend_X1.npy')
# Y_f1 = np.load('./examples/human/plot/Feed_pend_Y1.npy')
# Yn_f1 = np.load('./examples/human/plot/Feed_pend_Yn1.npy')
# X_f2 = np.load('./examples/human/plot/Feed_swing_pend_X2.npy')
# Y_f2 = np.load('./examples/human/plot/Feed_pend_Y2.npy')
# Yn_f2 = np.load('./examples/human/plot/Feed_pend_Yn2.npy')
# X_f3 = np.load('./examples/human/plot/Feed_swing_pend_X3.npy')
# Y_f3 = np.load('./examples/human/plot/Feed_pend_Y3.npy')
# Yn_f3 = np.load('./examples/human/plot/Feed_pend_Yn3.npy')
# X_f4 = np.load('./examples/human/plot/Feed_swing_pend_X4.npy')
# Y_f4 = np.load('./examples/human/plot/Feed_pend_Y4.npy')
# Yn_f4 = np.load('./examples/human/plot/Feed_pend_Yn4.npy')

# X_fa = np.mean( np.array([X_f, X_f1, X_f2, X_f3, X_f4]), axis=0 )
# Y_fa = np.mean( np.array([Y_f, Y_f1, Y_f2, Y_f3, Y_f4]), axis=0 )
# Yn_fa = np.mean( np.array([Yn_f, Yn_f1, Yn_f2, Yn_f3, Yn_f4]), axis=0 )

# Y_fmax = np.maximum.reduce([Y_f, Y_f1, Y_f2, Y_f3, Y_f4])
# Yn_fmax = np.maximum.reduce([Yn_f, Yn_f1, Yn_f2, Yn_f3, Yn_f4])

# Y_fmin = np.minimum.reduce([Y_f, Y_f1, Y_f2, Y_f3, Y_f4])
# Yn_fmin = np.minimum.reduce([Yn_f, Yn_f1, Yn_f2, Yn_f3, Yn_f4])

plt.plot(X_a, Y_a.flatten(), 'b', linewidth=3, label='Human demonstration + PILCO')
# plt.plot(X_a, Yn_a.flatten(), 'r--', label='Predictive reward with human')
plt.plot(X_oa, Y_oa.flatten(), 'r', linewidth=3, label='PILCO')
# plt.plot(X_oa, Yn_oa.flatten(), 'b--', label='Predictive reward without human')
# plt.plot(X_fa, Y_fa.flatten(), 'g', linewidth=3, label='Human feedback + PILCO')

plt.fill_between(X_a,Y_min.flatten(),Y_max.flatten(), alpha=0.3)
# plt.fill_between(X_a,Yn_min.flatten(),Yn_max.flatten(),  alpha=0.2)
plt.fill_between(X_oa,Y_omin.flatten(),Y_omax.flatten(), alpha=0.3)
# plt.fill_between(X_oa,Yn_omin.flatten(),Yn_omax.flatten())
# plt.fill_between(X_fa,Y_fmin.flatten(),Y_fmax.flatten(), alpha=0.4)

plt.xlabel('Iterations')
plt.ylabel('Rewards')
plt.title('Cart pole swing up')
plt.legend(loc=0)
plt.show()

# plt.plot(X, Y)
# plt.plot(X, Yn.flatten())
# plt.plot(X_o, Y_o)
# plt.plot(X_o, Yn_o.flatten())
# plt.xlabel('Iterations')
# plt.ylabel('Rewards')
# plt.show()

