import numpy as np
import matplotlib.pyplot as plt
import os


def get_rwrd_s(file_path):
    rewards = np.load(file_path)

    return rewards['total_r']



data_sets = []

for file in os.listdir('./model_change_results/'):
    data_sets.append(np.load('./model_change_results/' + file + '/rewards.npz'))

r_masses = []
for data_set in data_sets:
    r_masses.append(data_set['total_r_masses'])
    #plt.plot(data_set['masses'], data_set['total_r_masses'])

mean_var = np.mean(r_masses, axis=0)
std_var = np.std(r_masses, axis=0)

plt.plot(data_sets[0]['masses'], mean_var)
plt.fill_between(data_sets[0]['masses'], mean_var-2*std_var, mean_var+2*std_var, alpha=.1)

plt.xlabel('Pedulum Mass [kg]')
plt.ylabel('Total Reward [-]')
plt.savefig('mass_change.png')
plt.show()

r_lengths = []
for data_set in data_sets:
    r_lengths.append(data_set['total_r_lengths'])
    #plt.plot(data_set['masses'], data_set['total_r_masses'])

mean_var = np.mean(r_lengths, axis=0)
std_var = np.std(r_lengths, axis=0)

plt.plot(data_sets[0]['lengths'], mean_var)
plt.fill_between(data_sets[0]['lengths'], mean_var-2*std_var, mean_var+2*std_var, alpha=.1)

plt.xlabel('Pedulum Length [m]')
plt.ylabel('Total Reward [-]')
plt.savefig('length_change.png')
plt.show()

r_torques = []
for data_set in data_sets:
    r_torques.append(data_set['total_r_torques'])
    #plt.plot(data_set['masses'], data_set['total_r_masses'])

mean_var = np.mean(r_torques, axis=0)
std_var = np.std(r_torques, axis=0)

plt.plot(data_sets[0]['torques'], mean_var)
plt.fill_between(data_sets[0]['torques'], mean_var-2*std_var, mean_var+2*std_var, alpha=.1)

plt.xlabel('Pedulum Max Torque [Nm]')
plt.ylabel('Total Reward [-]')
plt.savefig('torque_change.png')
plt.show()

'''
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
'''