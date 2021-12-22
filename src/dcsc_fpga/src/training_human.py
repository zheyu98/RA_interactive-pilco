#!/home/zheyu/anaconda3/envs/RA/bin/python
import numpy as np
import gym
import rospy
from gpflow import Parameter, config
from pilco.controllers import HumanController
from pilco.rewards import ExponentialReward
import tensorflow as tf
import threading
import time
import random as rand
from pynput.keyboard import Key, Listener, Controller, KeyCode
from gpflow import set_trainable
from dcsc_fpga.srv import MopsWrite, MopsWriteRequest
from dcsc_fpga.msg import MopsSensors
import matplotlib.pyplot as plt
import os
np.random.seed(0)
float_type = config.default_float()

## human input
def on_press(key):
    global u_human
    if key == Key.right:
        # u_human = 8
        u_human = -10
        # u_human = 1
    if key == Key.left:
        # u_human = -8
        u_human = 10
        # u_human = 0
    if key == Key.down:
        u_human = 0
    if key == KeyCode(char = 'd'):
        if u_human <0:
            u_human += -1
        else:
            u_human = -1
    if key == KeyCode(char = 'a'):
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

class MopsNode(object):
    def __init__(self):
        self.mops_data = None
        self.rate = rospy.Rate(40)
        self.max_torque = 3.0

        # # Initialize request
        self.request = MopsWriteRequest()
        self.request.actuators.digital_outputs = 1
        self.request.actuators.voltage0 = 0.0  # Input voltage
        self.request.actuators.voltage1 = 0.0
        self.request.actuators.timeout = 0.5  # The timeout of the input (after 0.5 seconds the input will be set to 0)

        # Subscriber and service
        rospy.Subscriber('/mops/read', MopsSensors, self.read_callback)
        rospy.wait_for_message('/mops/read', MopsSensors, timeout=rospy.Duration(1))

        self.write_service = rospy.ServiceProxy('/mops/write', MopsWrite)

    def read_callback(self, msg):
        self.mops_data = msg
        self.joint_angle = self.mops_data.position0
        self.joint_velocity = self.mops_data.speed

    def run(self, controller):
        while not rospy.is_shutdown():
            x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            u = controller.compute_action(x[None, :])[0, :]
            self.write_service(u)
            self.rate.sleep()

    def rollout(self, SUBS=1, T=40, random=False, controller=None, last=False):
        X = []; Y = []; steps = 0
        u_z = tf.zeros([1], dtype=tf.float64)

        while steps < T:
            x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            if random: u_ps = rand.uniform(-self.max_torque,self.max_torque) + u_z
            else: u_ps = controller.compute_action(x[None, :])[0, :]
            u = u_ps 
            i = 0
            # for i in range(SUBS):
            self.request.actuators.voltage0 = u
            print(u)
            # rospy.wait_for_service('/mops/write')
            x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            self.write_service(self.request)
            while i < SUBS:
                i += 1
                self.rate.sleep()
            # self.request.actuators.voltage0 = u
            # self.write_service(self.request)
            # rospy.sleep(0.15)
            # rospy.wait_for_message('/mops/read', MopsSensors, timeout=rospy.Duration(1))
            x_new = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            if last:
                X.append(np.hstack((x, u)))
                Y.append(x_new - x)
            else:
                if steps % 3 == 0:
                    X.append(np.hstack((x, u)))
                    Y.append(x_new - x)
            steps += 1
            # X.append(np.hstack((x, u)))
            # Y.append(x_new - x)
            # x = x_new
        return np.stack(X), np.stack(Y)
    
    def rollout_ilosa(self, data, controller, T, control_dim=1, SUBS=1):
        X_new = []
        X_base = data[0]; Y_base = data[1]

        global u_human
        u_human = 0
        in_magni = 0.2

        t1=threading.Thread(target=start_key_listen)
        t1.start()
        print('You could give some corrective feedback: (Left or Right arrow)\n')

        steps = 0
        while steps < T:
            x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            uh = controller.compute_action(x[None, :], tf.zeros([controller.state_dim, controller.state_dim], float_type))[0]
            u = uh[0,:]+ cut(u_human, 10)*in_magni
            self.request.actuators.voltage0 = u
            x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            self.write_service(self.request)
            i = 0
            while i < SUBS:
                i += 1
                self.rate.sleep()
            X = x
            Y = u
            X_new.append(x)
            human = tf.zeros([control_dim], dtype=tf.float64) + cut(u_human, 10)*in_magni
            if u_human != 0:
                X_base, Y_base = check_ilosa(X_base, X, Y_base, Y, human, controller)
                controller.model.set_data((X_base, Y_base))
            steps += 1
            u_human = 0

        autoin = Controller()
        autoin.press(Key.esc)
        autoin.release(Key.esc)
        t1.join()
        return controller, np.stack(X_new), [X_base,Y_base] 

    def rollout_both(self, SUBS=1, T=40):
        X = []; Y = []; Xc = []; Yc = []; steps = 0

        global u_human
        u_human = 10
        in_magni = 0.2
        u_ps = tf.zeros([1], dtype=tf.float64)

        t1=threading.Thread(target=start_key_listen)
        t1.start()
        print('You could give some corrective feedback: (Left or Right arrow)\n')
        time.sleep(2)
        print("begin")

        while steps < T:
            u = u_ps + cut(u_human, 10)*in_magni
            self.request.actuators.voltage0 = u
            rospy.wait_for_service('/mops/write')
            x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            self.write_service(self.request)
            i = 0
            while i < SUBS:                
                i += 1
                self.rate.sleep()            
            x_new = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)

            Xc.append(x)
            Yc.append(u)
            X.append(np.hstack((x, u)))
            Y.append(x_new - x)
            steps += 1
            if steps % 5 == 0: u_human = 0

        autoin = Controller()
        autoin.press(Key.esc)
        autoin.release(Key.esc)
        autoin.press(Key.esc)
        autoin.release(Key.esc)
        autoin.press(Key.esc)
        autoin.release(Key.esc)
        t1.join()
        return np.stack(Xc), np.stack(Yc), np.stack(X), np.stack(Y)

