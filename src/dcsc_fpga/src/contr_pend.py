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
from std_msgs.msg import Float64
from dcsc_fpga.srv import MopsWrite, MopsWriteRequest
from dcsc_fpga.srv import Contr, ContrRequest
from dcsc_fpga.msg import MopsSensors
import dill 
import pickle

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class contr_pend(object):
    def __init__(self):
        self.mops_data = None
        self.rate = rospy.Rate(6)

        # # Initialize request
        self.request = MopsWriteRequest()
        self.request.actuators.digital_outputs = 1
        self.request.actuators.voltage0 = 0.0  # Input voltage
        self.request.actuators.voltage1 = 0.0
        self.request.actuators.timeout = 0.5  # The timeout of the input (after 0.5 seconds the input will be set to 0)

        self.request2 = ContrRequest()
        self.request2.angle = None
        self.request2.velocity = None

        # Subscriber and service
        # self.pub = rospy.Publisher('/pilco/contr_sig', Float64, queue_size=1)
        rospy.Subscriber('/mops/read', MopsSensors, self.read_callback)
        rospy.wait_for_message('/mops/read', MopsSensors, timeout=rospy.Duration(1))

        self.write_service = rospy.ServiceProxy('/mops/write', MopsWrite)
        # rospy.wait_for_service('/pilco/controll') 
        self.contr_service = rospy.ServiceProxy('/pilco/controll', Contr)

    def read_callback(self, msg):
        self.mops_data = msg
        self.joint_angle = self.mops_data.position0
        self.joint_velocity = self.mops_data.speed

    def random_contr(self, max_torque=1.0, step=10):
        u = rand.uniform(-max_torque,max_torque)
        alpha = 2
        u_t = u
        if u > 0.05: u_t = 1.5
        if u < -0.05: u_t = -1.5
        # u = max_torque * np.sin(2*np.pi*step/40*alpha)
        self.request.actuators.voltage0 = u_t
        # rospy.wait_for_service('/mops/write')        
        self.write_service(self.request)
        rospy.set_param('contr_flag', step)
        # self.pub.publish(u)

    # def controll(self, step=10):
    #     self.request2.angle = self.joint_angle
    #     self.request2.velocity = self.joint_velocity
    #     # rospy.wait_for_service('/pilco/controll') 
    #     response = self.contr_service(self.request2)
    #     u = response.action

    #     self.request.actuators.voltage0 = u
    #     # rospy.wait_for_service('/mops/write')        
    #     self.write_service(self.request)
    #     rospy.set_param('contr_flag', step)

    def controll(self, step, controller):
        u = controller.controll(self.joint_angle, self.joint_velocity)
        u_t = u
        if u > 0.05: u_t = 1.5
        if u < -0.05: u_t = -1.5
        self.request.actuators.voltage0 = u_t
        # rospy.wait_for_service('/mops/write')        
        self.write_service(self.request)
        rospy.set_param('contr_flag', step)

if __name__ == '__main__':
    rospy.init_node('contr_pend')
    pend_contr = contr_pend()
    max_action = 1.5
    rate = rospy.Rate(20)
    
    while not rospy.is_shutdown():
        random = rospy.get_param('rand_controll')
        compute = rospy.get_param('pilco_controll')
        if random: 
            step = 1
            while True:
                start = time.time()
                pend_contr.random_contr(max_torque=max_action, step=step)
                stop = rospy.get_param('stop')
                if stop: break
                end = time.time()
                print('Time cost: ', end-start)
                step += 1
                rate.sleep()
                
        if compute:
            with open("./pilco_model.pkl", "rb") as f:
                pilco = dill.load(f)
            step = 1
            while True:
                start = time.time()
                pend_contr.controll(step=step, controller=pilco)
                stop = rospy.get_param('stop')
                if stop: break
                end = time.time()
                print('Time cost: ', end-start)
                step += 1
                rate.sleep()
                
        
    


