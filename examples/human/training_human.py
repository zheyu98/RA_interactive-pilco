import numpy as np
import gym
from pilco.controllers import HumanController
from pilco.rewards import ExponentialReward
import tensorflow as tf
from utils_human import rollout, policy
from gpflow import set_trainable
import matplotlib.pyplot as plt
import os
np.random.seed(0)

class myPendulum():
    def __init__(self):
        self.env = gym.make('Pendulum-v0').env
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space
        ##
        self.l = 10
        self.m = 10

    def step(self, action):
        return self.env.step(action)

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

# def check(X, Y, R, X_new, Y_new, R_new, ep):
#     len = X.shape[0]; len_new = X_new.shape[0]; ind = []
#     for i in range(len_new):
#         for j in range(len):
#             err = abs(X_new[i,:]-X[j,:]) 
#             if np.all(err < ep) and ((X_new[i,-1]<0) == (X[j,-1]<0)):
#                 if R[j] < R_new[i]: X[j,:] = X_new[i,:]; Y[j,:] = Y_new[i,:]; R[j] = R_new[i]
#                 #     X_new = np.delete(X_new,i,axis=0); Y_new = np.delete(Y_new,i,axis=0); R_new = np.delete(R_new,i)
#                 # else: X_new = np.delete(X_new,i,axis=0); Y_new = np.delete(Y_new,i,axis=0); R_new = np.delete(R_new,i)
#                 ind.append(i)
#     X_new = np.delete(X_new,ind,axis=0); Y_new = np.delete(Y_new,ind,axis=0); R_new = np.delete(R_new,ind)
#     X = np.vstack((X, X_new)); Y = np.vstack((Y, Y_new)); R = np.append(R, R_new)
#     return X, Y, R

def check(X, X_new, Y, Y_new, error, sigma, step, controller):
    diff = controller.model.K(X, X_new)
    vars = []; ind_up = []; ind_agg = []
    for model in controller.model.models:
        vars.append(model.kernel.variance)
    vars = np.stack(vars)
    norm_diff = diff/vars[:, np.newaxis, np.newaxis]
    for i in range(X_new.shape[0]):
        if tf.reduce_any(norm_diff[:,:,i] > sigma): ind_up.append(i)
        else: ind_agg.append(i)
    # aggregate
    X_a = X_new[ind_agg,:]
    diff_a = controller.model.K(X, X_a) / vars[:, np.newaxis, np.newaxis]
    error_a = np.transpose(error[ind_agg, :])
    i1 = np.matmul(diff_a, error_a[:,:,None])
    i2 = np.transpose(np.squeeze(i1,axis=2))
    Y = Y + i2 * step
    # add
    X = np.vstack((X, X_new[ind_agg,:]))
    Y = np.vstack((Y, Y_new[ind_agg,:]))    
    return X, Y    


if __name__=='__main__':
    SUBS=3
    bf = 30
    maxiter=50
    max_action=2.0
    target = np.array([1.0, 0.0, 0.0])
    weights = np.diag([2.0, 2.0, 0.3])
    m_init = np.reshape([-1.0, 0.0, 0.0], (1,3))
    S_init = np.diag([0.01, 0.05, 0.01])
    T = 40
    T_sim = T
    J = 3
    N = 6
    restarts = 2
    control_dim = 1

    env = myPendulum()

    # Collect data for human controller
    j1 = input("Load database or not? (y/n)\n")
    if j1 == 'y':
        if os.path.exists('./examples/training_data_Xc.npy') & os.path.exists('./examples/training_data_Yc.npy'):
            X = np.load('./examples/training_data_Xc.npy')
            Y = np.load('./examples/training_data_Yc.npy')
        else:
            print("The database doesn't exist\n")
            X, Y, _, _, _ = rollout(env, None, timesteps=T, control_dim=control_dim, SUBS=SUBS, render=True)
    else:
        X, Y, _, _, _ = rollout(env, None, timesteps=T, control_dim=control_dim, SUBS=SUBS, render=True)
        # for i in range(1,3):
        #     X_, Y_, _, _ = rollout(env, None, timesteps=T, random=True, SUBS=SUBS, render=True)
        #     X = np.vstack((X, X_))
        #     Y = np.vstack((Y, Y_))
    
    X_hyper = X[:T,:]
    Y_hyper = Y[:T,:]
    state_dim = X.shape[1]

    controller = HumanController((X_hyper,Y_hyper), state_dim=state_dim, max_action=max_action)
    # R = ExponentialReward(state_dim=state_dim, t=target, W=weights)

    # Optimize the hyper-paramters
    for model in controller.model.models:
        model.likelihood.variance.assign(0.001)
        set_trainable(model.likelihood.variance, False)

    controller.model.set_data((X_hyper, Y_hyper))
    controller.optimize_models(maxiter=maxiter, restarts=restarts)
  
    # r_new = np.zeros((T, 1))
    j2 = input("Continue to collect data or not? (y/n)\n")
    if j2 == 'y':
        while True:
            X_new, Y_new, error, r, _ = rollout(env, controller, timesteps=T, control_dim=control_dim, p_use=True, SUBS=SUBS, render=True)
            print("Total reward of this turn", r)   

            # Update dataset
            # ep = [0.3, 0.3, 0.1]
            # X, Y, R = check(X, Y, R, X_new, Y_new, R_new, ep)
            sigma = 0.7; step = 0.3
            X, Y = check(X, X_new, Y, Y_new, error, sigma, step, controller)
            controller.model.set_data((X, Y))
            
            judge = input('Continue to collect data or not? (y/n)\n')
            if judge == 'n': 
                np.save('./examples/training_data_X.npy', X)
                np.save('./examples/training_data_Y.npy', Y)
                break
    else:
        controller.model.set_data((X, Y))

    # Demonstration
    print('Evaluate the performance of the human controller\n')
    X_new, Y_new, R_new, r, _ = rollout(env, controller, timesteps=T_sim, control_dim=control_dim, p_use=True, demon=True, SUBS=SUBS, render=True)
    print("Total reward of this turn", r)
