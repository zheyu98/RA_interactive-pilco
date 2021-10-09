import numpy as np
import gym
from pilco.models import PILCO
from pilco.controllers import RbfController, LinearController
from pilco.rewards import ExponentialReward, UnboundedExponentialReward
import tensorflow as tf
from utils import rollout, policy, save_pilco, load_pilco
from gpflow import set_trainable
from datetime import datetime
np.random.seed(0)

# NEEDS a different initialisation than the one in gym (change the reset() method),
# to (m_init, S_init), modifying the gym env

# Introduces subsampling with the parameter SUBS and modified rollout function
# Introduces priors for better conditioning of the GP model
# Uses restarts

class myPendulum():
    def __init__(self):
        self.env = gym.make('Pendulum-v0').env
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

    def step(self, action):
        return self.env.step(action)

    def reset(self):
        high = np.array([np.pi, 1])
        self.env.state = np.random.uniform(low=-high, high=high)
        self.env.state = np.random.uniform(low=0, high=0.01*high) # only difference
        self.env.state[0] += -np.pi
        self.env.last_u = None
        return self.env._get_obs()

    def render(self):
        self.env.render()

if __name__=='__main__':
    SUBS=3
    bf = 30
    maxiter=50
    max_action=2.0
    target = np.array([1.0, 0.0, 0.0])
    weights = np.diag([2.0, 2.0, 0.3])
    m_init = np.reshape([-1.0, 0, 0.0], (1,3))
    S_init = np.diag([0.01, 0.05, 0.01])
    T = 40
    T_sim = T
    J = 4
    N = 1
    restarts = 2
    continue_training = False

    env = myPendulum()

    # We should get this from the saved data really
    state_dim = 3
    control_dim = 4 - state_dim

    controller = RbfController(state_dim=state_dim, control_dim=control_dim, num_basis_functions=bf, max_action=max_action)
    R = ExponentialReward(state_dim=state_dim, t=target, W=weights)
    R2 = UnboundedExponentialReward(state_dim=state_dim, t=target, W=weights)

    # Initial random rollouts to generate a dataset
    pilco, X, Y = load_pilco('./logs/11-03-2021-20:19:21/rollout7/', controller=controller, reward=R, m_init=m_init, S_init=S_init)
    #pilco, X, Y = load_pilco('./logs/12-03-2021-12:23:25/rollout7/', controller=controller, reward=R2, m_init=m_init, S_init=S_init)
    #pilco, X, Y = load_pilco('./logs/15-03-2021-11:58:04/rollout9/', controller=controller, reward=R2, m_init=m_init, S_init=S_init)
    #pilco, X, Y = load_pilco('./logs/15-03-2021-13:38:08/rollout9/', controller=controller, reward=R, m_init=m_init, S_init=S_init)

    if continue_training:
        timeStr = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")


    r_new = np.zeros((T, 1))
    for rollouts in range(N):
        print("**** ITERATION no", rollouts, " ****")
        X_new, Y_new, _, _ = rollout(env, pilco, timesteps=T_sim, verbose=True, SUBS=SUBS, render=True)

        if continue_training:
            X = np.vstack((X, X_new)); Y = np.vstack((Y, Y_new))
            pilco.mgpr.set_data((X, Y))

            pilco.optimize_models(maxiter=maxiter, restarts=2)
            pilco.optimize_policy(maxiter=maxiter, restarts=2)
            save_pilco('./logs/' + timeStr + '/rollout' + str(rollouts) + '/', X, Y, pilco)

        # Since we had decide on the various parameters of the reward function
        # we might want to verify that it behaves as expected by inspection
        for i in range(T):
                r_new[i, 0] = pilco.reward.compute_reward(X_new[i,None,:-1], 0.001 * np.eye(pilco.state_dim))[0]
        total_r = sum(r_new)
        _, _, r = pilco.predict(X_new[0,None,:-1], 0.001 * S_init, T)
        print("Total ", total_r, " Predicted: ", r)
    
