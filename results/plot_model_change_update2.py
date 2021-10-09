import numpy as np
import matplotlib.pyplot as plt
import os


data_sets = []

for file in os.listdir('./results/ModelChangeUpdateMass/'):
    data_sets.append(np.load('./results/ModelChangeUpdateMass/' + file + '/rewards.npz'))

total_r = []
for data_set in data_sets:
    total_r.append(data_set['total_r_changed'])
    plt.plot(data_set['total_r_changed'])

mean_var = np.mean(total_r, axis=0)
std_var = np.std(total_r, axis=0)

x = range(len(mean_var))

plt.xlabel('Rollout [-]')
plt.xticks(x)
plt.ylabel('Total Reward [-]')
plt.savefig('model_change_update_mass.png')
plt.show()



plt.plot(x, mean_var)
plt.fill_between(x, mean_var-2*std_var, mean_var+2*std_var, alpha=.1)

plt.xlabel('Rollout [-]')
plt.xticks(x)
plt.ylabel('Total Reward [-]')
plt.savefig('model_change_update_conf_mass.png')
plt.show()