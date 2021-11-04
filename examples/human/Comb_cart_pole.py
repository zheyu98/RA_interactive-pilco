import numpy as np
import gym
from gym import spaces,logger
from gym.utils import seeding
import math
import gpflow
import os
from pilco.models import PILCO
from pilco.controllers import RbfController, LinearController, CombController
from pilco.rewards import ExponentialReward
import tensorflow as tf
from utils import rollout, policy
from utils_human import rollout_both
from gpflow import set_trainable
np.random.seed(0)

# Introduces a simple wrapper for the gym environment
# Reduces dimensions, avoids non-smooth parts of the state space that we can't model
# Uses a different number of timesteps for planning and testing
# Introduces priors

class mycartpole():
    def __init__(self):
        self.env = gym.make('CartPole-v1')
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.total_mass = self.masspole + self.masscart
        self.length = 0.5  # actually half the pole's length
        self.polemass_length = self.masspole * self.length
        self.force_mag = 10.0
        self.tau = 0.02  # seconds between state updates
        self.kinematics_integrator = "euler"
        # self.theta_threshold_radians = 12 * 2 * math.pi / 360
        self.theta_threshold_radians = math.pi / 2
        self.x_threshold = 2.4
        high = np.array(
            [
                self.x_threshold * 2,
                np.finfo(np.float64).max,
                self.theta_threshold_radians * 2,
                np.finfo(np.float64).max,
            ],
            dtype=np.float64,
        )
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(-high, high, dtype=np.float64)
        self.seed()
        self.viewer = None
        self.state = None
        self.steps_beyond_done = None
    
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg

        x, x_dot, theta, theta_dot = self.state
        force = self.force_mag if action == 1 else -self.force_mag
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        temp = (
            force + self.polemass_length * theta_dot ** 2 * sintheta
        ) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (
            self.length * (4.0 / 3.0 - self.masspole * costheta ** 2 / self.total_mass)
        )
        xacc = temp - self.polemass_length * thetaacc * costheta / self.total_mass

        if self.kinematics_integrator == "euler":
            x = x + self.tau * x_dot
            x_dot = x_dot + self.tau * xacc
            theta = theta + self.tau * theta_dot
            theta_dot = theta_dot + self.tau * thetaacc
        else:  # semi-implicit euler
            x_dot = x_dot + self.tau * xacc
            x = x + self.tau * x_dot
            theta_dot = theta_dot + self.tau * thetaacc
            theta = theta + self.tau * theta_dot

        state = (x, x_dot, theta, theta_dot)

        done = bool(
            x < -self.x_threshold
            or x > self.x_threshold
            or theta < -self.theta_threshold_radians
            or theta > self.theta_threshold_radians
        )

        if not done:
            self.state = state
            reward = 1.0
        else: 
            self.state = state
            reward = 0.0
        # elif self.steps_beyond_done is None:
        #     # Pole just fell!
        #     self.steps_beyond_done = 0
        #     reward = 1.0
        # else:
        #     if self.steps_beyond_done == 0:
        #         logger.warn(
        #             "You are calling 'step()' even though this "
        #             "environment has already returned done = True. You "
        #             "should always call 'reset()' once you receive 'done = "
        #             "True' -- any further steps are undefined behavior."
        #         )
        #     self.steps_beyond_done += 1
        #     reward = 0.0
        return np.array(self.state, dtype=np.float64), reward, done, {}

    def reset(self):
        self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        self.steps_beyond_done = None
        return np.array(self.state, dtype=np.float64)

    def render(self, mode="human"):
        screen_width = 600
        screen_height = 400

        world_width = self.x_threshold * 2
        scale = screen_width / world_width
        carty = 100  # TOP OF CART
        polewidth = 10.0
        polelen = scale * (2 * self.length)
        cartwidth = 50.0
        cartheight = 30.0

        if self.viewer is None:
            from gym.envs.classic_control import rendering

            self.viewer = rendering.Viewer(screen_width, screen_height)
            l, r, t, b = -cartwidth / 2, cartwidth / 2, cartheight / 2, -cartheight / 2
            axleoffset = cartheight / 4.0
            cart = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            self.carttrans = rendering.Transform()
            cart.add_attr(self.carttrans)
            self.viewer.add_geom(cart)
            l, r, t, b = (
                -polewidth / 2,
                polewidth / 2,
                polelen - polewidth / 2,
                -polewidth / 2,
            )
            pole = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            pole.set_color(0.8, 0.6, 0.4)
            self.poletrans = rendering.Transform(translation=(0, axleoffset))
            pole.add_attr(self.poletrans)
            pole.add_attr(self.carttrans)
            self.viewer.add_geom(pole)
            self.axle = rendering.make_circle(polewidth / 2)
            self.axle.add_attr(self.poletrans)
            self.axle.add_attr(self.carttrans)
            self.axle.set_color(0.5, 0.5, 0.8)
            self.viewer.add_geom(self.axle)
            self.track = rendering.Line((0, carty), (screen_width, carty))
            self.track.set_color(0, 0, 0)
            self.viewer.add_geom(self.track)

            self._pole_geom = pole

        if self.state is None:
            return None

        # Edit the pole polygon vertex
        pole = self._pole_geom
        l, r, t, b = (
            -polewidth / 2,
            polewidth / 2,
            polelen - polewidth / 2,
            -polewidth / 2,
        )
        pole.v = [(l, b), (l, t), (r, t), (r, b)]

        x = self.state
        cartx = x[0] * scale + screen_width / 2.0  # MIDDLE OF CART
        self.carttrans.set_translation(cartx, carty)
        self.poletrans.set_rotation(-x[2])

        return self.viewer.render(return_rgb_array=mode == "rgb_array")

    def close(self):
        return self.env.close()

