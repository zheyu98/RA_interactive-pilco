
import numpy as np
import gym
from gym import spaces
from pilco.models import PILCO
from pilco.controllers import HumanController, CombController, RbfController
from pilco.rewards import ExponentialReward, ExplodeReward, CombinedRewards
import tensorflow as tf
from utils import rollout, policy, rollout_comb
from utils_human import rollout_both, rollout_feed
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
        # self.env.max_position += 5
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
        self.env.state = np.array([self.env.np_random.uniform(low=-0.4, high=-0.2), 0])
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

    def close(self):
        self.env.close()

if __name__=='__main__':
    SUBS = 5
    T = 30
    env = myCar()
    env_re = myCar()
    # env = gym.make('MountainCarContinuous-v0')
    max_action = env.max_action
    
    X1, Y1, _, _ = rollout(env, None, timesteps=T, random=True, SUBS=SUBS, render=False)
    for i in range(1,4):
        X_, Y_, _, _ = rollout(env, None, timesteps=T, random=True, SUBS=SUBS, render=False)
        X1 = np.vstack((X1, X_))
        Y1 = np.vstack((Y1, Y_))

    env = Normalised_Env(env, np.mean(X1[:,:2],0), np.std(X1[:,:2], 0))
    env_re = Normalised_Env(env_re, np.mean(X1[:,:2],0), np.std(X1[:,:2], 0))
    # X = np.zeros(X1.shape)
    # X[:, :2] = np.divide(X1[:, :2] - np.mean(X1[:,:2],0), np.std(X1[:,:2], 0))
    # X[:, 2] = X1[:,-1] # control inputs are not normalised
    # Y = np.divide(Y1 , np.std(X1[:,:2], 0))

    # Xc = np.zeros(Xc1.shape)
    # Xc = np.divide(Xc1 - np.mean(Xc1,0), np.std(Xc1, 0))
    # Yc = Yc1

    if input("Give demonstration or not (y/n)\n") == 'y':
        Xc, Yc, X, Y = rollout_both(env,timesteps=T,SUBS=SUBS, render=True)

    state_dim = Y.shape[1]
    control_dim = X.shape[1] - state_dim
    m_init =  np.transpose(X[0,:-1,None])
    # m_init = np.reshape([0.0, 0.0], (1,2))
    S_init =  0.5 * np.eye(state_dim)

    controller = CombController(data=[Xc,Yc], max_action=max_action)
    # controller = RbfController(state_dim=state_dim, max_action=max_action, control_dim=control_dim, num_basis_functions=25)

    R = ExplodeReward(state_dim=1,
                    t=np.divide([-0.5,0.0] - env.m, env.std)[0],
                    W=np.array([0.5]),
                    select = [0]
                    )
    Rp = ExponentialReward(state_dim=state_dim,
                        t=np.divide([0.5,0.0] - env.m, env.std),
                        W=np.diag([0.5,0.1])
                        )
    R_pos = ExplodeReward(state_dim=1,
                    t=np.divide([-0.5,0.0] - env.m, env.std)[0],
                    W=np.array([1.0]) + 1e-6,
                    select = [0]
                    )
    R_vel = ExponentialReward(state_dim=1,
                    t=np.divide([-0.5,0.0] - env.m, env.std)[1],
                    W=np.array([1.0]) + 1e-6,
                    select = [1]
                    )
    R_comb = CombinedRewards(state_dim=state_dim, rewards=[R_pos, R_vel], coefs=[1.0, 2.0])

    pilco = PILCO((X, Y), controller=controller, horizon=T, reward=Rp, m_init=m_init, S_init=S_init)

    # _, _, X1, Y1 = rollout(env,timesteps=T,SUBS=SUBS, render=True)
    for i in range(1,4):
        X_, Y_, _, _ = rollout_feed(env, pilco, timesteps=T, random=False, sig=True, SUBS=SUBS, render=True)
        # _, _, X_, Y_ = rollout(env,timesteps=T,SUBS=SUBS, render=True)
        X = np.vstack((X, X_))
        Y = np.vstack((Y, Y_))
    pilco.mgpr.set_data((X,Y))

    best_r = 0
    all_Rs = np.zeros((X.shape[0], 1))
    for i in range(len(all_Rs)):
        all_Rs[i,0] = Rp.compute_reward(X[i,None,:-1], 0.001 * np.eye(state_dim))[0]

    ep_rewards = np.zeros((len(X)//T,1))
    for i in range(len(ep_rewards)):
        ep_rewards[i] = sum(all_Rs[i * T: i*T + T])
    r_new = np.zeros((T, 1))

    for model in pilco.mgpr.models:
        model.likelihood.variance.assign(0.05)
        set_trainable(model.likelihood.variance, False)

    re_p = []; count = []; re_pn = []
    for rollouts in range(10):
        print("**** ITERATION no", rollouts, " ****")
        pilco.optimize_models(maxiter=80, restarts=2)
        pilco.optimize_policy(maxiter=80, restarts=2)
        # import pdb; pdb.set_trace()
        X_new, Y_new,_,_ = rollout_comb(env=env, pilco=pilco, timesteps=T, SUBS=SUBS, render=True)

        for i in range(len(X_new)):
            r_new[i, :] = Rp.compute_reward(X_new[i,None,:-1], 0.001 * np.eye(state_dim))[0]
        total_r = sum(r_new)
        _, _, r = pilco.predict(m_init, S_init, T)
        re_p.append(total_r)
        re_pn.append(r)
        count.append(rollouts)

        print("Total ", total_r, " Predicted: ", r)
        X = np.vstack((X, X_new)); Y = np.vstack((Y, Y_new))
        all_Rs = np.vstack((all_Rs, r_new)); ep_rewards = np.vstack((ep_rewards, np.reshape(total_r,(1,1))))
        pilco.mgpr.set_data((X, Y))

    np.save('./plot/Feed_Comb_montain_car_X3.npy', count)
    np.save('./plot/Feed_Comb_montain_car_Y3.npy', re_p)
    np.save('./plot/Feed_Comb_montain_car_Yn3.npy', re_pn)
