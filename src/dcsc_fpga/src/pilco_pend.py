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

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class myPendulum():
    def __init__(self):
        self.env = gym.make('Pendulum-v1').env
        self.action_space = gym.spaces.Box(
            low=-self.env.max_torque, high=self.env.max_torque, shape=(1,), dtype=np.float64
        )
        self.observation_space = self.env.observation_space

    def step(self, u):
        th, thdot = self.env.state  # th := theta

        g = self.env.g
        m = self.env.m
        l = self.env.l
        dt = self.env.dt

        u = np.clip(u, -self.env.max_torque, self.env.max_torque)[0]
        self.env.last_u = u  # for rendering
        costs = angle_normalize(th) ** 2 + 0.1 * thdot ** 2 + 0.001 * (u ** 2)

        newthdot = thdot + (3 * g / (2 * l) * np.sin(th) + 3.0 / (m * l ** 2) * u) * dt
        newthdot = np.clip(newthdot, -self.env.max_speed, self.env.max_speed)
        newth = th + newthdot * dt

        self.env.state = np.array([newth, newthdot])
        return self.get_obs(), -costs, False, {}

    def reset(self):
        high = np.array([np.pi, 1.0])
        self.env.state = np.random.uniform(low=-high, high=high)
        self.env.state = np.random.uniform(low=0.0, high=0.01*high) # only difference
        self.env.state[0] += -np.pi
        self.env.last_u = None
        return self.get_obs()
    
    def get_obs(self):
        theta, thetadot = self.env.state
        return np.array([np.cos(theta), np.sin(theta), thetadot], dtype=np.float64)

    def render(self):
        self.env.render()

def angle_normalize(x):
    return ((x + np.pi) % (2 * np.pi)) - np.pi

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

