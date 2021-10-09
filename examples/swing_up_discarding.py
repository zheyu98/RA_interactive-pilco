import numpy as np
import gym
from pilco.models import PILCO
from pilco.controllers import RbfController, LinearController
from pilco.rewards import ExponentialReward
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
    N = 7
    restarts = 2

    # PILCO is not too happy with GPU compute sometimes
    # Uncomment to disable GPU
    #  tf.config.set_visible_devices([], 'GPU')

    env = myPendulum()

    
    # Initial random rollouts to generate a dataset
    X, Y, _, _ = rollout(env, None, timesteps=T, random=True, SUBS=SUBS, render=True)
    for i in range(1,J):
        X_, Y_, _, _ = rollout(env, None, timesteps=T, random=True, SUBS=SUBS, verbose=True, render=True)
        X = np.vstack((X, X_))
        Y = np.vstack((Y, Y_))

    state_dim = Y.shape[1]
    control_dim = X.shape[1] - state_dim

    controller = RbfController(state_dim=state_dim, control_dim=control_dim, num_basis_functions=bf, max_action=max_action)
    R = ExponentialReward(state_dim=state_dim, t=target, W=weights)

    pilco = PILCO((X, Y), controller=controller, horizon=T, reward=R, m_init=m_init, S_init=S_init)

    timeStr = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    save_pilco('./logs/' + timeStr + '/rollout_init' + '/', X, Y, pilco)

    # for numerical stability, we can set the likelihood variance parameters of the GP models
    for model in pilco.mgpr.models:
        model.likelihood.variance.assign(0.001)
        set_trainable(model.likelihood.variance, False)

    total_r = np.zeros(N)
    predicted_r = np.zeros(N)
    r_new = np.zeros((T, 1))
    for rollouts in range(N):
        print("**** ITERATION no", rollouts, " ****")
        pilco.optimize_models(maxiter=maxiter, restarts=2)
        pilco.optimize_policy(maxiter=maxiter, restarts=2)

        save_pilco('./logs/' + timeStr + '/rollout' + str(rollouts) + '/', X, Y, pilco)

        X_new, Y_new, _, reward = rollout(env, pilco, timesteps=T_sim, verbose=True, SUBS=SUBS, render=True)

        # Get the actual reward from the rollout
        for i in range(T):
            r_new[i, 0] = R.compute_reward(X_new[i,None,:-1], 0.001 * np.eye(state_dim))[0]
        total_r[rollouts] = sum(r_new)

        # Predict the reward for the total rollout from the initial state from the model
        _, _, predicted_r[rollouts] = pilco.predict(X_new[0,None,:-1], 0.001 * S_init, T_sim)

        # The difference gives us an idea of the convergence
        print("Total ", total_r[rollouts], " Predicted: ", predicted_r[rollouts])

        if rollouts < N-1:
            # Update dataset
            X = np.vstack((X, X_new)); Y = np.vstack((Y, Y_new))
            pilco.mgpr.set_data((X, Y))

    # Assuming we've converged

    dl = 0.05

    lengths = 1 - np.linspace(0.05, 0.75, 15)


    total_r_changed = np.zeros(len(lengths)+1)
    predicted_r_changed = np.zeros(len(lengths)+1)
    for idx, length in enumerate(lengths):
        env.env.l = length

        print("**** ITERATION no", rollouts, " ****")

        X_new, Y_new, _, reward = rollout(env, pilco, timesteps=T_sim, verbose=True, SUBS=SUBS, render=True)

        # Get the actual reward from the rollout
        for i in range(T):
            r_new[i, 0] = R.compute_reward(X_new[i,None,:-1], 0.001 * np.eye(state_dim))[0]
        total_r_changed[rollouts] = sum(r_new)

        # Predict the reward for the total rollout from the initial state from the model
        _, _, predicted_r_changed[rollouts] = pilco.predict(X_new[0,None,:-1], 0.001 * S_init, T_sim)

        # The difference gives us an idea of the convergence
        print("Total ", total_r_changed[rollouts], " Predicted: ", predicted_r_changed[rollouts])

        # FIFO roll with X_new & Y_new
        X[:-len(X_new)] = X[len(X_new):]; X[-len(X_new):] = X_new
        Y[:-len(Y_new)] = Y[len(Y_new):]; Y[-len(Y_new):] = Y_new

        pilco.mgpr.set_data((X, Y))

        pilco.optimize_models(maxiter=maxiter, restarts=2)
        pilco.optimize_policy(maxiter=maxiter, restarts=2)

        save_pilco('./logs/' + timeStr + '/rollout' + str(rollouts+N) + '/', X, Y, pilco)

    #Do the last run

    X_new, Y_new, _, reward = rollout(env, pilco, timesteps=T_sim, verbose=True, SUBS=SUBS, render=True)

    # Get the actual reward from the rollout
    for i in range(T):
        r_new[i, 0] = R.compute_reward(X_new[i,None,:-1], 0.001 * np.eye(state_dim))[0]
    total_r_changed[len(lengths)] = sum(r_new)

    # Predict the reward for the total rollout from the initial state from the model
    _, _, predicted_r_changed[len(lengths)] = pilco.predict(X_new[0,None,:-1], 0.001 * S_init, T_sim)

    # The difference gives us an idea of the convergence
    print("Total ", total_r_changed[len(lengths)], " Predicted: ", predicted_r_changed[len(lengths)])

    np.savez('./logs/' + timeStr + '/rewards.npz', total_r=total_r, predicted_r=predicted_r, \
        lengths=lengths, total_r_changed=total_r_changed, predicted_r_changed=predicted_r_changed)