if __name__=='__main__':
    SUBS=3
    bf = 30
    maxiter=50
    max_action=2.0
    target = np.array([1.0, 0.0, 0.0])
    weights = np.diag([2.0, 2.0, 0.3])
    m_init = np.reshape([-1.0, 0.0, 0.0], (1,3))
    S_init = np.diag([0.01, 0.05, 0.01])
    T = 200
    T_sim = T
    J = 3
    N = 6
    restarts = 2
    control_dim = 1

    rospy.init_node('human_node')

    pend_contr = MopsNode()

    # Collect data for human controller
    X, Y, _, _ = pend_contr.rollout_both(SUBS=SUBS, T=T)
    # X = np.load("./human_X.npy")
    # Y = np.load("./human_Y.npy")

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
        model.kernel.variance.assign(0.68)
        model.kernel.lengthscales.assign([0.2,0.2,0.3])
        set_trainable(model.likelihood.variance, False)
        set_trainable(model.kernel.lengthscales, False)
        set_trainable(model.kernel.variance, False)

    controller.optimize_models(maxiter=maxiter, restarts=restarts, op=False)

    r_new = np.zeros((T, 1))
    q = 0
    while q < 10:
        # ILOSA
        controller, X_new, data = pend_contr.rollout_ilosa(data, controller, T=T, control_dim=control_dim, SUBS=SUBS)
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
    X_new, _ = pend_contr.rollout(SUBS=SUBS, T=T, random=False, controller=controller, last=True)
    for i in range(len(X_new)):
        r_new[:, 0] = R.compute_reward(X_new[i,None,:], 0.001 * np.eye(state_dim))[0]
    total_r = sum(r_new)
    print("Total reward of this turn", total_r) 
