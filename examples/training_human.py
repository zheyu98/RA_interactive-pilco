import numpy as np
import gym
from pilco.controllers import HumanController
from pilco.rewards import ExponentialReward
import tensorflow as tf
from utils_human import rollout_ilosa, rollout_hgdagger, rollout_both, rollout
from gpflow import set_trainable
import matplotlib.pyplot as plt
import os
np.random.seed(0)

class myPendulum():
    def __init__(self):
        self.env = gym.make('Pendulum-v1').env
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space
        ##
        self.l = 10
        self.m = 10

    def step(self, action):
        return self.env.step(action)

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

    def close(self):
        self.env.close()

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
    J = 3
    N = 6
    restarts = 2
    control_dim = 1

    env = myPendulum()

    # Collect data for human controller
    # X, Y, _, _ = rollout_both(env, timesteps=T, SUBS=SUBS, render=True)
    X = np.load("./human_X.npy")
    Y = np.load("./human_Y.npy")

    np.save("./human_X", X)
    np.save("./human_Y", Y)

    state_dim = X.shape[1]
    control_dim = Y.shape[1]
    data = [X,Y]

    controller = HumanController((X,Y), state_dim=state_dim, max_action=max_action)
    R = ExponentialReward(state_dim=state_dim, t=target, W=weights)

    # Optimize the hyper-paramters
    for model in controller.model.models:
        model.likelihood.variance.assign(0.001)
        set_trainable(model.likelihood.variance, False)

    controller.optimize_models(maxiter=maxiter, restarts=restarts)
  
    r_new = np.zeros((T, 1))
    q = 0
    while q < 10:
        # ILOSA
        controller, X_new, data = rollout_ilosa(env, data, controller, timesteps=T, control_dim=control_dim, p_use=True, SUBS=SUBS, render=True)
        print(data[0].shape[0])
        # HG-DAGGER
        # X_a, Y_a, X_new = rollout_hgdagger(env, controller, timesteps=T, control_dim=control_dim, p_use=True, SUBS=SUBS, render=True)
        # X = np.vstack((X, X_a)); Y = np.vstack((Y, Y_a))
        # controller.model.set_data((X, Y))
        
        for i in range(len(X_new)):
            r_new[:, 0] = R.compute_reward(X_new[i,None,:], 0.001 * np.eye(state_dim))[0]
        total_r = sum(r_new)
        print("Total reward of this turn", total_r)         

        q += 1

    # Demonstration
    print('Evaluate the performance of the human controller\n')
    X_new, _ = rollout(env, controller, timesteps=T, SUBS=SUBS, render=True)
    for i in range(len(X_new)):
        r_new[:, 0] = R.compute_reward(X_new[i,None,:], 0.001 * np.eye(state_dim))[0]
    total_r = sum(r_new)
    print("Total reward of this turn", total_r) 
