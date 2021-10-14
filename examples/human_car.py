import numpy as np
import gym
from gym import spaces
from pilco.controllers import HumanController
from pilco.rewards import ExponentialReward
import tensorflow as tf
from utils_human import rollout, policy
from gpflow import set_trainable
import matplotlib.pyplot as plt
import os
np.random.seed(0)

class myCar():
    def __init__(self):
        self.env = gym.make('MountainCarContinuous-v0').env
        self.min_action = self.env.min_action
        self.max_action = self.env.max_action
        self.min_position = self.env.min_position
        self.max_position = self.env.max_position
        self.max_speed = self.env.max_speed
        self.low_state = np.array(
            [self.min_position, -self.max_speed], dtype=np.float64
        )
        self.high_state = np.array(
            [self.max_position, self.max_speed], dtype=np.float64
        )

        self.action_space = spaces.Box(
            low=self.min_action, high=self.max_action, shape=(1,), dtype=np.float64
        )
        self.observation_space = spaces.Box(
            low=self.low_state, high=self.high_state, dtype=np.float64
        )

    def step(self, action):
        return self.env.step(action)

    def reset(self):
        self.env.state = np.array([self.env.np_random.uniform(low=-0.6, high=-0.4), 0])
        return np.array(self.env.state, dtype=np.float64)

    def render(self):
        self.env.render()

    def close(self):
        self.env.close()

class Normalised_Env():
    def __init__(self, env, m, std):
        self.env = env
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space
        self.m = m
        self.std = std

    def state_trans(self, x):
        return np.divide(x-self.m, self.std)

    def step(self, action):
        ob, r, done, _ = self.env.step(action)
        return self.state_trans(ob), r, done, {}

    def reset(self):
        ob =  self.env.reset()
        return self.state_trans(ob)

    def render(self):
        self.env.render()


def check(X, Y, R, X_new, Y_new, R_new, ep):
    len = X.shape[0]; len_new = X_new.shape[0]; ind = []
    for i in range(len_new):
        for j in range(len):
            err = abs(X_new[i,:]-X[j,:]) 
            if np.all(err < ep) and ((X_new[i,-1]<0) == (X[j,-1]<0)):
                if R[j] < R_new[i]: X[j,:] = X_new[i,:]; Y[j,:] = Y_new[i,:]; R[j] = R_new[i]
                #     X_new = np.delete(X_new,i,axis=0); Y_new = np.delete(Y_new,i,axis=0); R_new = np.delete(R_new,i)
                # else: X_new = np.delete(X_new,i,axis=0); Y_new = np.delete(Y_new,i,axis=0); R_new = np.delete(R_new,i)
                ind.append(i)
    X_new = np.delete(X_new,ind,axis=0); Y_new = np.delete(Y_new,ind,axis=0); R_new = np.delete(R_new,ind)
    X = np.vstack((X, X_new)); Y = np.vstack((Y, Y_new)); R = np.append(R, R_new)
    return X, Y, R


if __name__=='__main__':
    SUBS = 5
    T = 25
    env = myCar()

    # Initial random rollouts to generate a dataset
    X1, Y1, R, _, _ =  rollout(env, None, timesteps=T, SUBS=SUBS, render=True)
    # for i in range(1,5):
    #     X1_, Y1_,_,_ = rollout(env=env, pilco=None, random=True,  timesteps=T, SUBS=SUBS, render=True)
    #     X1 = np.vstack((X1, X1_))
    #     Y1 = np.vstack((Y1, Y1_))
    env.close()

    env = Normalised_Env(env, np.mean(X1[:,:2],0), np.std(X1[:,:2], 0))
    X = np.zeros(X1.shape)
    X = np.divide(X1 - np.mean(X1,0), np.std(X1, 0))
    Y = Y1

    state_dim = X.shape[1]
    control_dim = Y.shape[1]
    m_init =  np.transpose(X[0,:,None])
    S_init =  0.5 * np.eye(state_dim)
    controller = HumanController((X,Y), state_dim=state_dim)
    # R = ExponentialReward(state_dim=state_dim, t=target, W=weights)

    # Optimize the hyper-paramters
    for model in controller.model.models:
        model.likelihood.variance.assign(0.05)
        set_trainable(model.likelihood.variance, False)

    controller.model.set_data((X, Y))
    controller.optimize_models(maxiter=100, restarts=3)
  
    # r_new = np.zeros((T, 1))
    counter = 0
    j2 = input("Continue to collect data or not? (y/n)\n")
    if j2 == 'y':
        while True:
            if counter < 1:
                X_new, Y_new, R_new, r, _ = rollout(env, controller, timesteps=T, p_use=False, SUBS=SUBS, render=True)
            else:
                X_new, Y_new, R_new, r, _ = rollout(env, controller, timesteps=T, p_use=True, SUBS=SUBS, render=True)
            counter += 1
            print("Total reward of this turn", r)   

            # Update dataset
            ep = [0.05, 0.01]
            X, Y, R = check(X, Y, R, X_new, Y_new, R_new, ep)
            controller.model.set_data((X, Y))
            
            judge = input('Continue to collect data or not? (y/n)\n')
            if judge == 'n': 
                # np.save('./examples/training_data_X.npy', X)
                # np.save('./examples/training_data_Y.npy', Y)
                break
    else:
        controller.model.set_data((X, Y))

    # Demonstration
    print('Evaluate the performance of the human controller\n')
    X_new, Y_new, R_new, r, _ = rollout(env, controller, timesteps=T, p_use=True, demon=True, SUBS=SUBS, render=True)
    print("Total reward of this turn", r)
