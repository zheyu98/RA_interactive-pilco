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

def rollout(env, controller, timesteps, control_dim=1, p_use=False, demon=False, random=False, SUBS=1, render=False):
        X = []; Y = []; human = []
        x = env.reset()
        ep_return_full = 0
        ep_return_sampled = 0

        global u_human
        u_human = 0
        in_magni = 0.2
        u_ps = tf.zeros([control_dim], dtype=tf.float64)
        if not demon:
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
                x_new, r, done, _ = env.step(u)
                ep_return_full += r
                if done: break
                if render: env.render()
            # if verbose:
            #     print("Action: ", u)
            #     print("State : ", x_new)
            #     print("Return so far: ", ep_return_full)
            X.append(x)
            Y.append(u)
            human.append(tf.zeros([control_dim], dtype=tf.float64) + cut(u_human, 10)*in_magni)
            ep_return_sampled += r
            x = x_new
            if done: break
            time.sleep(0.3)
        if not demon:
            autoin = Controller()
            autoin.press(Key.esc)
            autoin.release(Key.esc)
            t1.join()
        return np.stack(X), np.stack(Y), np.stack(human), ep_return_sampled, ep_return_full

def policy(env, pilco, x, random):
    if random:
        return env.action_space.sample()
    else:
        return pilco.compute_action(x[None, :])[0, :]

## human input
def on_press(key):
    global u_human
    if key == Key.right:
        # u_human = 8
        u_human = 5
        # u_human = 1
    if key == Key.left:
        # u_human = -8
        u_human = -5
        # u_human = 0
    if key == Key.down:
        u_human = 0
    if key == KeyCode(char = 'a'):
        if u_human <0:
            u_human += -1
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
            time.sleep(0.1)

        autoin = Controller()
        autoin.press(Key.esc)
        autoin.release(Key.esc)
        t1.join()
        env.close()
        return np.stack(Xc), np.stack(Yc), np.stack(X), np.stack(Y)

def rollout_feed(env, pilco, timesteps, random=False, SUBS=1, sig=False, render=False):
        X = []; Y = []; X_re = []; counter = 0
        x = env.reset()
        ep_return_full = 0
        ep_return_sampled = 0
        # Add human input
        global u_human
        u_human = 0
        in_magni = 1.0
        t1=threading.Thread(target=start_key_listen)
        t1.start()
        print('You could give some corrective feedback: (Left or Right arrow)')
        time.sleep(1)
        for timestep in range(timesteps):
            if render: env.render()
            if timestep == 0: time.sleep(3); print('start now!')
            u_ps = policy(env, pilco, x, random)

            ##################################################
            # if abs(u_ps-0) <= abs(u_ps-1) :u=0
            # else:u=1
            ###############################################3##

            u = u_ps + cut(u_human, 8)*in_magni
            for i in range(SUBS):
                x_new, r, done, _ = env.step(u)
                ep_return_full += r
                # if done: break
                if render: env.render()
            if sig:
                if counter % 6 == 0 or u_human != 0:
                    X.append(np.hstack((x, u)))
                    Y.append(x_new - x)
                counter += 1
            # else: 
            #     if counter % 5 == 0:
            #         X.append(np.hstack((x, u)))
            #         Y.append(x_new - x)
            #     counter += 1
            else:
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
        return np.stack(X), np.stack(Y), ep_return_sampled, ep_return_full