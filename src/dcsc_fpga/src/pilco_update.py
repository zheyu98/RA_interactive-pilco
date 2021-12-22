#!/home/zheyu/anaconda3/envs/RA/bin/python
from sys import flags
import rospy
import numpy as np
import tensorflow as tf
import threading
import os
import gym
from tensorflow_probability import bijectors as tfb
import gpflow
import time
import random as rand
import matplotlib.pyplot as plt
from pynput.keyboard import Key, Listener, Controller, KeyCode
from pilco.models import PILCO
from pilco.controllers import RbfController, LinearController
from pilco.rewards import ExponentialReward
from gpflow import set_trainable
from dcsc_fpga.srv import Contr, ContrResponse
from dcsc_fpga.msg import MopsSensors
from data_coll import data_collect
import dill
import pickle

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class def_pilco(object):
    def __init__(self, X, Y):
        self.bf = 60
        self.maxiter=50
        self.max_action=1.5
        self.target = np.array([1.0, 0.0, 0.0])
        self.weights = np.diag([2.0, 2.0, 0.3])
        self.m_init = np.reshape([-1.0, 0.0, 0.0], (1,3))
        self.S_init = np.diag([0.05, 0.05, 0.01])
        self.T_sim = 40
        self.horizon = 40
        self.restarts = 2
        self.state_dim = Y.shape[1]
        self.control_dim = X.shape[1] - self.state_dim

        self.X_base = X
        self.Y_base = Y

        self.controller = RbfController(state_dim=self.state_dim, control_dim=self.control_dim, num_basis_functions=self.bf, max_action=self.max_action)
        self.R = ExponentialReward(state_dim=self.state_dim, t=self.target, W=self.weights)
        self.pilco = PILCO((X, Y), controller=self.controller, horizon=self.horizon, reward=self.R, m_init=self.m_init, S_init=self.S_init)

        self.control_service = rospy.Service('/pilco/controll', Contr, self.controll)
    
    def constraints(self):
        for model in self.pilco.mgpr.models:
            model.likelihood.variance.assign(0.001)
            # model.kernel.lengthscales.assign([0.2, 0.2, 1.0, 1.0])
            # model.kernel.lengthscales.assign(lens[j,:])
            # model.kernel.variance.assign(0.5) 
            # model.kernel.variance.assign(var[j])       
            # set_trainable(model.kernel.lengthscales, False)
            # set_trainable(model.kernel.variance, False)
            set_trainable(model.likelihood.variance, False)
    
    def optimize(self):
        self.pilco.optimize_models(maxiter=self.maxiter, restarts=self.restarts)
        self.pilco.optimize_policy(maxiter=self.maxiter, restarts=self.restarts)

    def set_data(self, X_new, Y_new):
        self.X_base = np.vstack((self.X_base, X_new))
        self.Y_base = np.vstack((self.Y_base, Y_new))
        print(self.X_base.shape)
        self.pilco.mgpr.set_data((self.X_base, self.X_base))
    
    # def controll(self, states):
    #     x = np.array([np.cos(states.angle), np.sin(states.angle), states.velocity], dtype=np.float64)
    #     u = self.pilco.compute_final_action(x[None, :])[0, :]
    #     response = ContrResponse()
    #     response.action = u
    #     return response

    def controll(self, angle, velocity):
        x = np.array([np.cos(angle), np.sin(angle), velocity], dtype=np.float64)
        u = self.pilco.compute_final_action(x[None, :])[0, :]
        return u

    def reward(self, X_new):
        r_new = np.zeros((self.T_sim, 1))
        for i in range(len(X_new)):
            r_new[:, 0] = self.R.compute_reward(X_new[i,None,:-1], 0.001 * np.eye(self.state_dim))[0]
        total_r = sum(r_new)
        _, _, r = self.pilco.predict(X_new[0,None,:-1], 0.001 * self.S_init, self.T_sim)
        print("Total ", total_r, " Predicted: ", r)

    def plots(self, X_new):
        m_p = np.zeros((self.T_sim, self.state_dim))
        S_p = np.zeros((self.T_sim, self.state_dim, self.state_dim))

        m_p[0,:] = self.m_init
        S_p[0, :, :] = self.S_init

        for h in range(1, self.T_sim):
            m_p[h,:], S_p[h,:,:] = self.pilco.propagate(m_p[h-1, None, :], S_p[h-1,:,:])
            

        for i in range(self.state_dim):    
            plt.plot(range(self.T_sim-1), m_p[0:self.T_sim-1, i], X_new[1:self.T_sim, i]) # can't use Y_new because it stores differences (Dx)
            plt.fill_between(range(self.T_sim-1),
                            m_p[0:self.T_sim-1, i] - 2*np.sqrt(S_p[0:self.T_sim-1, i, i]),
                            m_p[0:self.T_sim-1, i] + 2*np.sqrt(S_p[0:self.T_sim-1, i, i]), alpha=0.2)
            plt.show()
      
if __name__ == '__main__':   
    rospy.init_node('pilco_node')
    rospy.sleep(3)
    J = 2
    N = 10

    data = data_collect()
    rospy.set_param('rand_controll',True)
    X, Y = data.collect()
    rospy.set_param('rand_controll',False)
    rospy.set_param('stop',True)
    rospy.sleep(3)
    for i in range(J-1):
        rospy.set_param('stop',False)
        rospy.set_param('rand_controll',True)
        X_, Y_ = data.collect()
        rospy.set_param('rand_controll',False)
        rospy.set_param('stop',True)
        X = np.vstack((X, X_))
        Y = np.vstack((Y, Y_))
        rospy.sleep(3)
    
    pilco = def_pilco(X, Y)
    pilco.constraints()
    
    for rollouts in range(N):
        print("**** ITERATION no", rollouts, " ****")
        pilco.optimize()
        with open('pilco_model.pkl', 'wb') as wf:
            frozen_model = gpflow.utilities.freeze(pilco)
            dill.dump(frozen_model, wf)

        rospy.set_param('stop',False)
        rospy.set_param('pilco_controll',True)
        X_new, Y_new = data.collect()
        rospy.set_param('pilco_controll',False)
        rospy.set_param('stop',True)

        fig1,ax1 = plt.subplots()
        ax1.plot(X_new[:,0],label='1')
        ax1.plot(X_new[:,1],label='2')
        ax1.plot(X_new[:,2],label='3')
        ax1.plot(X_new[:,3],label='4')
        ax1.legend()

        fig2,ax2 = plt.subplots()
        ax2.plot(Y_new[:,0],label='1')
        ax2.plot(Y_new[:,1],label='2')
        ax2.plot(Y_new[:,2],label='3')
        ax2.legend()

        pilco.set_data(X_new, Y_new)
        pilco.reward(X_new)
    pilco.plots(X_new)

    rospy.spin()


    








