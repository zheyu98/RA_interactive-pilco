#!/home/zheyu/anaconda3/envs/RA/bin/python
import rospy
import numpy as np
import tensorflow as tf
import threading
import os
import time
import random as rand
from pynput.keyboard import Key, Listener, Controller, KeyCode
from pilco.models import PILCO
from pilco.controllers import RbfController, LinearController, CombController
from pilco.rewards import ExponentialReward
from gpflow import set_trainable
from dcsc_fpga.srv import MopsWrite, MopsWriteRequest
from dcsc_fpga.msg import MopsSensors

## human input
def on_press(key):
    global u_human
    if key == Key.right:
        u_human = -10
        # u_human = 5
        # u_human = 1
    if key == Key.left:
        u_human = 10
        # u_human = -5
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

class MopsNode(object):
    def __init__(self):
        self.mops_data = None
        self.rate = rospy.Rate(10)
        self.max_torque = 3.0

        # # Initialize request
        self.request = MopsWriteRequest()
        self.request.actuators.digital_outputs = 1
        self.request.actuators.voltage0 = 0.0  # Input voltage
        self.request.actuators.voltage1 = 0.0
        self.request.actuators.timeout = 0.1  # The timeout of the input (after 0.5 seconds the input will be set to 0)

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

    # def rollout(self, SUBS=1, T=40, random=False, controller=None):
    #     X = []; Y = []; steps = 0
    #     u_z = tf.zeros([1], dtype=tf.float64)

    #     while steps < T:
    #         x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
    #         if random: u_ps = rand.uniform(-self.max_torque,self.max_torque) + u_z
    #         else: u_ps = controller.compute_action(x[None, :])[0, :]
    #         u = u_ps 
    #         i = 0
    #         # for i in range(SUBS):
    #         self.request.actuators.voltage0 = u
    #         rospy.wait_for_service('/mops/write')
    #         x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
    #         self.write_service(self.request)
    #         while i < SUBS:
    #             i += 1
    #             self.rate.sleep()
    #         # self.request.actuators.voltage0 = u
    #         # self.write_service(self.request)
    #         # rospy.sleep(0.15)
    #         rospy.wait_for_message('/mops/read', MopsSensors, timeout=rospy.Duration(1))
    #         x_new = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
    #         if steps % 3 == 0:
    #             X.append(np.hstack((x, u)))
    #             Y.append(x_new - x)
    #         steps += 1
    #         # X.append(np.hstack((x, u)))
    #         # Y.append(x_new - x)
    #         # x = x_new
    #     return np.stack(X), np.stack(Y)
    def rollout_inter(self, SUBS=1, T=40, random=False, controller=None, last=False):
        X = []; Y = []; steps = 0
        u_z = tf.zeros([1], dtype=tf.float64)

        global u_human
        u_human = 0
        in_magni = 0.21
        u_ps = tf.zeros([1], dtype=tf.float64)

        t1=threading.Thread(target=start_key_listen)
        t1.start()
        print('You could give some corrective feedback: (Left or Right arrow)\n')
        time.sleep(2)
        print("begin")

        while steps < T:
            if steps>0 & steps%3==0:
                x_new = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
                X.append(np.hstack((x, u)))
                Y.append(x_new - x)
            x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            if random: u_ps = rand.uniform(-self.max_torque,self.max_torque) + u_z
            else: u_ps = controller.compute_action(x[None, :])[0, :] + cut(u_human, 10)*in_magni
            u = u_ps 
            ##i = 0
            # for i in range(SUBS):
            self.request.actuators.voltage0 = u
            #print(u)
            # rospy.wait_for_service('/mops/write')
            #x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            self.write_service(self.request)
            #while i < SUBS:
                #i += 1   
            # self.request.actuators.voltage0 = u
            # self.write_service(self.request)
            # rospy.sleep(0.15)
            # rospy.wait_for_message('/mops/read', MopsSensors, timeout=rospy.Duration(1))
            # X.append(np.hstack((x, u)))
            # Y.append(x_new - x)
            # x = x_new
            steps+=1
            self.rate.sleep() 

        autoin = Controller()
        autoin.press(Key.esc)
        autoin.release(Key.esc)
        autoin.press(Key.esc)
        autoin.release(Key.esc)
        autoin.press(Key.esc)
        autoin.release(Key.esc)
        t1.join()
        return np.stack(X), np.stack(Y)

    def rollout(self, SUBS=1, T=40, random=False, controller=None, last=False):
        X = []; Y = []; steps = 0
        u_z = tf.zeros([1], dtype=tf.float64)

        while steps < T:
            if steps>0 & steps%3==0:
                x_new = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
                X.append(np.hstack((x, u)))
                Y.append(x_new - x)
            x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            if random: u_ps = rand.uniform(-self.max_torque,self.max_torque) + u_z
            else: u_ps = controller.compute_action(x[None, :])[0, :]
            u = u_ps 
            ##i = 0
            # for i in range(SUBS):
            self.request.actuators.voltage0 = u
            #print(u)
            # rospy.wait_for_service('/mops/write')
            #x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            self.write_service(self.request)
            #while i < SUBS:
                #i += 1   
            # self.request.actuators.voltage0 = u
            # self.write_service(self.request)
            # rospy.sleep(0.15)
            # rospy.wait_for_message('/mops/read', MopsSensors, timeout=rospy.Duration(1))
            # X.append(np.hstack((x, u)))
            # Y.append(x_new - x)
            # x = x_new
            steps+=1
            self.rate.sleep() 
        return np.stack(X), np.stack(Y)
    
    def rollout_both(self, SUBS=1, T=40):
        X = []; Y = []; Xc = []; Yc = []; steps = 0

        global u_human
        u_human = 10
        in_magni = 0.21
        u_ps = tf.zeros([1], dtype=tf.float64)

        t1=threading.Thread(target=start_key_listen)
        t1.start()
        print('You could give some corrective feedback: (Left or Right arrow)\n')
        time.sleep(2)
        print("begin")

        while steps < T:
            if steps > 0 and steps%3 == 0: 
                x_new = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
                Xc.append(x)
                Yc.append(u)
                X.append(np.hstack((x, u)))
                Y.append(x_new - x)
            u = u_ps + cut(u_human, 10)*in_magni
            self.request.actuators.voltage0 = u
            rospy.wait_for_service('/mops/write')
            x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            self.write_service(self.request)
            steps += 1
            self.rate.sleep() 
            # x = x_new

        autoin = Controller()
        autoin.press(Key.esc)
        autoin.release(Key.esc)
        autoin.press(Key.esc)
        autoin.release(Key.esc)
        autoin.press(Key.esc)
        autoin.release(Key.esc)
        t1.join()
        return np.stack(Xc), np.stack(Yc), np.stack(X), np.stack(Y)

