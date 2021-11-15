import numpy as np
import gym
from pilco.models import PILCO
from pilco.controllers import RbfController, LinearController
from pilco.rewards import ExponentialReward
import tensorflow as tf
from utils import rollout, policy
from gpflow import set_trainable
# %matplotlib inline
# import matplotlib
import matplotlib.pyplot as plt
import time
np.random.seed(0)

# NEEDS a different initialisation than the one in gym (change the reset() method),
# to (m_init, S_init), modifying the gym env

# Introduces subsampling with the parameter SUBS and modified rollout function
# Introduces priors for better conditioning of the GP model
# Uses restarts

class myPendulum():
    def __init__(self):
        self.env = gym.make('Pendulum-v1').env
        self.action_space = gym.spaces.Box(
            low=-self.env.max_torque, high=self.env.max_torque, shape=(1,), dtype=np.float64
        )
        self.observation_space = self.env.observation_space

    def step(self, u):
        th, thdot = self.env.state  # th := theta

        g = self.env.g
        m = self.env.m
        l = self.env.l
        dt = self.env.dt

        u = np.clip(u, -self.env.max_torque, self.env.max_torque)[0]
        self.env.last_u = u  # for rendering
        costs = angle_normalize(th) ** 2 + 0.1 * thdot ** 2 + 0.001 * (u ** 2)

        newthdot = thdot + (3 * g / (2 * l) * np.sin(th) + 3.0 / (m * l ** 2) * u) * dt
        newthdot = np.clip(newthdot, -self.env.max_speed, self.env.max_speed)
        newth = th + newthdot * dt

        self.env.state = np.array([newth, newthdot])
        return self.get_obs(), -costs, False, {}

    def reset(self):
        high = np.array([np.pi, 1.0])
        self.env.state = np.random.uniform(low=-high, high=high)
        self.env.state = np.random.uniform(low=0.0, high=0.01*high) # only difference
        self.env.state[0] += -np.pi
        self.env.last_u = None
        return self.get_obs()
    
    def get_obs(self):
        theta, thetadot = self.env.state
        return np.array([np.cos(theta), np.sin(theta), thetadot], dtype=np.float64)

    def render(self):
        self.env.render()

def angle_normalize(x):
    return ((x + np.pi) % (2 * np.pi)) - np.pi

if __name__=='__main__':
    SUBS=3
    bf = 30
    maxiter=50
    max_action=2.0
    target = np.array([1.0, 0.0, 0.0])
    weights = np.diag([2.0, 2.0, 0.3])
    m_init = np.reshape([-1.0, 0.0, 0.0], (1,3))
    S_init = np.diag([0.01, 0.05, 0.01])
    T = 40
    T_sim = T
    J = 4
    N = 10
    restarts = 2

    env = myPendulum()

    # Initial random rollouts to generate a dataset
    X, Y, _, _ = rollout(env, None, timesteps=T, random=True, SUBS=SUBS, render=True)
    start = time.time()
    for i in range(1,J):
        X_, Y_, _, _ = rollout(env, None, timesteps=T, random=True, SUBS=SUBS, verbose=True, render=True)
        X = np.vstack((X, X_))
        Y = np.vstack((Y, Y_))

    state_dim = Y.shape[1]
    control_dim = X.shape[1] - state_dim

    controller = RbfController(state_dim=state_dim, control_dim=control_dim, num_basis_functions=bf, max_action=max_action)
    R = ExponentialReward(state_dim=state_dim, t=target, W=weights)

    pilco = PILCO((X, Y), controller=controller, horizon=T, reward=R, m_init=m_init, S_init=S_init)

    # for numerical stability, we can set the likelihood variance parameters of the GP models
    for model in pilco.mgpr.models:
        model.likelihood.variance.assign(0.001)
        set_trainable(model.likelihood.variance, False)

    r_new = np.zeros((T, 1))
    re_p = []; count = []; re_pn = []
    for rollouts in range(N):
        print("**** ITERATION no", rollouts, " ****")
        pilco.optimize_models(maxiter=maxiter, restarts=2)
        pilco.optimize_policy(maxiter=maxiter, restarts=2)

        X_new, Y_new, _, _ = rollout(env, pilco, timesteps=T_sim, verbose=True, SUBS=SUBS, render=True)

        # Since we had decide on the various parameters of the reward function
        # we might want to verify that it behaves as expected by inspection
        for i in range(len(X_new)):
                r_new[:, 0] = R.compute_reward(X_new[i,None,:-1], 0.001 * np.eye(state_dim))[0]
        total_r = sum(r_new)
        _, _, r = pilco.predict(X_new[0,None,:-1], 0.001 * S_init, T)
        print("Total ", total_r, " Predicted: ", r)
        re_p.append(total_r)
        re_pn.append(r)
        count.append(rollouts)

        # Update dataset
        X = np.vstack((X, X_new)); Y = np.vstack((Y, Y_new))
        pilco.mgpr.set_data((X, Y))

    end = time.time()
    print("Time cost of this training process is ", end-start)

    # np.save('./examples/human/plot/swing_pend_X.npy', count)
    # np.save('./examples/human/plot/swing_pend_Y.npy', re_p)
    # np.save('./examples/human/plot/swing_pend_Yn.npy', re_pn)

    # np.save('./plot/swing_pend_X2.npy', count)
    # np.save('./plot/swing_pend_Y2.npy', re_p)
    # np.save('./plot/swing_pend_Yn2.npy', re_pn)