class Normalised_Env():
    def __init__(self, env, m, std):
        self.env = env
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

if __name__=='__main__':
    maxiter=10
    max_action=1.0 # actions for these environments are discrete
    T = 50
    J = 4
    N = 5
    T_sim = T
    lens = []
    target = np.array([0.0, 0.0])
    weights = np.diag([4.0, 3.0])

    env = mycartpole()

    if input("Give demonstration or not (y/n)\n") == 'y':
        Xc1, Yc1, X1, Y1 = rollout_both(env, timesteps=T, random=False, render=True)
    else:
        if os.path.exists('./examples/human/training_data_cp_X.npy') & os.path.exists('./examples/human/training_data_cp_Y.npy') \
        & os.path.exists('./examples/human/training_data_cp_Yc.npy') & os.path.exists('./examples/human/training_data_cp_Xc.npy'):
            Xc1 = np.load('./examples/human/training_data_cp_Xc.npy')
            Yc1 = np.load('./examples/human/training_data_cp_Yc.npy')
            X1 = np.load('./examples/human/training_data_cp_X.npy')
            Y1 = np.load('./examples/human/training_data_cp_Y.npy')
        else:
            raise Exception('Please give demonstration')

    # np.save('./examples/human/training_data_cp_X.npy', X)
    # np.save('./examples/human/training_data_cp_Y.npy', Y)
    # np.save('./examples/human/training_data_cp_Xc.npy', Xc)
    # np.save('./examples/human/training_data_cp_Yc.npy', Yc)

    # np.save('training_data_cp_X.npy', X)
    # np.save('training_data_cp_Y.npy', Y)
    # np.save('training_data_cp_Xc.npy', Xc)
    # np.save('training_data_cp_Yc.npy', Yc)

    Yc1 = Yc1[:,None]

    env = Normalised_Env(env, np.mean(X1[:,:4],0), np.std(X1[:,:4], 0))
    X = np.zeros(X1.shape)
    Xc = np.zeros(Xc1.shape)
    X[:, :4] = np.divide(X1[:, :4] - np.mean(X1[:,:4],0), np.std(X1[:,:4], 0))
    Xc = np.divide(Xc1 - np.mean(Xc1,0), np.std(Xc1, 0))
    X[:, 4] = X1[:,-1] # control inputs are not normalised
    Y = np.divide(Y1 , np.std(X1[:,:4], 0))
    Yc = Yc1

    data_c = [Xc,Yc]
    state_dim = Y.shape[1]
    control_dim = X.shape[1] - state_dim

    controller = CombController(data_c, max_action=max_action)

    R = ExponentialReward(state_dim=2, W=weights, t=target, select=[2,3])

    pilco = PILCO((X, Y), controller=controller, reward=R, horizon=T)

    # Initial random rollouts to generate a dataset
    for i in range(1,J):
        X_, Y_, _, _ = rollout(env, pilco, timesteps=T, random=False, render=True)
        X = np.vstack((X, X_))
        Y = np.vstack((Y, Y_))
    pilco.mgpr.set_data((X, Y))
    # print(X.shape); print(Y.shape)

    # for numerical stability
    r_new = np.zeros((T, 1))
    for model in pilco.mgpr.models:
        model.likelihood.variance.assign(0.05)
        set_trainable(model.likelihood.variance, False)
    
    re_p = []; count = []; re_pn = []
    for rollouts in range(N):
        print("**** ITERATION no", rollouts, " ****")
        pilco.optimize_models(maxiter=maxiter, restarts=2)
        pilco.optimize_policy(maxiter=maxiter, restarts=2)

        X_new, Y_new, _, _ = rollout(env, pilco, timesteps=T_sim, render=True)

        for i in range(len(X_new)):
            r_new[:, 0] = R.compute_reward(X_new[i,None,:-1], 0.001 * np.eye(state_dim))[0]
            total_r = sum(r_new)
            _, _, r = pilco.predict(X_new[0,None,:-1], 0.001 * np.diag(np.ones(state_dim) * 0.1), T)
        print("Total ", total_r, " Predicted: ", r)
        re_p.append(total_r)
        re_pn.append(r)
        count.append(rollouts)

        X = np.vstack((X, X_new)); Y = np.vstack((Y, Y_new))
        pilco.mgpr.set_data((X, Y))
        # print(X.shape); print(Y.shape)

    np.save('./examples/human/plot/Comb_cart_pole_X3.npy', count)
    np.save('./examples/human/plot/Comb_cart_pole_Y3.npy', re_p)
    np.save('./examples/human/plot/Comb_cart_pole_Yn3.npy', re_pn)

