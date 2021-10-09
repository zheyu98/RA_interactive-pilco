import numpy as np
import matplotlib.pyplot as plt
import os

def get_rwrd(time_str):
    rewards = np.load('./logs/' + time_str + '/rewards.npz')

    return rewards['total_r']

def get_rwrd_s(file_path):
    rewards = np.load(file_path)

    return rewards['total_r']


data_sets = ['25-03-2021-11.31.33', '25-03-2021-12.01.23', '25-03-2021-13.51.16', '25-03-2021-15.07.37', '25-03-2021-17.15.42']

data_sets_var = []

for file in os.listdir('./examples/WithVarianceRuns'):
    if '-10runs' in file:
        data_sets_var.append('./examples/WithVarianceRuns/' + file + '/rewards.npz')

#Select only 5 for fair comparison
data_sets_var = data_sets_var[:5]

data_var = []

for data_set in data_sets_var:
    r = get_rwrd_s(data_set)
    plt.plot(r)
    data_var.append(r)

plt.xticks(range(len(r)))
plt.xlabel('Rollout [-]')
plt.ylabel('Total Reward [-]')
plt.savefig('with_var_trials.png')
plt.show()

data = []

for data_set in data_sets:
    r = get_rwrd(data_set)
    plt.plot(r)
    data.append(r)

plt.xticks(range(len(r)))
plt.xlabel('Rollout [-]')
plt.ylabel('Total Reward [-]')
plt.savefig('no_var_trials.png')
plt.show()


mean_var = np.mean(data_var, axis=0)
std_var = np.std(data_var, axis=0)

plt.plot(mean_var)
plt.fill_between(range(len(mean_var)), mean_var-2*std_var, mean_var+2*std_var, alpha=.1)

plt.xticks(range(len(mean_var)))
plt.xlabel('Rollout [-]')
plt.ylabel('Total Reward [-]')
plt.savefig('with_var_conf.png')
plt.show()

mean = np.mean(data, axis=0)
std = np.std(data, axis=0)

plt.plot(mean)
plt.fill_between(range(len(mean)), mean-2*std, mean+2*std, alpha=.1)

plt.xticks(range(len(mean)))
plt.xlabel('Rollout [-]')
plt.ylabel('Total Reward [-]')
plt.savefig('no_var_conf.png')
plt.show()

plt.plot(mean_var)
plt.plot(mean)
plt.fill_between(range(len(mean_var)), mean_var-2*std_var, mean_var+2*std_var, alpha=.1)
plt.fill_between(range(len(mean)), mean-2*std, mean+2*std, alpha=.1)

plt.xticks(range(len(mean)))
plt.xlabel('Rollout [-]')
plt.ylabel('Total Reward [-]')
plt.legend(('With variance', 'Without variance'))
plt.savefig('conf.png')
plt.show()