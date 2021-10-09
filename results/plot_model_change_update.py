import numpy as np
import matplotlib.pyplot as plt
import os


data_sets = []

for file in os.listdir('./results/ModelChangeUpdate/'):
    data_sets.append(np.load('./results/ModelChangeUpdate/' + file + '/rewards.npz'))

'''
total_r = []
for data_set in data_sets:
    total_r.append(data_set['total_r'])
    #plt.plot(data_set['masses'], data_set['total_r_masses'])

mean_var = np.mean(total_r, axis=0)
std_var = np.std(total_r, axis=0)

x = range(len(mean_var))

plt.plot(x, mean_var)
plt.fill_between(x, mean_var-2*std_var, mean_var+2*std_var, alpha=.1)

plt.xlabel('Rollout [-]')
plt.ylabel('Total Reward [-]')
plt.savefig('test.png')
plt.show()
'''
total_r = []
for data_set in data_sets:
    total_r.append(np.append(data_set['total_r'][:3], data_set['total_r_changed'][3]))
    plt.plot(range(4), np.append(data_set['total_r'][:3], data_set['total_r_changed'][3]))

mean_var = np.mean(total_r, axis=0)
std_var = np.std(total_r, axis=0)

x = range(len(mean_var))

plt.xlabel('Rollout [-]')
plt.xticks(x)
plt.ylabel('Total Reward [-]')
plt.savefig('model_change_update.png')
plt.show()



plt.plot(x, mean_var)
plt.fill_between(x, mean_var-2*std_var, mean_var+2*std_var, alpha=.1)

plt.xlabel('Rollout [-]')
plt.xticks(x)
plt.ylabel('Total Reward [-]')
plt.savefig('model_change_update_conf.png')
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