class MopsNode(object):
    def __init__(self):
        self.mops_data = None
        self.rate = rospy.Rate(20)
        self.max_torque = 1.5
        self.env = myPendulum()

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
        self.joint_torque = self.mops_data.voltage

    def run(self, controller):
        while not rospy.is_shutdown():
            x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            u = controller.compute_action(x[None, :])[0, :]
            self.write_service(u)
            self.rate.sleep()

    # def rollout(self, X_base=None, SUBS=1, T=40, random=False, controller=None, last=False, first=False):
    #     X = []; Y = []; steps = 0
    #     x = self.env.reset()
    #     # u_z = tf.zeros([1], dtype=tf.float64)

    #     while steps < T:
    #         self.env.render()
    #         if steps>0:
    #             for i in range(SUBS):
    #                 x_new, _, _, _ = self.env.step(u)
    #                 self.env.render()
    #             if first or last:
    #                 X.append(np.hstack((x, u)))
    #                 Y.append(x_new - x)
    #             else:
    #                 add= check(X_base, np.hstack((x, u)), controller.mgpr)
    #                 if steps == 1 or add:
    #                     X.append(np.hstack((x, u)))
    #                     Y.append(x_new - x)
    #             # X.append(np.hstack((x, u)))
    #             # Y.append(x_new - x)
    #             x = x_new
    #         if random: u_ps = self.env.action_space.sample()
    #         else: u_ps = controller.compute_action(x[None, :])[0, :]
    #         u = u_ps

    #         #while i < SUBS:
    #             #i += 1   
    #         # self.request.actuators.voltage0 = u
    #         # self.write_service(self.request)
    #         # rospy.sleep(0.15)
    #         # rospy.wait_for_message('/mops/read', MopsSensors, timeout=rospy.Duration(1))
    #         # X.append(np.hstack((x, u)))
    #         # Y.append(x_new - x)
    #         # x = x_new
    #         steps+=1
    #         self.rate.sleep() 
    #     return np.stack(X), np.stack(Y)

    def rollout(self, X_base=None, SUBS=1, T=40, random=False, controller=None, last=False, first=False):
        X = []; Y = []; steps = 0
        u_z = tf.zeros([1], dtype=tf.float64)

        while steps < T:
            if steps>0:
                x_new = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
                # if first or last:
                #     X.append(np.hstack((x, u)))
                #     Y.append(x_new - x)
                # else:
                #     add= check(X_base, np.hstack((x, u)), controller.mgpr)
                #     if steps == 1 or add:
                #         X.append(np.hstack((x, u)))
                #         Y.append(x_new - x)
                X.append(np.hstack((x, u)))
                Y.append(x_new - x)
            x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            alpha = 2
            start = time.time()
            if random: u_ps = rand.uniform(-self.max_torque,self.max_torque) + np.sin(2*np.pi*steps/T*alpha)
            # alpha = 2
            # if random: u_ps = self.max_torque * np.sin(2*np.pi*steps/T*alpha)
            else: u_ps = controller.compute_final_action(x[None, :])[0, :]
            u = u_ps 

            self.request.actuators.voltage0 = u
            #print(u)
            # rospy.wait_for_service('/mops/write')
            
            self.write_service(self.request)
            end = time.time()
            print('Time cost: ', end-start)
            # u_act = self.joint_torque
            x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
            steps+=1
            rospy.sleep(0.05)
        return np.stack(X), np.stack(Y)


    # def rollout(self, X_base=None, SUBS=1, T=40, random=False, controller=None, last=False, first=False):
    #     X = []; Y = []; steps = 0
    #     u_z = tf.zeros([1], dtype=tf.float64)

    #     while steps < T:
    #         if steps>0:
    #             x_new = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
    #             if first or last:
    #                 X.append(np.hstack((x, u)))
    #                 Y.append(x_new - x)
    #             else:
    #                 add= check(X_base, np.hstack((x, u)), controller.mgpr)
    #                 if steps == 1 or add:
    #                     X.append(np.hstack((x, u)))
    #                     Y.append(x_new - x)
    #             # X.append(np.hstack((x, u)))
    #             # Y.append(x_new - x)
    #         x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
    #         if random: u_ps = rand.uniform(-self.max_torque,self.max_torque) + u_z
    #         else: u_ps = controller.compute_action(x[None, :])[0, :]
    #         u = u_ps 

    #         self.request.actuators.voltage0 = u
    #         #print(u)
    #         # rospy.wait_for_service('/mops/write')
    #         x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
    #         self.write_service(self.request)
    #         steps+=1
    #         self.rate.sleep() 
    #     return np.stack(X), np.stack(Y)

    # def rollout(self, X_base=None, Y_base=None, SUBS=1, T=40, random=False, controller=None, last=False, first=False):
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
    #         # rospy.wait_for_service('/mops/write')
    #         x = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
    #         self.write_service(self.request)
    #         while i < SUBS:
    #             i += 1
    #             self.rate.sleep()
    #         # self.request.actuators.voltage0 = u
    #         # self.write_service(self.request)
    #         # rospy.sleep(0.15)
    #         # rospy.wait_for_message('/mops/read', MopsSensors, timeout=rospy.Duration(1))
    #         x_new = np.array([np.cos(self.joint_angle), np.sin(self.joint_angle), self.joint_velocity], dtype=np.float64)
    #         if first or last:
    #             X.append(np.hstack((x, u)))
    #             Y.append(x_new - x)
    #         else:
    #             add= check(X_base, np.hstack((x, u)), controller.mgpr)
    #             if steps == 0 or add:
    #                 X.append(np.hstack((x, u)))
    #                 Y.append(x_new - x)
    #         steps += 1
    #         # X.append(np.hstack((x, u)))
    #         # Y.append(x_new - x)
    #     return np.stack(X), np.stack(Y)

def bounded_lengthscale(low, high, lengthscale):
    """Make lengthscale tfp Parameter with optimization bounds."""
    sigmoid = tfb.Sigmoid(low, high)
    parameter = gpflow.Parameter(lengthscale, transform=sigmoid, dtype='float64')
    return parameter

