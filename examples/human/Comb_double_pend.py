import numpy as np
from numpy import sin, cos, pi
import gym
from gym import spaces
from pilco.models import PILCO
from pilco.controllers import RbfController, LinearController, CombController
from pilco.rewards import ExponentialReward
import tensorflow as tf
from utils import rollout, policy
from utils_human import rollout_both
from gpflow import set_trainable
# %matplotlib inline
# import matplotlib
import matplotlib.pyplot as plt
import os
np.random.seed(0)

class mydoublepend():
    def __init__(self):
        self.env = gym.make('Acrobot-v1').env
        self.max_torque = 2.0
        self.action_space = spaces.Box(
            low=-self.max_torque, high=self.max_torque, shape=(1,), dtype=np.float64
        )
        high = np.array(
            [1.0, 1.0, 1.0, 1.0, self.env.MAX_VEL_1, self.env.MAX_VEL_2], dtype=np.float64
        )
        low = -high
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float64)

    def step(self, action):
        s = self.env.state
        torque = action

        s_augmented = np.append(s, torque)

        ns = rk4(self.env._dsdt, s_augmented, [0, self.env.dt])

        ns[0] = wrap(ns[0], -pi, pi)
        ns[1] = wrap(ns[1], -pi, pi)
        ns[2] = bound(ns[2], -self.env.MAX_VEL_1, self.env.MAX_VEL_1)
        ns[3] = bound(ns[3], -self.env.MAX_VEL_2, self.env.MAX_VEL_2)
        self.env.state = ns
        terminal = self.env._terminal()
        reward = -1.0 if not terminal else 0.0
        return (self._get_ob(), reward, terminal, {})
    
    def reset(self):
        self.env.state = self.env.np_random.uniform(low=-0.1, high=0.1, size=(4,)).astype(
            np.float64
        )
        return self._get_ob()
    
    def render(self):
        self.env.render()

    def _get_ob(self):
        s = self.env.state
        return np.array(
            [cos(s[0]), sin(s[0]), cos(s[1]), sin(s[1]), s[2], s[3]], dtype=np.float64
        )
    
    def close(self):
        self.env.close()

def wrap(x, m, M):
    diff = M - m
    while x > M:
        x = x - diff
    while x < m:
        x = x + diff
    return x

def bound(x, m, M=None):
    if M is None:
        M = m[1]
        m = m[0]
    return min(max(x, m), M)

def rk4(derivs, y0, t):
    try:
        Ny = len(y0)
    except TypeError:
        yout = np.zeros((len(t),), np.float_)
    else:
        yout = np.zeros((len(t), Ny), np.float_)

    yout[0] = y0

    for i in np.arange(len(t) - 1):

        thist = t[i]
        dt = t[i + 1] - thist
        dt2 = dt / 2.0
        y0 = yout[i]

        k1 = np.asarray(derivs(y0))
        k2 = np.asarray(derivs(y0 + dt2 * k1))
        k3 = np.asarray(derivs(y0 + dt2 * k2))
        k4 = np.asarray(derivs(y0 + dt * k3))
        yout[i + 1] = y0 + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
    return yout[-1][:4]

