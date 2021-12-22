#!/home/zheyu/anaconda3/envs/RA/bin/python
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
from dcsc_fpga.srv import MopsWrite, MopsWriteRequest
from dcsc_fpga.msg import MopsSensors
from std_msgs.msg import Float64
import dill

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def check(X_base, X, controller):
    # K_star = controller.model.K(X, X_new)
    vars = []
    for model in controller.models:
        vars.append(model.kernel.variance)
    vars = np.stack(vars)

    # Calculate the variance (uncertainty) at a new input
    K_starstar = controller.K(X, X)
    K_star = controller.K(X_base, X)
    K = controller.K(X_base, X_base)
    # print(K.shape); print(K_star.shape); print(K_starstar.shape)
    classify = []; Add = False
    for j in range(K.shape[0]):
        # print(K_star[j,...].shape); print(np.linalg.inv(K[j,...]).shape)
        var = K_starstar[j] - np.transpose(K_star[j,...,None]) @ np.linalg.inv(K[j,...]) @ K_star[j,...,None]
        var_p_max = controller.models[j].likelihood.variance.numpy() + controller.models[j].kernel.variance.numpy()
        var_p_min = controller.models[j].likelihood.variance.numpy()
        if (var-var_p_min) / (var_p_max-var_p_min) > 0.3: classify.append(True)
        else: classify.append(False)
    classify = np.array(classify)
    if np.any(classify): Add = True

    return Add

class data_collect(object):
    def __init__(self):
        self.mops_data = None
        self.X_base = None
        self.Y_base = None
        self.length = 100

        # Subscriber and service
        rospy.Subscriber('/mops/read', MopsSensors, self.read_callback)
        # rospy.Subscriber('/pilco/contr_sig', Float64, self.contr_callback)
        rospy.wait_for_message('/mops/read', MopsSensors, timeout=rospy.Duration(1))

    def read_callback(self, msg):
        self.mops_data = msg
        self.joint_angle = self.mops_data.position0
        self.joint_velocity = self.mops_data.speed
        self.joint_torque = self.mops_data.voltage

    # def contr_callback(self, data):
    #     self.u = data.data

    def collect(self):
        X = []; Y = []; steps = 0
        # flag = rospy.get_param('contr_flag')
        # u_act = self.joint_torque
        # x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
        
        while steps < self.length:
            x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            u = self.joint_torque
            rospy.sleep(0.02)
            x_new = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            X.append(np.hstack((x, u)))
            Y.append(x_new - x)
            steps+=1
        # while True:
        #     if u != self.u:
        #         x_new = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
        #         X.append(np.hstack((x, u_act)))
        #         Y.append(x_new - x)
        #         x = x_new; u = self.u; u_act = self.joint_torque
        #         steps += 1
        #         if steps == self.length: break
        # while True:
        #     flag_new = rospy.get_param('contr_flag')
        #     if flag != flag_new:
        #         x_new = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
        #         X.append(np.hstack((x, u_act)))
        #         Y.append(x_new - x)
        #         x = x_new; flag = flag_new; u_act = self.joint_torque
        #         steps += 1
        #         if steps == self.length: break

        return np.stack(X), np.stack(Y)

if __name__ == '__main__':
    rospy.init_node('data_collect')
    data = data_collect()
    rospy.spin()