if __name__ == '__main__':
    SUBS=3
    bf = 30
    maxiter=50
    max_action=1.5
    target = np.array([1.0, 0.0, 0.0])
    weights = np.diag([2.0, 2.0, 0.3])
    m_init = np.reshape([-1.0, 0.0, 0.0], (1,3))
    S_init = np.diag([0.05, 0.05, 0.01])
    T = 40
    T_sim = 40
    J = 2
    N = 20
    restarts = 2
    rospy.init_node('mops_node')

    pend_contr = MopsNode()

    # if input("Give demonstration or not (y/n)\n") == 'y':
    #     Xc, Yc, X, Y = pend_contr.rollout_both(SUBS=SUBS, T=T)
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

    X, Y = pend_contr.rollout(SUBS=SUBS, random=True, T=T, controller=None, first=True)
    # print(X); print(Y)
    time.sleep(3)
    # start = time.time()
    for i in range(1,J):
        X_, Y_ = pend_contr.rollout(X, SUBS=SUBS, random=True, T=T, controller=None, first=True)
        X = np.vstack((X, X_))
        Y = np.vstack((Y, Y_))
        time.sleep(3)

    state_dim = Y.shape[1]
    control_dim = X.shape[1] - state_dim

    controller = RbfController(state_dim=state_dim, control_dim=control_dim, num_basis_functions=bf, max_action=max_action)
    R = ExponentialReward(state_dim=state_dim, t=target, W=weights)

    pilco = PILCO((X, Y), controller=controller, horizon=40, reward=R, m_init=m_init, S_init=S_init)
    # pilco = PILCO(X, Y, controller=controller, horizon=40, reward=R)

    lens = np.array([[2.834, 2.101, 7.677, 19.142], [2.061, 2.475, 6.971, 17.429], [3.766, 3.842, 18.615, 15.778]])
    var = np.array([0.873, 0.66, 7.81])
    # for numerical stability, we can set the likelihood variance parameters of the GP models
    j = 0
    for model in pilco.mgpr.models:
        model.likelihood.variance.assign(0.001)
        # model.kernel.lengthscales.assign([0.2, 0.2, 1.0, 1.0])
        # model.kernel.lengthscales.assign(lens[j,:])
        # model.kernel.variance.assign(0.5) 
        # model.kernel.variance.assign(var[j])       
        # set_trainable(model.kernel.lengthscales, False)
        # set_trainable(model.kernel.variance, False)
        set_trainable(model.likelihood.variance, False)
        # if j == 2: 
        #     set_trainable(model.likelihood.variance, False)
        #     model.likelihood.variance.assign(0.001)
        j += 1

    r_new = np.zeros((T, 1))
    # re_p = []; count = []; re_pn = []
    for rollouts in range(N):
        print("**** ITERATION no", rollouts, " ****")
        pilco.optimize_models(maxiter=maxiter, restarts=2)
        pilco.optimize_policy(maxiter=maxiter, restarts=2)
        # pilco.optimize()

        last = False
        if rollouts==N-1: last = True

        X_new, Y_new = pend_contr.rollout(X, SUBS=SUBS, random=False, T=T_sim, controller=pilco, last=last)

        # Since we had decide on the various parameters of the reward function
        # we might want to verify that it behaves as expected by inspection
        for i in range(len(X_new)):
                r_new[:, 0] = R.compute_reward(X_new[i,None,:-1], 0.001 * np.eye(state_dim))[0]
        total_r = sum(r_new)
        _, _, r = pilco.predict(X_new[0,None,:-1], 0.001 * S_init, T_sim)
        print("Total ", total_r, " Predicted: ", r)
        # re_p.append(total_r)
        # re_pn.append(r)
        # count.append(rollouts)

        # Update dataset
        X = np.vstack((X, X_new)); Y = np.vstack((Y, Y_new))
        pilco.mgpr.set_data((X, Y))
        # pilco.mgpr.set_XY(X, Y)
        print(X.shape)

    # end = time.time()
    # print("Time cost of this training process is ", end-start)

    for i,m in enumerate(pilco.mgpr.models):
        y_pred_test, var_pred_test = m.predict_y(X_new)
        plt.plot(range(len(y_pred_test)), y_pred_test, Y_new[:,i])
        plt.fill_between(range(len(y_pred_test)),
                        y_pred_test[:,0] - 2*np.sqrt(var_pred_test[:, 0]), 
                        y_pred_test[:,0] + 2*np.sqrt(var_pred_test[:, 0]), alpha=0.3)
        plt.show()
    
    np.shape(var_pred_test)

    # np.save("./base_X", X)
    # np.save("./base_Y", Y)

    m_p = np.zeros((T_sim, state_dim))
    S_p = np.zeros((T_sim, state_dim, state_dim))

    m_p[0,:] = m_init
    S_p[0, :, :] = S_init

    for h in range(1, T_sim):
        m_p[h,:], S_p[h,:,:] = pilco.propagate(m_p[h-1, None, :], S_p[h-1,:,:])
        

    for i in range(state_dim):    
        plt.plot(range(T_sim-1), m_p[0:T_sim-1, i], X_new[1:T_sim, i]) # can't use Y_new because it stores differences (Dx)
        plt.fill_between(range(T_sim-1),
                        m_p[0:T_sim-1, i] - 2*np.sqrt(S_p[0:T_sim-1, i, i]),
                        m_p[0:T_sim-1, i] + 2*np.sqrt(S_p[0:T_sim-1, i, i]), alpha=0.2)
        plt.show()

