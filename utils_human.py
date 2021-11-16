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
from pynput.keyboard import Key, Listener, Controller, KeyCode
##
float_type = config.default_float()

def rollout(env, controller, timesteps, random=False, SUBS=1, render=False):
    X = []; Y = []
    x = env.reset()
    for timestep in range(timesteps):
        if render: env.render()
        u = policy(env, controller, x, random)
        for i in range(SUBS):
            x_new, _, _, _ = env.step(u)
            # if done: break
            if render: env.render()
        X.append(x)
        Y.append(u)
        x = x_new
        # if done: break
        time.sleep(0.1)
    return np.stack(X), np.stack(Y)

def rollout_ilosa(env, data, controller, timesteps, control_dim=1, p_use=False, random=False, SUBS=1, render=False):
    X_new = []
    X_base = data[0]; Y_base = data[1]
    x = env.reset()

    global u_human
    u_human = 0
    in_magni = 0.2
    u_ps = tf.zeros([control_dim], dtype=tf.float64)

    t1=threading.Thread(target=start_key_listen)
    t1.start()
    print('You could give some corrective feedback: (Left or Right arrow)\n')
    for timestep in range(timesteps):
        if render: env.render()
        if p_use: u_ps = policy(env, controller, x, random)
        if timestep == 0:
            sec = input('Let me know when to start.\n')
            time.sleep(int(sec))
            print('start now!')
        u = u_ps + cut(u_human, 10)*in_magni
        for i in range(SUBS):
            x_new, _, _, _ = env.step(u)
            # if done: break
            if render: env.render()
        X = x
        Y = u
        X_new.append(x)
        human = tf.zeros([control_dim], dtype=tf.float64) + cut(u_human, 10)*in_magni
        if u_human != 0:
            X_base, Y_base = check_ilosa(X_base, X, Y_base, Y, human, controller)
            controller.model.set_data((X_base, Y_base))
        x = x_new
        # if done: break
        time.sleep(0.2)
    autoin = Controller()
    autoin.press(Key.esc)
    autoin.release(Key.esc)
    t1.join()
    return controller, np.stack(X_new), [X_base,Y_base] 

def rollout_hgdagger(env, controller, timesteps, control_dim=1, p_use=False, random=False, SUBS=1, render=False):
    X = []; Y = []; X_new = []
    x = env.reset()

    global u_human
    u_human = 0
    in_magni = 0.2
    u_ps = tf.zeros([control_dim], dtype=tf.float64)

    t1=threading.Thread(target=start_key_listen)
    t1.start()
    print('You could give some corrective feedback: (Left or Right arrow)\n')
    for timestep in range(timesteps):
        if render: env.render()
        if p_use: u_ps = policy(env, controller, x, random)
        if timestep == 0:
            sec = input('Let me know when to start.\n')
            time.sleep(int(sec))
            print('start now!')
        u = u_ps + cut(u_human, 10)*in_magni
        for i in range(SUBS):
            x_new, _, _, _ = env.step(u)
            # if done: break
            if render: env.render()
        if u_human != 0:
            X.append(x)
            Y.append(u)
        x = x_new
        X_new.append(x)
        # if done: break
        time.sleep(0.3)
    autoin = Controller()
    autoin.press(Key.esc)
    autoin.release(Key.esc)
    t1.join()
    return np.stack(X), np.stack(Y), np.stack(X_new)

def policy(env, controller, x, random):
    if random:
        return env.action_space.sample()
    else:
        uh = controller.compute_action(x[None, :], tf.zeros([controller.state_dim, controller.state_dim], float_type))[0]
        return uh[0,:]

def check_ilosa(X_base, X, Y_base, Y, human, controller):
    # K_star = controller.model.K(X, X_new)
    vars = []
    for model in controller.model.models:
        vars.append(model.kernel.variance)
    vars = np.stack(vars)

    # Calculate the variance (uncertainty) at a new input
    K_starstar = controller.model.K(X, X)
    K_star = controller.model.K(X_base, X)
    K = controller.model.K(X_base, X_base)
    # print(K.shape); print(K_star.shape); print(K_starstar.shape)
    classify = []; Add = False
    for j in range(K.shape[0]):
        # print(K_star[j,...].shape); print(np.linalg.inv(K[j,...]).shape)
        var = K_starstar[j] - np.transpose(K_star[j,...,None]) @ np.linalg.inv(K[j,...]) @ K_star[j,...,None]
        var_p_max = controller.model.models[j].likelihood.variance.numpy() + controller.model.models[j].kernel.variance.numpy()
        var_p_min = controller.model.models[j].likelihood.variance.numpy()
        if (var-var_p_min) / (var_p_max-var_p_min) > 0.3: classify.append(True)
        else: classify.append(False)
    classify = np.array(classify)
    if np.all(classify): Add = True

    if Add:
        # add
        X_base = np.vstack((X_base, X))
        Y_base = np.vstack((Y_base, Y)) 
    else:
        diff_a = controller.model.K(X_base, X) / vars[:, np.newaxis]
        i1 = diff_a * human
        # i2 = np.transpose(np.squeeze(i1,axis=2))
        i2 = np.transpose(i1)
        Y_base = Y_base + i2
   
    return X_base, Y_base

## human input
def on_press(key):
    global u_human
    if key == Key.right:
        u_human = 8
    if key == Key.left:
        u_human = -8
    if key == Key.down:
        u_human = 0
    if key == KeyCode(char = 'a'):
        if u_human <0:
            u_human -= 1
        else:
            u_human = -1
    if key == KeyCode(char = 'd'):
        if u_human >0:
            u_human += 1
        else:
            u_human = 1
    if key == KeyCode(char = 's'):
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

def rollout_both(env, timesteps, SUBS=1, random=False, render=False):
        X = []; Y = []; Xc = []; Yc = []; counter = 0
        x = env.reset()
        ep_return_full = 0
        ep_return_sampled = 0

        global u_human
        u_human = 0
        in_magni = 0.2
        u_ps = tf.zeros([1], dtype=tf.float64)

        t1=threading.Thread(target=start_key_listen)
        t1.start()
        print('You could give some corrective feedback: (Left or Right arrow)\n')

        for timestep in range(timesteps):
            if render: env.render()
            if timestep == 0:
                sec = input('Let me know when to start.\n')
                time.sleep(int(sec))
                print('start now!')
            u = u_ps + cut(u_human, 10)*in_magni
            # u = u_human + u_ps
            if random: u = env.action_space.sample()
            for i in range(SUBS):
                # x_new, r, done, _, sig = env.step(u)
                x_new, r, done, _ = env.step(u)
                ep_return_full += r
                # if done: break
                if render: env.render()
            # if counter % 5 == 0:
            #     Xc.append(x)
            #     Yc.append(u)
            #     X.append(np.hstack((x, u)))
            #     Y.append(x_new - x)
            # counter += 1
            Xc.append(x)
            Yc.append(u)
            X.append(np.hstack((x, u)))
            Y.append(x_new - x)
            ep_return_sampled += r
            x = x_new
            # if done: break
            time.sleep(0.2)

        autoin = Controller()
        autoin.press(Key.esc)
        autoin.release(Key.esc)
        t1.join()
        env.close()
        return np.stack(Xc), np.stack(Yc), np.stack(X), np.stack(Y)