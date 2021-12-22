import numpy as np
from gpflow import config
from gym import make
import os
import tensorflow as tf
from pilco.models import PILCO
from pilco.rewards import ExponentialReward
from pilco.controllers import RbfController
import gpflow
##  
import time
import pynput
import threading
from pynput.keyboard import Key, Listener, Controller
##
float_type = config.default_float()

def rollout(env, pilco, timesteps, verbose=True, random=False, SUBS=1, render=False):
        X = []; Y = []; counter = 0
        x = env.reset()
        ep_return_full = 0
        ep_return_sampled = 0
        ## Add human input
        # global u_human
        # u_human = 0
        # in_magni = 0.2
        # t1=threading.Thread(target=start_key_listen)
        # t1.start()
        # print('You could give some corrective feedback: (Left or Right arrow)')
        # time.sleep(1)
        for timestep in range(timesteps):
            if render: env.render()
            # if timestep == 0:
            #     sec = input('Let me know when to start.\n')
            #     time.sleep(int(sec))
            #     print('start now!')
            u_ps = policy(env, pilco, x, random)

            ##################################################
            # if abs(u_ps-0) <= abs(u_ps-1) :u=0
            # else:u=1
            ###############################################3##

            u = u_ps #+ cut(u_human, 8)*in_magni
            for i in range(SUBS):
                x_new, r, done, _ = env.step(u)
                ep_return_full += r
                # if done: break
                if render: env.render()
            # if verbose:
            #     print("Action: ", u)
            #     print("State : ", x_new)
            #     print("Return so far: ", ep_return_full)

            ##########################
            # if sig == 1:
            #     X.append(np.hstack((x, u)))
            #     Y.append(x_new - x)
            #     ep_return_sampled += r
            #     x = x_new
            ##########################
            if counter % 5 == 0:
                X.append(np.hstack((x, u)))
                Y.append(x_new - x)
            counter += 1
            # X.append(np.hstack((x, u)))
            # Y.append(x_new - x)
            ep_return_sampled += r
            x = x_new
            # if done: break
            #if done: success = True
            # time.sleep(0.1)
        # autoin = Controller()
        # autoin.press(Key.esc)
        # autoin.release(Key.esc)
        # t1.join()
        return np.stack(X), np.stack(Y), ep_return_sampled, ep_return_full#, success

def policy(env, pilco, x, random):
    # if random:
    #     return env.action_space.sample()
    # else:
    #     return pilco.compute_action(x[None, :])[0, :]
    # env.action_space.np_random.seed(123)
    if random:
        return env.action_space.sample()
    else:
        return pilco.compute_action(x[None, :])[0, :]

## human input
def on_press(key):
    global u_human
    if key == Key.right:
        if u_human>0:
            u_human += 2
        else:
            u_human = 2
    if key == Key.left:
        if u_human<0:
            u_human -= 2
        else:
            u_human = -2
    if key == Key.down:
        u_human = 0

def on_release(key):
    if key == Key.esc:
        return False

def start_key_listen():
    with Listener(on_press=on_press, on_release=on_release) as KeyboardListener:
        KeyboardListener.join()

def cut(x,umax):
    if x < -umax:
        x = -umax
    if x > umax:
        x = umax
    return x

class Normalised_Env():
    def __init__(self, env_id, m, std):
        self.env = make(env_id).env
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

def save_pilco(path, X, Y, pilco, sparse=False):
    os.makedirs(path)
    # Dit hoeft eigenlijk niet. Staat in pilco.controller.models[0].X & Y
    np.savetxt(path + 'X.csv', X, delimiter=',')
    np.savetxt(path + 'Y.csv', Y, delimiter=',')
    if sparse:
        with open(path+ 'n_ind.txt', 'w') as f:
            f.write('%d' % pilco.mgpr.num_induced_points)
            f.close()
    np.save(path + 'pilco_values.npy', gpflow.utilities.parameter_dict(pilco))
    #for i,m in enumerate(pilco.mgpr.models):
    #    np.save(path + "model_" + str(i) + ".npy", gpflow.utilities.parameter_dict(m))

def load_pilco(path, sparse=False, controller=None, reward=None, m_init=None, S_init=None):
    X = np.loadtxt(path + 'X.csv', delimiter=',').reshape(-1, 4)
    Y = np.loadtxt(path + 'Y.csv', delimiter=',').reshape(-1, 3)

    if not sparse:
        pilco = PILCO((X, Y), controller=controller, reward=reward, m_init=m_init, S_init=S_init)
    else:
        with open(path+ 'n_ind.txt', 'r') as f:
            n_ind = int(f.readline())
            f.close()
        pilco = PILCO((X, Y), controller=controller, reward=reward, m_init=m_init, S_init=S_init, num_induced_points=n_ind)
    params = np.load(path + "pilco_values.npy", allow_pickle=True).item()
    print(params)
    gpflow.utilities.multiple_assign(pilco, params)
    #for i,m in enumerate(pilco.mgpr.models):
    #    values = np.load(path + "model_" + str(i) + ".npy", allow_pickle=True).item()
    #    print(values)
    #    gpflow.utilities.multiple_assign(m, values)
    return pilco, X, Y

def rollout_comb(env, pilco, timesteps, verbose=True, random=False, SUBS=1, render=False):
        X = []; Y = []; counter = 0
        x = env.reset()
        ep_return_full = 0
        ep_return_sampled = 0
        for timestep in range(timesteps):
            if render: env.render()
            u_ps = policy(env, pilco, x, random)
            u = u_ps #+ cut(u_human, 8)*in_magni
            for i in range(SUBS):
                x_new, r, done, _ = env.step(u)
                ep_return_full += r
                # if done: break
                if render: env.render()
            # if counter % 5 == 0:
            #     X.append(np.hstack((x, u)))
            #     Y.append(x_new - x)
            # counter += 1
            X.append(np.hstack((x, u)))
            Y.append(x_new - x)
            ep_return_sampled += r
            x = x_new
            # if done: break
            # time.sleep(0.1)
        return np.stack(X), np.stack(Y), ep_return_sampled, ep_return_full