if __name__ == '__main__':
    SUBS=1
    bf = 30
    maxiter=30
    max_action=3.0
    target = np.array([1.0, 0.0, 0.0])
    weights = np.diag([3.0, 3.0, 0.3])
    m_init = np.reshape([-1.0, 0.0, 0.0], (1,3))
    S_init = np.diag([0.01, 0.05, 0.01])
    T = 60
    T_sim = T
    J = 2
    N = 20
    restarts = 2
    rospy.init_node('mops_node')

    pend_contr = MopsNode()

    # if input("Give demonstration or not (y/n)\n") == 'y':
    Xc, Yc, X, Y = pend_contr.rollout_both(SUBS=SUBS, T=30)
    time.sleep(3)
    # else:
    #     if os.path.exists('./examples/human/training_data_X.npy') & os.path.exists('./examples/human/training_data_Y.npy') \
    #     & os.path.exists('./examples/human/training_data_Yc.npy') & os.path.exists('./examples/human/training_data_Xc.npy'):
    #         Xc = np.load('./examples/human/training_data_Xc.npy')
    #         Yc = np.load('./examples/human/training_data_Yc.npy')
    #         X = np.load('./examples/human/training_data_X.npy')
    #         Y = np.load('./examples/human/training_data_Y.npy')
    #     else:
    #         raise Exception('Please give demonstration')

    # np.save('./examples/human/training_data_X.npy', X)
    # np.save('./examples/human/training_data_Y.npy', Y)
    # np.save('./examples/human/training_data_Xc.npy', Xc)
    # np.save('./examples/human/training_data_Yc.npy', Yc)

    data_c = [Xc,Yc]
    state_dim = Y.shape[1]
    control_dim = X.shape[1] - state_dim

    R = ExponentialReward(state_dim=state_dim, t=target, W=weights)
    controller = CombController(data_c, max_action=max_action)
    pilco = PILCO((X, Y), controller=controller, horizon=40, reward=R, m_init=m_init, S_init=S_init)
    print("Start PILCO optimization!")

    # start = time.time()
    for i in range(1,J):
        X_, Y_ = pend_contr.rollout(SUBS=SUBS, random=False, T=30, controller=pilco)
        X = np.vstack((X, X_))
        Y = np.vstack((Y, Y_))
        time.sleep(3)
    pilco.mgpr.set_data((X, Y))

    # for numerical stability, we can set the likelihood variance parameters of the GP models
    for model in pilco.mgpr.models:
        model.likelihood.variance.assign(0.01)
        model.kernel.variance.assign(0.5)
        model.kernel.lengthscales.assign([0.2,0.2,1.0, 1.0])
        set_trainable(model.likelihood.variance, False)
        set_trainable(model.kernel.lengthscales, True)
        set_trainable(model.kernel.variance, True)

    r_new = np.zeros((T, 1))
    # re_p = []; count = []; re_pn = []
    for rollouts in range(N):
        print("**** ITERATION no", rollouts, " ****")
        pilco.optimize_models(maxiter=maxiter, restarts=2)
        pilco.optimize_policy(maxiter=maxiter, restarts=2)

        X_new, Y_new = pend_contr.rollout_inter(SUBS=SUBS, random=False, T=T, controller=pilco)

        # Since we had decide on the various parameters of the reward function
        # we might want to verify that it behaves as expected by inspection
        for i in range(len(X_new)):
                r_new[:, 0] = R.compute_reward(X_new[i,None,:-1], 0.001 * np.eye(state_dim))[0]
        total_r = sum(r_new)
        _, _, r = pilco.predict(X_new[0,None,:-1], 0.001 * S_init, T)
        print("Total ", total_r, " Predicted: ", r)
        # re_p.append(total_r)
        # re_pn.append(r)
        # count.append(rollouts)

        # Update dataset
        X = np.vstack((X, X_new)); Y = np.vstack((Y, Y_new))
        pilco.mgpr.set_data((X, Y))

    # end = time.time()
    # print("Time cost of this training process is ", end-start)