if __name__=='__main__':
    SUBS=3
    bf = 30
    maxiter=50
    max_action=2.0
    target = np.array([0.0, 1.0, 1.0, 0.0, 0.0, 0.0])
    weights = np.diag([2.0, 2.0, 2.0, 2.0, 0.3, 0.3])
    m_init = np.reshape([1.0, 0.0, 1.0, 0.0, 0.0, 0.0], (1,6))
    S_init = np.diag([0.01, 0.05, 0.01, 0.05, 0.01, 0.01])
    T = 100
    T_sim = T
    J = 2
    N = 6
    restarts = 2
 
    env = mydoublepend()

    if input("Give demonstration or not (y/n)\n") == 'y':
        Xc, Yc, X, Y = rollout_both(env,timesteps=T,SUBS=SUBS, render=True)
    else:
        if os.path.exists('./examples/human/training_data_X.npy') & os.path.exists('./examples/human/training_data_Y.npy') \
        & os.path.exists('./examples/human/training_data_Yc.npy') & os.path.exists('./examples/human/training_data_Xc.npy'):
            Xc = np.load('./examples/human/training_data_Xc.npy')
            Yc = np.load('./examples/human/training_data_Yc.npy')
            X = np.load('./examples/human/training_data_X.npy')
            Y = np.load('./examples/human/training_data_Y.npy')
        else:
            raise Exception('Please give demonstration')

    np.save('./examples/human/training_data_X.npy', X)
    np.save('./examples/human/training_data_Y.npy', Y)
    np.save('./examples/human/training_data_Xc.npy', Xc)
    np.save('./examples/human/training_data_Yc.npy', Yc)

    data_c = [Xc,Yc]
    state_dim = Y.shape[1]
    control_dim = X.shape[1] - state_dim

    R = ExponentialReward(state_dim=state_dim, t=target, W=weights)
    controller = CombController(data_c, max_action=max_action)
    pilco = PILCO((X, Y), controller=controller, horizon=T, reward=R, m_init=m_init, S_init=S_init)
    print("Start PILCO optimization!")

    # Initial random rollouts to generate a dataset
    # X, Y, _, _ = rollout(env, pilco, timesteps=T, random=True, SUBS=SUBS, render=True)
    for i in range(1,J):
        X_, Y_, _, _, success = rollout(env, pilco, timesteps=T, random=False, SUBS=SUBS, render=True)
        X = np.vstack((X, X_))
        Y = np.vstack((Y, Y_))
    pilco.mgpr.set_data((X, Y))

    # for numerical stability, we can set the likelihood variance parameters of the GP models
    for model in pilco.mgpr.models:
        model.likelihood.variance.assign(0.001)
        set_trainable(model.likelihood.variance, False)

    r_new = np.zeros((T, 1))
    for rollouts in range(N):
        print("**** ITERATION no", rollouts, " ****")
        pilco.optimize_models(maxiter=maxiter, restarts=2)
        pilco.optimize_policy(maxiter=maxiter, restarts=2)

        X_new, Y_new, _, _, success = rollout(env, pilco, timesteps=T_sim, verbose=True, SUBS=SUBS, render=True)

        # Since we had decide on the various parameters of the reward function
        # we might want to verify that it behaves as expected by inspection
        if success:
            print("Succeed in ", rollouts, "th rollout")
        for i in range(len(X_new)):
                r_new[:, 0] = R.compute_reward(X_new[i,None,:-1], 0.001 * np.eye(state_dim))[0]
        total_r = sum(r_new)
        _, _, r = pilco.predict(X_new[0,None,:-1], 0.001 * S_init, T)
        print("Total ", total_r, " Predicted: ", r)

        # Update dataset
        X = np.vstack((X, X_new)); Y = np.vstack((Y, Y_new))
        pilco.mgpr.set_data((X, Y))

    last = input('last command (y/n)\n')
    if last == 'y':
        print("**** Last visual ****")
        X_new, Y_new, _, _ = rollout(env, pilco, timesteps=T_sim, verbose=True, SUBS=SUBS, render=True)
        while True:
            ornot = input('watch again? (y/n)\n')
            if ornot == 'y':
                X_new, Y_new, _, _ = rollout(env, pilco, timesteps=T_sim, verbose=True, SUBS=SUBS, render=True)
            else:
                break

    for i,m in enumerate(pilco.mgpr.models):
        y_pred_test, var_pred_test = m.predict_y(X_new)
        plt.plot(range(len(y_pred_test)), y_pred_test, Y_new[:,i])
        plt.fill_between(range(len(y_pred_test)),
                        y_pred_test[:,0] - 2*np.sqrt(var_pred_test[:, 0]), 
                        y_pred_test[:,0] + 2*np.sqrt(var_pred_test[:, 0]), alpha=0.3)
        plt.show()

    np.shape(var_pred_test)

    m_p = np.zeros((T, state_dim))
    S_p = np.zeros((T, state_dim, state_dim))

    m_p[0,:] = m_init
    S_p[0, :, :] = S_init

    for h in range(1, T):
        m_p[h,:], S_p[h,:,:] = pilco.propagate(m_p[h-1, None, :], S_p[h-1,:,:])
        

    for i in range(state_dim):    
        plt.plot(range(T-1), m_p[0:T-1, i], X_new[1:T, i]) # can't use Y_new because it stores differences (Dx)
        plt.fill_between(range(T-1),
                        m_p[0:T-1, i] - 2*np.sqrt(S_p[0:T-1, i, i]),
                        m_p[0:T-1, i] + 2*np.sqrt(S_p[0:T-1, i, i]), alpha=0.2)
        plt.show()