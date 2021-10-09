import numpy as np
import gym
from pilco.controllers import HumanController
from pilco.rewards import ExponentialReward
import tensorflow as tf
from utils_human import rollout, policy
from gpflow import set_trainable
import matplotlib.pyplot as plt
import os
np.random.seed(0)

class myPendulum():
    def __init__(self):
        self.env = gym.make('Pendulum-v0').env
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space
        ##
        self.l = 1.5
        self.m = 2

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
    N = 6
    restarts = 2

    env = myPendulum()

    # Collect data for human controller
    if os.path.exists('./examples/training_data_X.npy') & os.path.exists('./examples/training_data_Y.npy'):
        X = np.load('./examples/training_data_X.npy')
        Y = np.load('./examples/training_data_Y.npy')
    else:
        X, Y, _, _ = rollout(env, None, timesteps=T, random=True, SUBS=SUBS, render=True)
        for i in range(1,J):
            X_, Y_, _, _ = rollout(env, None, timesteps=T, random=True, SUBS=SUBS, render=True)
            X = np.vstack((X, X_))
            Y = np.vstack((Y, Y_))

    state_dim = X.shape[1]
    control_dim = Y.shape[1]

    controller = HumanController((X,Y), state_dim=state_dim, max_action=max_action)
    R = ExponentialReward(state_dim=state_dim, t=target, W=weights)

    for model in controller.model.models:
        model.likelihood.variance.assign(0.001)
        set_trainable(model.likelihood.variance, False)

    r_new = np.zeros((T, 1))
    while True:
        controller.optimize_models(maxiter=maxiter, restarts=restarts)
        X_new, Y_new, r, _ = rollout(env, None, timesteps=T, p_use=False, random=True, SUBS=SUBS, render=True)
        # for i in range(len(X_new)):
        #     r_new[:, 0] = R.compute_reward(X_new[i,None,:], 0.001 * np.eye(state_dim))[0]
        # total_r = sum(r_new)
        # print("Total ", total_r)
        print("Total reward of this turn", r)   

        # Update dataset
        X = np.vstack((X, X_new)); Y = np.vstack((Y, Y_new))
        controller.model.set_data((X, Y))

        judge = input('Continue to collect data or not? (y/n)\n')
        if judge == 'n': 
            np.save('./examples/training_data_X.npy', X)
            np.save('./examples/training_data_Y.npy', Y)
            break

    # Demonstration
    print('Evaluate the performance of the human controller\n')
    X_new, Y_new, _, _ = rollout(env, controller, timesteps=T_sim, p_use=True, SUBS=SUBS, render=True)
